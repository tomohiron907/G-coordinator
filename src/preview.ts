import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { Line2 } from 'three/addons/lines/Line2.js';
import { LineMaterial } from 'three/addons/lines/LineMaterial.js';
import { LineGeometry } from 'three/addons/lines/LineGeometry.js';
import { listen } from '@tauri-apps/api/event';

// ---- Scene setup ----

const container = document.getElementById('canvas-container') as HTMLElement;

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setClearColor(0x1e1e1e);
container.appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.fog = null;

const camera = new THREE.PerspectiveCamera(
    60,
    container.clientWidth / container.clientHeight,
    0.1,
    10000
);
camera.position.set(110, -70, 200);
camera.up.set(0, 0, 1);
camera.lookAt(110, 110, 0);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.target.set(110, 110, 0);

// ---- Render on demand ----

let needsRender = true;
function scheduleRender(): void { needsRender = true; }

// Fires on every camera change (including during damping), so damping frames are covered.
controls.addEventListener('change', scheduleRender);

// ---- Shared materials ----

const brightMaterial = new THREE.MeshPhongMaterial({ color: 0xffffff, side: THREE.FrontSide, flatShading: true, shininess: 60 });
const dimMaterial    = new THREE.MeshPhongMaterial({ color: 0x555555, side: THREE.FrontSide, flatShading: true, shininess: 60 });

// ---- Origin marker: axes + XYZ labels ----

function makeAxisLabel(text: string, color: string): THREE.Sprite {
    const canvas = document.createElement('canvas');
    canvas.width = 64;
    canvas.height = 64;
    const ctx = canvas.getContext('2d')!;
    ctx.font = 'Bold 52px sans-serif';
    ctx.fillStyle = color;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(text, 32, 32);
    const mat = new THREE.SpriteMaterial({
        map: new THREE.CanvasTexture(canvas),
        depthTest: true,
        depthWrite: false,
    });
    const sprite = new THREE.Sprite(mat);
    sprite.scale.set(4, 4, 1);
    sprite.renderOrder = 1;
    return sprite;
}

const AXES_SIZE = 30;
const axes = new THREE.AxesHelper(AXES_SIZE);
const axesMat = axes.material as THREE.LineBasicMaterial;
axesMat.depthTest = true;
axesMat.depthWrite = false;
axes.renderOrder = 1;

const xLabel = makeAxisLabel('X', '#ff4444');
xLabel.position.set(AXES_SIZE + 6, 0, 0);
const yLabel = makeAxisLabel('Y', '#44ff44');
yLabel.position.set(0, AXES_SIZE + 6, 0);
const zLabel = makeAxisLabel('Z', '#4488ff');
zLabel.position.set(0, 0, AXES_SIZE + 6);

const originGroup = new THREE.Group();
originGroup.add(axes, xLabel, yLabel, zLabel);
scene.add(originGroup);

// ---- Print path group (offset by origin so user-space (0,0) aligns with axes) ----
const pathGroup = new THREE.Group();
scene.add(pathGroup);

// ---- Bed visualization (dynamic) ----

let bedGrid: THREE.LineSegments | null = null;
let bedOutline: THREE.LineSegments | null = null;

export function updateBedSize(bedX: number, bedY: number): void {
    if (bedGrid) {
        scene.remove(bedGrid);
        bedGrid.geometry.dispose();
        (bedGrid.material as THREE.Material).dispose();
        bedGrid = null;
    }
    if (bedOutline) {
        scene.remove(bedOutline);
        bedOutline.geometry.dispose();
        (bedOutline.material as THREE.Material).dispose();
        bedOutline = null;
    }

    // Rectangular grid from (0,0) to (bedX, bedY) — 10mm spacing
    const step = 10;
    const gridPts: number[] = [];
    for (let y = 0; y <= bedY + 0.001; y += step) {
        gridPts.push(0, y, 0,  bedX, y, 0);
    }
    for (let x = 0; x <= bedX + 0.001; x += step) {
        gridPts.push(x, 0, 0,  x, bedY, 0);
    }
    const gridGeo = new THREE.BufferGeometry();
    gridGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(gridPts), 3));
    bedGrid = new THREE.LineSegments(gridGeo, new THREE.LineBasicMaterial({ color: 0x333333, depthWrite: false }));
    bedGrid.renderOrder = -1;
    scene.add(bedGrid);

    // Bed boundary outline (brighter)
    const outlinePts = new Float32Array([
        0,    0,    0,   bedX, 0,    0,
        bedX, 0,    0,   bedX, bedY, 0,
        bedX, bedY, 0,   0,    bedY, 0,
        0,    bedY, 0,   0,    0,    0,
    ]);
    const outlineGeo = new THREE.BufferGeometry();
    outlineGeo.setAttribute('position', new THREE.BufferAttribute(outlinePts, 3));
    bedOutline = new THREE.LineSegments(outlineGeo, new THREE.LineBasicMaterial({ color: 0x888888, depthWrite: false }));
    bedOutline.renderOrder = -1;
    scene.add(bedOutline);
    scheduleRender();
}

export function updateOrigin(x: number, y: number): void {
    originGroup.position.set(x, y, 0);
    pathGroup.position.set(x, y, 0);
    scheduleRender();
}

// Initialize with defaults; overridden once settings load
updateBedSize(220, 220);

const ambientLight = new THREE.AmbientLight(0xffffff, 0.15);
scene.add(ambientLight);

const dirLight1 = new THREE.DirectionalLight(0xffffff, 1.2);
dirLight1.position.set(1, -1, 2);
scene.add(dirLight1);

const dirLight2 = new THREE.DirectionalLight(0xffffff, 0.5);
dirLight2.position.set(-1, 1, -1);
scene.add(dirLight2);

// ---- Nozzle cone ----

const NOZZLE_HEIGHT = 10;
const nozzleGeo = new THREE.ConeGeometry(4, NOZZLE_HEIGHT, 16);
const nozzleMat = new THREE.MeshPhongMaterial({
    color: 0xffffff,
    transparent: true,
    opacity: 0.45,
    depthWrite: false,
    side: THREE.DoubleSide,
});
const nozzleMesh = new THREE.Mesh(nozzleGeo, nozzleMat);
nozzleMesh.rotation.x = -Math.PI / 2;
nozzleMesh.visible = false;
pathGroup.add(nozzleMesh);

// ---- State ----

let pathMeshes: THREE.Mesh[] = [];
let travelLines: Line2[] = [];
let travelLineMaterials: LineMaterial[] = [];
let storedPathLengths: number[] = [];
let storedLayerCoords: Float32Array[] = [];
let storedTravelCoords: Float32Array[] = [];
let storedTravelPathLengths: number[] = [];
let currentTopIndex = -1;

// ---- Vertical slider (layer range) ----

const vSlider    = document.getElementById('layer-slider') as HTMLInputElement;
const vValLabel  = document.getElementById('layer-val')   as HTMLElement;
const totalLabel = document.getElementById('layer-total') as HTMLElement;

function applyVerticalSlider(): void {
    const total = pathMeshes.length;
    if (total === 0) { return; }

    const maxVisible = parseInt(vSlider.value, 10);

    if (currentTopIndex >= 0 && currentTopIndex < pathMeshes.length) {
        const prevN = storedPathLengths[currentTopIndex];
        pathMeshes[currentTopIndex].geometry.setDrawRange(0, (prevN - 1) * 24);
    }

    dimLowerLayers(false);

    vValLabel.textContent = String(maxVisible + 1);
    pathMeshes.forEach((mesh, i) => {
        mesh.visible = i <= maxVisible;
    });
    travelLines.forEach((line, i) => {
        const vis = (i + 1) <= maxVisible;
        line.visible = vis;
        if (vis) {
            (line.geometry as LineGeometry).instanceCount = Infinity;
        } else {
            (line.geometry as LineGeometry).instanceCount = 0;
        }
    });

    currentTopIndex = maxVisible;

    const topLen = storedPathLengths[maxVisible];
    const travelExtra = (storedTravelPathLengths[maxVisible] ?? 0) > 0
        ? (storedTravelPathLengths[maxVisible] + 1) : 0;
    const totalLen = topLen + travelExtra;
    hSlider.min   = '1';
    hSlider.max   = String(totalLen);
    hSlider.value = String(totalLen);
    hTotalLabel.textContent = String(totalLen);
    updateSliderFill(vSlider, '--v-fill', true);
    applyHorizontalSlider();
    scheduleRender();
}

vSlider.addEventListener('input', applyVerticalSlider);

function updateSliderFill(slider: HTMLInputElement, prop: string, toTop: boolean): void {
    const min = parseFloat(slider.min) || 0;
    const max = parseFloat(slider.max) || 1;
    const val = parseFloat(slider.value) || 0;
    const pct = max > min ? ((val - min) / (max - min)) * 100 : 100;
    slider.style.setProperty(prop, `${pct.toFixed(1)}%`);
}

// ---- Horizontal slider (curve range of the top layer) ----

const hSlider      = document.getElementById('curve-slider') as HTMLInputElement;
const hValLabel    = document.getElementById('curve-val')   as HTMLElement;
const hTotalLabel  = document.getElementById('curve-total') as HTMLElement;

function dimLowerLayers(dim: boolean): void {
    pathMeshes.forEach((mesh, i) => {
        if (i < currentTopIndex) {
            mesh.material = dim ? dimMaterial : brightMaterial;
        }
    });
}

function applyHorizontalSlider(): void {
    if (currentTopIndex < 0 || pathMeshes.length === 0) { return; }
    const pointCount = parseInt(hSlider.value, 10);
    const mainLen    = storedPathLengths[currentTopIndex];
    const maxPoints  = parseInt(hSlider.max, 10);

    if (pointCount <= mainLen) {
        const indexCount = Math.max(0, pointCount - 1) * 24;
        pathMeshes[currentTopIndex].geometry.setDrawRange(0, indexCount);
        const tl = travelLines[currentTopIndex];
        if (tl) { tl.visible = false; (tl.geometry as LineGeometry).instanceCount = 0; }
        hValLabel.textContent = String(pointCount);
        dimLowerLayers(pointCount < maxPoints);
        updateNozzle(currentTopIndex, pointCount - 1);
    } else {
        pathMeshes[currentTopIndex].geometry.setDrawRange(0, (mainLen - 1) * 24);
        const travelStep = pointCount - mainLen;
        const tl   = travelLines[currentTopIndex];
        const tPts = storedTravelCoords[currentTopIndex];
        if (tl && tPts) {
            tl.visible = true;
            (tl.geometry as LineGeometry).instanceCount = travelStep;
            nozzleMesh.position.set(
                tPts[travelStep * 3],
                tPts[travelStep * 3 + 1],
                tPts[travelStep * 3 + 2] + NOZZLE_HEIGHT / 2
            );
            nozzleMesh.visible = true;
        }
        hValLabel.textContent = String(pointCount);
        dimLowerLayers(true);
    }
    updateSliderFill(hSlider, '--h-fill', false);
    scheduleRender();
}

hSlider.addEventListener('input', applyHorizontalSlider);

// ---- Nozzle update ----

function updateNozzle(layerIndex: number, pointIndex: number): void {
    const coords = storedLayerCoords[layerIndex];
    if (!coords) { nozzleMesh.visible = false; return; }

    nozzleMesh.position.set(
        coords[pointIndex * 3],
        coords[pointIndex * 3 + 1],
        coords[pointIndex * 3 + 2] + NOZZLE_HEIGHT / 2
    );
    nozzleMesh.visible = true;
}

// ---- Helpers ----

function b64ToFloat32Array(b64: string): Float32Array {
    const binary = atob(b64);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {
        bytes[i] = binary.charCodeAt(i);
    }
    return new Float32Array(bytes.buffer);
}

// ---- Diamond tube geometry builder ----

const _Z_AXIS = new THREE.Vector3(0, 0, 1);
const _X_AXIS = new THREE.Vector3(1, 0, 0);

function buildDiamondTube(positions: Float32Array, N: number, nozzleSize: number): THREE.BufferGeometry {
    const halfWidth  = nozzleSize / 2;
    const halfHeight = nozzleSize / 4;

    const posOut   = new Float32Array(12 * N);
    const indexOut = new Uint32Array((N - 1) * 24);

    const d     = new THREE.Vector3();
    const right = new THREE.Vector3();
    const up    = new THREE.Vector3();
    const tmp   = new THREE.Vector3();

    for (let i = 0; i < N; i++) {
        const prev = i > 0     ? i - 1 : 0;
        const next = i < N - 1 ? i + 1 : N - 1;

        d.set(
            positions[next * 3]     - positions[prev * 3],
            positions[next * 3 + 1] - positions[prev * 3 + 1],
            positions[next * 3 + 2] - positions[prev * 3 + 2]
        );
        if (d.lengthSq() < 1e-20) { d.set(1, 0, 0); }
        d.normalize();

        right.crossVectors(_Z_AXIS, d);
        if (right.lengthSq() < 1e-10) { right.crossVectors(_X_AXIS, d); }
        right.normalize();

        up.crossVectors(d, right).normalize();

        const px = positions[i * 3];
        const py = positions[i * 3 + 1];
        const pz = positions[i * 3 + 2];
        const base = i * 12;

        tmp.set(px, py, pz).addScaledVector(right, halfWidth);
        posOut[base]     = tmp.x; posOut[base + 1] = tmp.y; posOut[base + 2] = tmp.z;

        tmp.set(px, py, pz).addScaledVector(up, halfHeight);
        posOut[base + 3] = tmp.x; posOut[base + 4] = tmp.y; posOut[base + 5] = tmp.z;

        tmp.set(px, py, pz).addScaledVector(right, -halfWidth);
        posOut[base + 6] = tmp.x; posOut[base + 7] = tmp.y; posOut[base + 8] = tmp.z;

        tmp.set(px, py, pz).addScaledVector(up, -halfHeight);
        posOut[base + 9]  = tmp.x; posOut[base + 10] = tmp.y; posOut[base + 11] = tmp.z;
    }

    let idx = 0;
    for (let i = 0; i < N - 1; i++) {
        const b = i * 4;
        for (let c = 0; c < 4; c++) {
            const c1 = (c + 1) & 3;
            const bi = b + c;
            const ni = b + c1;
            const bj = b + 4 + c;
            const nj = b + 4 + c1;
            indexOut[idx++] = bi; indexOut[idx++] = ni; indexOut[idx++] = nj;
            indexOut[idx++] = bi; indexOut[idx++] = nj; indexOut[idx++] = bj;
        }
    }

    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(posOut, 3));
    geo.setIndex(new THREE.BufferAttribute(indexOut, 1));
    return geo;
}

// ---- Preview update handler ----

export interface PreviewData {
    path_lengths: number[];
    coords_b64: string;
    travel_path_lengths: number[];
    travel_coords_b64: string;
    nozzleSize?: number;
}

export function applyPreviewData(msg: PreviewData): void {
    const computingOverlay = document.getElementById('computing-overlay');
    computingOverlay?.classList.remove('visible');

    // Clear old meshes (materials are shared — do not dispose them)
    pathMeshes.forEach((mesh) => {
        pathGroup.remove(mesh);
        mesh.geometry.dispose();
    });
    pathMeshes = [];
    travelLines.forEach((line) => {
        pathGroup.remove(line);
        line.geometry.dispose();
        (line.material as THREE.Material).dispose();
    });
    travelLines = [];
    travelLineMaterials = [];
    storedLayerCoords = [];
    storedTravelCoords = [];

    const { path_lengths, coords_b64, travel_path_lengths, travel_coords_b64, nozzleSize = 0.4 } = msg;
    storedTravelPathLengths = travel_path_lengths || [];
    storedPathLengths = path_lengths;
    const allCoords = b64ToFloat32Array(coords_b64);
    const travelCoords = travel_coords_b64 ? b64ToFloat32Array(travel_coords_b64) : new Float32Array(0);

    // Build one diamond-tube Mesh per path
    let offset = 0;
    for (let pi = 0; pi < path_lengths.length; pi++) {
        const len = path_lengths[pi];
        const positions = allCoords.slice(offset * 3, (offset + len) * 3);
        const geometry = buildDiamondTube(positions, len, nozzleSize);
        const mesh = new THREE.Mesh(geometry, brightMaterial);
        pathGroup.add(mesh);
        pathMeshes.push(mesh);
        storedLayerCoords.push(positions);
        offset += len;
    }

    // Build travel lines
    let travelOffset = 0;
    for (let pi = 0; pi < path_lengths.length - 1; pi++) {
        const endCoords   = storedLayerCoords[pi];
        const startCoords = storedLayerCoords[pi + 1];
        const endLen = path_lengths[pi];
        const wayCount = (travel_path_lengths && travel_path_lengths[pi]) ? travel_path_lengths[pi] : 0;

        const pts: number[] = [
            endCoords[(endLen - 1) * 3],
            endCoords[(endLen - 1) * 3 + 1],
            endCoords[(endLen - 1) * 3 + 2],
        ];
        for (let wi = 0; wi < wayCount; wi++) {
            pts.push(
                travelCoords[(travelOffset + wi) * 3],
                travelCoords[(travelOffset + wi) * 3 + 1],
                travelCoords[(travelOffset + wi) * 3 + 2],
            );
        }
        pts.push(startCoords[0], startCoords[1], startCoords[2]);

        const ptsArray = new Float32Array(pts);
        const geo = new LineGeometry();
        geo.setPositions(pts);
        const mat = new LineMaterial({
            color: 0xffffff,
            linewidth: 2,
            opacity: 0.1,
            transparent: true,
            resolution: new THREE.Vector2(container.clientWidth, container.clientHeight),
        });
        const line = new Line2(geo, mat);
        pathGroup.add(line);
        travelLines.push(line);
        travelLineMaterials.push(mat);
        storedTravelCoords.push(ptsArray);
        travelOffset += wayCount;
    }

    // Reset sliders
    const total = path_lengths.length;
    vSlider.min   = '0';
    vSlider.max   = String(total - 1);
    vSlider.value = String(total - 1);
    totalLabel.textContent = String(total);
    vValLabel.textContent  = String(total);
    currentTopIndex = total - 1;

    const topLen = path_lengths[total - 1];
    const initTravelExtra = (storedTravelPathLengths[total - 1] ?? 0) > 0
        ? (storedTravelPathLengths[total - 1] + 1) : 0;
    hSlider.min   = '1';
    hSlider.max   = String(topLen + initTravelExtra);
    hSlider.value = String(topLen + initTravelExtra);
    hTotalLabel.textContent = String(topLen + initTravelExtra);

    pathMeshes.forEach((mesh, i) => { mesh.visible = i <= currentTopIndex; });
    travelLines.forEach((line, i) => {
        const vis = (i + 1) <= currentTopIndex;
        line.visible = vis;
        if (vis) { line.geometry.setDrawRange(0, Infinity); }
        else      { line.geometry.setDrawRange(0, 0); }
    });
    updateSliderFill(vSlider, '--v-fill', true);
    applyHorizontalSlider();
    scheduleRender();
}

export function showComputing(visible: boolean): void {
    document.getElementById('computing-overlay')?.classList.toggle('visible', visible);
}

// ---- Tauri event listener ----

listen<PreviewData>('preview-update', (event) => {
    applyPreviewData(event.payload);
}).catch(console.error);

// ---- Animation loop ----

function animate(): void {
    requestAnimationFrame(animate);
    controls.update(); // fires 'change' events during damping, keeping needsRender true
    if (needsRender) {
        renderer.render(scene, camera);
        needsRender = false;
    }
}
animate();

// ---- Resize handler ----

window.addEventListener('resize', () => {
    const w = container.clientWidth;
    const h = container.clientHeight;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
    travelLineMaterials.forEach(mat => mat.resolution.set(w, h));
    scheduleRender();
});
