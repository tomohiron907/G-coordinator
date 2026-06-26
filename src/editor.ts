/// <reference types="vite/client" />
import * as monaco from 'monaco-editor';
import editorWorker from 'monaco-editor/esm/vs/editor/editor.worker?worker';

self.MonacoEnvironment = {
  getWorker(_: unknown, _label: string) {
    return new editorWorker();
  },
};

const DEFAULT_CODE = `# Documentation:
# English:  https://gcoordinator.readthedocs.io/en/latest/
# Japanese: https://gcoordinator.readthedocs.io/ja/latest/

import gcoordinator as gc


gc.gui_export()
`;

let editor: monaco.editor.IStandaloneCodeEditor | null = null;
let currentFilePath: string | null = null;
let isModifiedState = false;
let suppressNextChange = false;

export function initEditor(containerId: string): void {
  const container = document.getElementById(containerId) as HTMLElement;

  monaco.editor.defineTheme('gc-dark', {
    base: 'vs-dark',
    inherit: true,
    rules: [],
    colors: {
      'editor.background': '#1e1e1e',
    },
  });

  editor = monaco.editor.create(container, {
    value: DEFAULT_CODE,
    language: 'python',
    theme: 'gc-dark',
    fontSize: 13,
    fontFamily: "'Fira Code', 'Consolas', 'Courier New', monospace",
    fontLigatures: true,
    minimap: { enabled: false },
    scrollBeyondLastLine: false,
    renderLineHighlight: 'line',
    automaticLayout: true,
    tabSize: 4,
    insertSpaces: true,
    wordWrap: 'off',
    lineNumbers: 'on',
  });

  editor.onDidChangeModelContent(() => {
    if (suppressNextChange) {
      suppressNextChange = false;
      return;
    }
    if (!isModifiedState) {
      isModifiedState = true;
      window.dispatchEvent(new CustomEvent('editor-dirty'));
    }
  });

  editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => {
    document.getElementById('run-btn')?.click();
  });

  editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, () => {
    window.dispatchEvent(new CustomEvent('request-save'));
  });

  editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.KeyS, () => {
    window.dispatchEvent(new CustomEvent('request-save-as'));
  });
}

export function getCode(): string {
  return editor?.getValue() ?? '';
}

export function setCode(code: string): void {
  suppressNextChange = true;
  editor?.setValue(code);
}

export function getCurrentFilePath(): string | null {
  return currentFilePath;
}

export function setCurrentFilePath(path: string | null): void {
  currentFilePath = path;
}

export function isModified(): boolean {
  return isModifiedState;
}

export function markSaved(): void {
  isModifiedState = false;
}
