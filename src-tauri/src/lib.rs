use std::io::Write;
use std::path::PathBuf;
use std::process::{Command, Stdio};

use serde_json::Value;
use tauri::{AppHandle, Manager};

// ---- Subprocess helpers ----

fn workspace_root() -> PathBuf {
    // During `tauri dev` the CWD is the workspace root (where tauri.conf.json lives)
    // adjusted one level up from src-tauri.
    let cwd = std::env::current_dir().unwrap_or_default();
    // If CWD ends in "src-tauri", go up
    if cwd.file_name().and_then(|n| n.to_str()) == Some("src-tauri") {
        cwd.parent().map(|p| p.to_path_buf()).unwrap_or(cwd)
    } else {
        cwd
    }
}

fn make_python_cmd(app: &AppHandle, script: &str) -> Command {
    #[cfg(debug_assertions)]
    {
        let _ = app;
        let root = workspace_root();
        let python = root.join(".venv").join("bin").join("python3");
        let mut cmd = Command::new(python);
        cmd.arg(root.join("python").join(script));
        cmd
    }
    #[cfg(not(debug_assertions))]
    {
        // Sidecar binary: e.g. runner-aarch64-apple-darwin
        let stem = script.trim_end_matches(".py");
        let triple = tauri::utils::platform::target_triple().unwrap_or_default();
        let bin_name = format!("{}-{}", stem, triple);
        let resource_dir = app.path().resource_dir().unwrap_or_default();
        Command::new(resource_dir.join("binaries").join(bin_name))
    }
}

fn run_subprocess(mut cmd: Command, input: &str) -> Result<Value, String> {
    let mut child = cmd
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| format!("Failed to spawn subprocess: {e}"))?;

    if let Some(mut stdin) = child.stdin.take() {
        stdin
            .write_all(input.as_bytes())
            .map_err(|e| format!("Failed to write stdin: {e}"))?;
    }

    let output = child
        .wait_with_output()
        .map_err(|e| format!("Subprocess wait failed: {e}"))?;

    if output.status.success() {
        let stdout = String::from_utf8_lossy(&output.stdout);
        serde_json::from_str(stdout.trim())
            .map_err(|e| format!("JSON parse error: {e}\nstdout: {stdout}"))
    } else {
        let stderr = String::from_utf8_lossy(&output.stderr);
        Err(format!(
            "Subprocess exited with {}\nstderr: {}",
            output.status, stderr
        ))
    }
}

// ---- Settings helpers ----

fn settings_path(app: &AppHandle) -> PathBuf {
    app.path()
        .app_config_dir()
        .unwrap_or_else(|_| PathBuf::from("."))
        .join("settings.json")
}

fn default_settings_path(app: &AppHandle) -> PathBuf {
    app.path()
        .resource_dir()
        .unwrap_or_else(|_| workspace_root().join("src"))
        .join("settings")
        .join("settings.json")
}

// ---- G-code helpers ----

fn gcode_user_path(app: &AppHandle, name: &str) -> PathBuf {
    app.path()
        .app_config_dir()
        .unwrap_or_else(|_| PathBuf::from("."))
        .join(name)
}

fn gcode_default_path(app: &AppHandle, name: &str) -> PathBuf {
    app.path()
        .resource_dir()
        .unwrap_or_else(|_| workspace_root().join("src"))
        .join("settings")
        .join(name)
}

fn read_gcode(app: &AppHandle, name: &str) -> String {
    let user_path = gcode_user_path(app, name);
    if user_path.exists() {
        std::fs::read_to_string(user_path).unwrap_or_default()
    } else {
        std::fs::read_to_string(gcode_default_path(app, name)).unwrap_or_default()
    }
}

// ---- Tauri commands ----

#[tauri::command]
async fn run_script(
    code: String,
    settings: Value,
    app: AppHandle,
) -> Result<Value, String> {
    let input = serde_json::json!({ "code": code, "settings": settings });
    let input_str = input.to_string();

    let cmd = make_python_cmd(&app, "runner.py");
    tokio::task::spawn_blocking(move || run_subprocess(cmd, &input_str))
        .await
        .map_err(|e| e.to_string())?
}

#[tauri::command]
async fn export_gcode(
    pickle_b64: String,
    settings: Value,
    app: AppHandle,
) -> Result<Value, String> {
    let start_gcode = read_gcode(&app, "start_gcode.txt");
    let end_gcode   = read_gcode(&app, "end_gcode.txt");

    let input = serde_json::json!({
        "pickle_b64": pickle_b64,
        "settings":   settings,
        "start_gcode": start_gcode,
        "end_gcode":   end_gcode,
    });
    let input_str = input.to_string();
    let cmd = make_python_cmd(&app, "gcode_gen.py");

    tokio::task::spawn_blocking(move || run_subprocess(cmd, &input_str))
        .await
        .map_err(|e| e.to_string())?
}

#[tauri::command]
fn get_settings(app: AppHandle) -> Result<Value, String> {
    let path = settings_path(&app);
    if path.exists() {
        let raw = std::fs::read_to_string(&path)
            .map_err(|e| format!("Failed to read settings: {e}"))?;
        serde_json::from_str(&raw).map_err(|e| format!("Invalid settings JSON: {e}"))
    } else {
        // Fall back to bundled default
        let default = default_settings_path(&app);
        let raw = std::fs::read_to_string(&default)
            .map_err(|e| format!("Failed to read default settings: {e}"))?;
        let parsed: Value =
            serde_json::from_str(&raw).map_err(|e| format!("Invalid default settings: {e}"))?;
        // Persist it
        if let Some(parent) = path.parent() {
            std::fs::create_dir_all(parent).ok();
        }
        std::fs::write(&path, &raw).ok();
        Ok(parsed)
    }
}

#[tauri::command]
fn save_settings(settings: Value, app: AppHandle) -> Result<(), String> {
    let path = settings_path(&app);
    if let Some(parent) = path.parent() {
        std::fs::create_dir_all(parent)
            .map_err(|e| format!("Failed to create settings dir: {e}"))?;
    }
    let raw = serde_json::to_string_pretty(&settings)
        .map_err(|e| format!("Failed to serialize settings: {e}"))?;
    std::fs::write(&path, raw).map_err(|e| format!("Failed to write settings: {e}"))
}

#[tauri::command]
fn get_gcode_texts(app: AppHandle) -> Result<Value, String> {
    Ok(serde_json::json!({
        "start_gcode": read_gcode(&app, "start_gcode.txt"),
        "end_gcode":   read_gcode(&app, "end_gcode.txt"),
    }))
}

#[tauri::command]
fn save_gcode_texts(start_gcode: String, end_gcode: String, app: AppHandle) -> Result<(), String> {
    let config_dir = app.path()
        .app_config_dir()
        .map_err(|e| format!("Failed to get config dir: {e}"))?;
    std::fs::create_dir_all(&config_dir)
        .map_err(|e| format!("Failed to create config dir: {e}"))?;
    std::fs::write(config_dir.join("start_gcode.txt"), start_gcode)
        .map_err(|e| format!("Failed to write start_gcode.txt: {e}"))?;
    std::fs::write(config_dir.join("end_gcode.txt"), end_gcode)
        .map_err(|e| format!("Failed to write end_gcode.txt: {e}"))?;
    Ok(())
}

#[tauri::command]
async fn open_file(app: AppHandle) -> Result<Option<Value>, String> {
    use tauri_plugin_dialog::DialogExt;

    let file = app
        .dialog()
        .file()
        .add_filter("Python", &["py"])
        .blocking_pick_file();

    match file {
        Some(fp) => {
            let path = fp.into_path().map_err(|e| format!("Invalid path: {e}"))?;
            let path_str = path.to_string_lossy().to_string();
            let content = std::fs::read_to_string(&path)
                .map_err(|e| format!("Failed to read file: {e}"))?;
            Ok(Some(serde_json::json!({ "path": path_str, "content": content })))
        }
        None => Ok(None),
    }
}

#[tauri::command]
fn save_script(path: String, code: String) -> Result<(), String> {
    std::fs::write(&path, code)
        .map_err(|e| format!("Failed to save file: {e}"))
}

#[tauri::command]
async fn save_script_dialog(code: String, app: AppHandle) -> Result<Option<String>, String> {
    use tauri_plugin_dialog::DialogExt;

    let path = app
        .dialog()
        .file()
        .add_filter("Python", &["py"])
        .set_file_name("untitled.py")
        .blocking_save_file();

    match path {
        Some(fp) => {
            let p = fp.into_path().map_err(|e| format!("Invalid path: {e}"))?;
            let path_str = p.to_string_lossy().to_string();
            std::fs::write(&p, code)
                .map_err(|e| format!("Failed to save file: {e}"))?;
            Ok(Some(path_str))
        }
        None => Ok(None),
    }
}

#[tauri::command]
async fn save_gcode_dialog(gcode: String, app: AppHandle) -> Result<Option<String>, String> {
    use tauri_plugin_dialog::DialogExt;

    let path = app
        .dialog()
        .file()
        .add_filter("G-code", &["gcode", "g"])
        .set_file_name("output.gcode")
        .blocking_save_file();

    match path {
        Some(fp) => {
            let p = fp.into_path().map_err(|e| format!("Invalid path: {e}"))?;
            let path_str = p.to_string_lossy().to_string();
            std::fs::write(&p, gcode)
                .map_err(|e| format!("Failed to write G-code: {e}"))?;
            Ok(Some(path_str))
        }
        None => Ok(None),
    }
}

// ---- App entry point ----

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_fs::init())
        .invoke_handler(tauri::generate_handler![
            run_script,
            export_gcode,
            get_settings,
            save_settings,
            open_file,
            save_script,
            save_script_dialog,
            save_gcode_dialog,
            get_gcode_texts,
            save_gcode_texts,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
