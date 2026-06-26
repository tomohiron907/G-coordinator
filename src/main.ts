import './style.css';
import './preview.ts';
import { initEditor, getCode, setCode, getCurrentFilePath, setCurrentFilePath } from './editor.ts';
import { initConsole, consoleClear, consoleLog, consoleError } from './console.ts';
import { initParameters, getSettings } from './parameters.ts';
import { showComputing } from './preview.ts';
import { invoke } from '@tauri-apps/api/core';
import { Pane } from 'tweakpane';

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

// ---- Machine Settings dialog ----

const msDialog = document.getElementById('machine-settings-dialog') as HTMLElement;
let msPane: Pane | null = null;

const msState = {
  hw: { kinematics: 'Cartesian', bed_size_x: 220, bed_size_y: 220, bed_size_z: 250 },
  nt: { tilt_code: 'B', rot_code: 'C', tilt_offset: 0, rot_offset: 0 },
  bt: { tilt_code: 'B', rot_code: 'C', tilt_offset: 0, rot_offset: 0, div_distance: 1.0 },
  br: { rot_code: 'C', rot_offset: 0, div_distance: 1.0 },
};

function msLoadState(settings: ReturnType<typeof getSettings>): void {
  if (!settings) return;
  const { Hardware: hw, Kinematics: kin } = settings;
  msState.hw.kinematics   = hw.kinematics;
  msState.hw.bed_size_x   = hw.bed_size.bed_size_x;
  msState.hw.bed_size_y   = hw.bed_size.bed_size_y;
  msState.hw.bed_size_z   = hw.bed_size.bed_size_z;
  msState.nt.tilt_code    = kin.NozzleTilt.tilt_code;
  msState.nt.rot_code     = kin.NozzleTilt.rot_code;
  msState.nt.tilt_offset  = kin.NozzleTilt.tilt_offset;
  msState.nt.rot_offset   = kin.NozzleTilt.rot_offset;
  msState.bt.tilt_code    = kin.BedTiltBC.tilt_code;
  msState.bt.rot_code     = kin.BedTiltBC.rot_code;
  msState.bt.tilt_offset  = kin.BedTiltBC.tilt_offset;
  msState.bt.rot_offset   = kin.BedTiltBC.rot_offset;
  msState.bt.div_distance = kin.BedTiltBC.div_distance;
  msState.br.rot_code     = kin.BedRotate.rot_code;
  msState.br.rot_offset   = kin.BedRotate.rot_offset;
  msState.br.div_distance = kin.BedRotate.div_distance;
}

function msBuildPane(): void {
  const container = document.getElementById('ms-tweakpane-container')!;
  msPane?.dispose();
  msPane = new Pane({ container });

  const fHW = msPane.addFolder({ title: 'Hardware', expanded: true });
  fHW.addBinding(msState.hw, 'kinematics', {
    label: 'Kinematics',
    options: { Cartesian: 'Cartesian', NozzleTilt: 'NozzleTilt', BedTilt: 'BedTilt', BedRotate: 'BedRotate' },
  });
  fHW.addBinding(msState.hw, 'bed_size_x', { label: 'Bed X (mm)', step: 1 });
  fHW.addBinding(msState.hw, 'bed_size_y', { label: 'Bed Y (mm)', step: 1 });
  fHW.addBinding(msState.hw, 'bed_size_z', { label: 'Bed Z (mm)', step: 1 });

  const fNT = msPane.addFolder({ title: 'NozzleTilt', expanded: true });
  fNT.addBinding(msState.nt, 'tilt_code',   { label: 'Tilt Axis' });
  fNT.addBinding(msState.nt, 'rot_code',    { label: 'Rot Axis' });
  fNT.addBinding(msState.nt, 'tilt_offset', { label: 'Tilt Offset', step: 0.1 });
  fNT.addBinding(msState.nt, 'rot_offset',  { label: 'Rot Offset',  step: 0.1 });

  const fBT = msPane.addFolder({ title: 'BedTiltBC', expanded: true });
  fBT.addBinding(msState.bt, 'tilt_code',    { label: 'Tilt Axis' });
  fBT.addBinding(msState.bt, 'rot_code',     { label: 'Rot Axis' });
  fBT.addBinding(msState.bt, 'tilt_offset',  { label: 'Tilt Offset',  step: 0.1 });
  fBT.addBinding(msState.bt, 'rot_offset',   { label: 'Rot Offset',   step: 0.1 });
  fBT.addBinding(msState.bt, 'div_distance', { label: 'Div Distance', step: 0.1 });

  const fBR = msPane.addFolder({ title: 'BedRotate', expanded: true });
  fBR.addBinding(msState.br, 'rot_code',     { label: 'Rot Axis' });
  fBR.addBinding(msState.br, 'rot_offset',   { label: 'Rot Offset',   step: 0.1 });
  fBR.addBinding(msState.br, 'div_distance', { label: 'Div Distance', step: 0.1 });

  const updateKinFolders = () => {
    fNT.hidden = msState.hw.kinematics !== 'NozzleTilt';
    fBT.hidden = msState.hw.kinematics !== 'BedTilt';
    fBR.hidden = msState.hw.kinematics !== 'BedRotate';
  };
  updateKinFolders();
  msPane.on('change', updateKinFolders);
}

function msClose(): void {
  msDialog.hidden = true;
}

document.getElementById('machine-settings-btn')!.addEventListener('click', async () => {
  try {
    const gcodeResult = await invoke<{ start_gcode: string; end_gcode: string }>('get_gcode_texts');
    msLoadState(getSettings());
    (document.getElementById('ms-start-gcode') as HTMLTextAreaElement).value = gcodeResult.start_gcode;
    (document.getElementById('ms-end-gcode')   as HTMLTextAreaElement).value = gcodeResult.end_gcode;
    msBuildPane();
    msDialog.hidden = false;
  } catch (e) {
    consoleError('Failed to open Machine Settings: ' + String(e));
  }
});

document.getElementById('ms-close-btn')!.addEventListener('click', msClose);
document.getElementById('ms-cancel-btn')!.addEventListener('click', msClose);
msDialog.addEventListener('click', (e) => { if (e.target === msDialog) msClose(); });

document.getElementById('ms-save-btn')!.addEventListener('click', async () => {
  const settings = getSettings();
  if (!settings) return;

  settings.Hardware.kinematics          = msState.hw.kinematics;
  settings.Hardware.bed_size.bed_size_x = msState.hw.bed_size_x;
  settings.Hardware.bed_size.bed_size_y = msState.hw.bed_size_y;
  settings.Hardware.bed_size.bed_size_z = msState.hw.bed_size_z;

  settings.Kinematics.NozzleTilt.tilt_code   = msState.nt.tilt_code;
  settings.Kinematics.NozzleTilt.rot_code    = msState.nt.rot_code;
  settings.Kinematics.NozzleTilt.tilt_offset = msState.nt.tilt_offset;
  settings.Kinematics.NozzleTilt.rot_offset  = msState.nt.rot_offset;

  settings.Kinematics.BedTiltBC.tilt_code    = msState.bt.tilt_code;
  settings.Kinematics.BedTiltBC.rot_code     = msState.bt.rot_code;
  settings.Kinematics.BedTiltBC.tilt_offset  = msState.bt.tilt_offset;
  settings.Kinematics.BedTiltBC.rot_offset   = msState.bt.rot_offset;
  settings.Kinematics.BedTiltBC.div_distance = msState.bt.div_distance;

  settings.Kinematics.BedRotate.rot_code     = msState.br.rot_code;
  settings.Kinematics.BedRotate.rot_offset   = msState.br.rot_offset;
  settings.Kinematics.BedRotate.div_distance = msState.br.div_distance;

  const startGcode = (document.getElementById('ms-start-gcode') as HTMLTextAreaElement).value;
  const endGcode   = (document.getElementById('ms-end-gcode')   as HTMLTextAreaElement).value;

  try {
    await Promise.all([
      invoke('save_settings', { settings }),
      invoke('save_gcode_texts', { startGcode, endGcode }),
    ]);
    msClose();
    consoleLog('Machine settings saved.');
  } catch (e) {
    consoleError('Failed to save machine settings: ' + String(e));
  }
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
