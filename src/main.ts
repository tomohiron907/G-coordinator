import './style.css';
import './preview.ts';
import { initEditor, getCode, setCode, getCurrentFilePath, setCurrentFilePath } from './editor.ts';
import { initConsole, consoleClear, consoleLog, consoleError } from './console.ts';
import { initParameters, getSettings } from './parameters.ts';
import { showComputing } from './preview.ts';
import { invoke } from '@tauri-apps/api/core';

// ---- Init ----

initConsole('console-output');
initEditor('monaco-container');

let lastPickleB64: string | null = null;

initParameters('tweakpane-container').catch(console.error);

// ---- Run button ----

document.getElementById('run-btn')!.addEventListener('click', async () => {
  const code = getCode();
  const settings = getSettings();
  if (!settings) return;

  consoleClear();
  showComputing(true);
  document.getElementById('run-btn')!.setAttribute('disabled', '');
  document.getElementById('export-gcode-btn')!.setAttribute('disabled', '');

  try {
    const result: {
      success: boolean;
      stdout: string;
      error?: string;
      path_lengths?: number[];
      coords_b64?: string;
      travel_path_lengths?: number[];
      travel_coords_b64?: string;
      nozzleSize?: number;
      pickle_b64?: string;
    } = await invoke('run_script', { code, settings });

    if (result.stdout) {
      consoleLog(result.stdout);
    }

    if (!result.success) {
      consoleError(result.error ?? 'Unknown error');
      showComputing(false);
      return;
    }

    lastPickleB64 = result.pickle_b64 ?? null;
    document.getElementById('export-gcode-btn')!.removeAttribute('disabled');

    // Emit preview update via Tauri event (already listened in preview.ts)
    // Instead, call applyPreviewData directly
    const { applyPreviewData } = await import('./preview.ts');
    applyPreviewData({
      path_lengths: result.path_lengths ?? [],
      coords_b64: result.coords_b64 ?? '',
      travel_path_lengths: result.travel_path_lengths ?? [],
      travel_coords_b64: result.travel_coords_b64 ?? '',
      nozzleSize: result.nozzleSize ?? settings.Print.nozzle.nozzle_diameter,
    });

  } catch (e: unknown) {
    const msg = e instanceof Error ? e.message : String(e);
    consoleError('Error: ' + msg);
    showComputing(false);
  } finally {
    document.getElementById('run-btn')!.removeAttribute('disabled');
  }
});

// ---- Open file button ----

document.getElementById('open-btn')!.addEventListener('click', async () => {
  try {
    const result: { path: string; content: string } | null = await invoke('open_file');
    if (result) {
      setCode(result.content);
      setCurrentFilePath(result.path);
      consoleClear();
      consoleLog(`Opened: ${result.path}`);
    }
  } catch (e: unknown) {
    consoleError('Failed to open file: ' + String(e));
  }
});

// ---- Export G-code button ----

document.getElementById('export-gcode-btn')!.addEventListener('click', async () => {
  if (!lastPickleB64) {
    consoleError('Run the script first to generate print paths.');
    return;
  }
  const settings = getSettings();
  if (!settings) return;

  consoleLog('Generating G-code...');

  try {
    const result: { success: boolean; gcode?: string; error?: string } = await invoke('export_gcode', {
      pickleB64: lastPickleB64,
      settings,
    });

    if (!result.success || !result.gcode) {
      consoleError('G-code generation failed: ' + (result.error ?? 'unknown error'));
      return;
    }

    const savedPath: string | null = await invoke('save_gcode_dialog', { gcode: result.gcode });
    if (savedPath) {
      consoleLog('G-code saved: ' + savedPath);
    }
  } catch (e: unknown) {
    consoleError('Export failed: ' + String(e));
  }
});

// ---- Machine Settings button ----

document.getElementById('machine-settings-btn')!.addEventListener('click', () => {
  consoleLog('Machine Settings window is not yet implemented in Tauri version.');
});

// ---- Resizable panes ----

setupResizer('v-resize-left', 'left-pane', 'width', true);
setupResizer('v-resize-right', 'right-pane', 'width', false);
setupResizer('h-resize-handle', 'console-wrapper', 'height', false);

function setupResizer(handleId: string, targetId: string, dimension: 'width' | 'height', leftOrTop: boolean): void {
  const handle = document.getElementById(handleId)!;
  const target = document.getElementById(targetId)!;

  let startPos = 0;
  let startSize = 0;

  handle.addEventListener('mousedown', (e) => {
    e.preventDefault();
    handle.classList.add('dragging');
    startPos = dimension === 'width' ? e.clientX : e.clientY;
    startSize = dimension === 'width' ? target.offsetWidth : target.offsetHeight;

    const onMove = (e: MouseEvent) => {
      const current = dimension === 'width' ? e.clientX : e.clientY;
      const delta = leftOrTop ? current - startPos : startPos - current;
      const newSize = Math.max(80, startSize + delta);
      target.style[dimension] = newSize + 'px';
    };

    const onUp = () => {
      handle.classList.remove('dragging');
      window.removeEventListener('mousemove', onMove);
      window.removeEventListener('mouseup', onUp);
      window.dispatchEvent(new Event('resize'));
    };

    window.addEventListener('mousemove', onMove);
    window.addEventListener('mouseup', onUp);
  });
}
