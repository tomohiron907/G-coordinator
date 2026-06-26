import { Pane } from 'tweakpane';
import { invoke } from '@tauri-apps/api/core';

export interface Settings {
  Print: {
    nozzle: { nozzle_diameter: number; filament_diameter: number };
    layer: { layer_height: number };
    speed: { print_speed: number; travel_speed: number };
    origin: { x: number; y: number };
    fan_speed: { fan_speed: number };
    temperature: { nozzle_temperature: number; bed_temperature: number };
    travel_option: {
      retraction: boolean;
      retraction_distance: number;
      unretraction_distance: number;
      z_hop: boolean;
      z_hop_distance: number;
    };
    extrusion_option: { extrusion_multiplier: number };
  };
  Hardware: {
    kinematics: string;
    bed_size: { bed_size_x: number; bed_size_y: number; bed_size_z: number };
  };
  Kinematics: {
    NozzleTilt: { tilt_code: string; rot_code: string; tilt_offset: number; rot_offset: number };
    BedTiltBC:  { tilt_code: string; rot_code: string; tilt_offset: number; rot_offset: number; div_distance: number };
    BedRotate:  { rot_code: string; rot_offset: number; div_distance: number };
  };
}

let pane: Pane | null = null;
let currentSettings: Settings | null = null;

export function getSettings(): Settings | null {
  return currentSettings;
}

export async function initParameters(containerId: string): Promise<Settings> {
  const container = document.getElementById(containerId) as HTMLElement;

  const settings: Settings = await invoke('get_settings');
  currentSettings = settings;

  pane = new Pane({ container });

  const print = settings.Print;

  const fNozzle = pane.addFolder({ title: 'Nozzle', expanded: true });
  fNozzle.addBinding(print.nozzle, 'nozzle_diameter', { label: 'Diameter', min: 0.1, max: 2.0, step: 0.05 });
  fNozzle.addBinding(print.nozzle, 'filament_diameter', { label: 'Filament ⌀', min: 1.0, max: 3.0, step: 0.05 });

  const fLayer = pane.addFolder({ title: 'Layer', expanded: true });
  fLayer.addBinding(print.layer, 'layer_height', { label: 'Height', min: 0.05, max: 1.0, step: 0.01 });

  const fSpeed = pane.addFolder({ title: 'Speed', expanded: false });
  fSpeed.addBinding(print.speed, 'print_speed', { label: 'Print', min: 100, max: 100000, step: 100 });
  fSpeed.addBinding(print.speed, 'travel_speed', { label: 'Travel', min: 100, max: 100000, step: 100 });

  const fTemp = pane.addFolder({ title: 'Temperature', expanded: false });
  fTemp.addBinding(print.temperature, 'nozzle_temperature', { label: 'Nozzle', min: 150, max: 300, step: 1 });
  fTemp.addBinding(print.temperature, 'bed_temperature', { label: 'Bed', min: 0, max: 120, step: 1 });

  const fFan = pane.addFolder({ title: 'Fan', expanded: false });
  fFan.addBinding(print.fan_speed, 'fan_speed', { label: 'Speed', min: 0, max: 255, step: 1 });

  const fOrigin = pane.addFolder({ title: 'Origin', expanded: false });
  fOrigin.addBinding(print.origin, 'x', { label: 'X', min: -300, max: 300, step: 0.5 });
  fOrigin.addBinding(print.origin, 'y', { label: 'Y', min: -300, max: 300, step: 0.5 });

  const fTravel = pane.addFolder({ title: 'Travel', expanded: false });
  fTravel.addBinding(print.travel_option, 'retraction', { label: 'Retraction' });
  fTravel.addBinding(print.travel_option, 'retraction_distance', { label: 'Retract Dist', min: 0, max: 10, step: 0.1 });
  fTravel.addBinding(print.travel_option, 'unretraction_distance', { label: 'Unretract Dist', min: 0, max: 10, step: 0.1 });
  fTravel.addBinding(print.travel_option, 'z_hop', { label: 'Z-hop' });
  fTravel.addBinding(print.travel_option, 'z_hop_distance', { label: 'Z-hop Dist', min: 0, max: 10, step: 0.1 });

  const fExtrusion = pane.addFolder({ title: 'Extrusion', expanded: false });
  fExtrusion.addBinding(print.extrusion_option, 'extrusion_multiplier', { label: 'Multiplier', min: 0.5, max: 2.0, step: 0.01 });

  pane.on('change', () => {
    saveSettings();
  });

  return settings;
}

async function saveSettings(): Promise<void> {
  if (!currentSettings) return;
  try {
    await invoke('save_settings', { settings: currentSettings });
  } catch (e) {
    console.error('Failed to save settings:', e);
  }
}
