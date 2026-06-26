/// <reference types="vite/client" />
import * as monaco from 'monaco-editor';
import editorWorker from 'monaco-editor/esm/vs/editor/editor.worker?worker';
import { invoke } from '@tauri-apps/api/core';

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

// ---- Completion types ----

interface CompletionItem {
  name: string;
  kind: 'function' | 'class' | 'value';
  signature: string | null;
  doc: string | null;
  members?: CompletionItem[];
}

interface CompletionData {
  gc?: CompletionItem[];
  np?: CompletionItem[];
}

// ---- Dynamic completions ----

function kindToMonaco(kind: string): monaco.languages.CompletionItemKind {
  switch (kind) {
    case 'class': return monaco.languages.CompletionItemKind.Class;
    case 'function': return monaco.languages.CompletionItemKind.Function;
    default: return monaco.languages.CompletionItemKind.Property;
  }
}

function buildInsertText(item: CompletionItem): { text: string; format: monaco.languages.CompletionItemInsertTextRule } {
  if (!item.signature || item.kind === 'class' && !item.members) {
    // Class with no callable context — just insert name
    return { text: item.name, format: monaco.languages.CompletionItemInsertTextRule.None };
  }

  if (item.kind === 'class') {
    // A class used as a namespace (e.g. gc.Transform) — insert just the name
    return { text: item.name, format: monaco.languages.CompletionItemInsertTextRule.None };
  }

  // Parse signature to build snippet
  try {
    const inner = item.signature.replace(/^\(/, '').replace(/\).*$/, '');
    if (!inner.trim()) {
      return { text: `${item.name}()$0`, format: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet };
    }
    const params = inner.split(',').map(p => p.trim());
    const snippetParams = params
      .filter(p => p !== 'self')
      .map((p, i) => {
        const name = p.split('=')[0].split(':')[0].trim().replace(/^\*+/, '');
        return `\${${i + 1}:${name}}`;
      });
    return {
      text: `${item.name}(${snippetParams.join(', ')})$0`,
      format: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
    };
  } catch {
    return { text: item.name, format: monaco.languages.CompletionItemInsertTextRule.None };
  }
}

function buildSuggestions(
  items: CompletionItem[],
  model: monaco.editor.ITextModel,
  position: monaco.Position,
): monaco.languages.CompletionItem[] {
  const word = model.getWordUntilPosition(position);
  const range: monaco.IRange = {
    startLineNumber: position.lineNumber,
    endLineNumber: position.lineNumber,
    startColumn: word.startColumn,
    endColumn: word.endColumn,
  };

  return items.map((item): monaco.languages.CompletionItem => {
    const { text, format } = buildInsertText(item);
    const label = item.signature ? `${item.name}${item.signature}` : item.name;
    return {
      label,
      kind: kindToMonaco(item.kind),
      insertText: text,
      insertTextRules: format,
      documentation: item.doc
        ? { value: `\`\`\`python\n${item.name}${item.signature ?? ''}\n\`\`\`\n\n${item.doc}` }
        : undefined,
      range,
    };
  });
}

async function registerDynamicCompletions(): Promise<void> {
  let data: CompletionData;
  try {
    data = await invoke<CompletionData>('get_completion_data');
  } catch (e) {
    console.warn('Could not load completion data:', e);
    return;
  }

  monaco.languages.registerCompletionItemProvider('python', {
    triggerCharacters: ['.'],
    provideCompletionItems(model, position) {
      const lineText = model.getLineContent(position.lineNumber);
      const textBefore = lineText.substring(0, position.column - 1);

      // gc.ClassName. → show members of that class
      const nestedMatch = textBefore.match(/\bgc\.(\w+)\.$/);
      if (nestedMatch && data.gc) {
        const className = nestedMatch[1];
        const gcClass = data.gc.find(i => i.name === className);
        if (gcClass?.members?.length) {
          return { suggestions: buildSuggestions(gcClass.members, model, position) };
        }
        return { suggestions: [] };
      }

      // gc. → show gcoordinator top-level
      if (/\bgc\.$/.test(textBefore) && data.gc) {
        return { suggestions: buildSuggestions(data.gc, model, position) };
      }

      // np. → show numpy top-level
      if (/\bnp\.$/.test(textBefore) && data.np) {
        return { suggestions: buildSuggestions(data.np, model, position) };
      }

      return { suggestions: [] };
    },
  });
}

// ---- Editor init ----

export function initEditor(containerId: string): void {
  const container = document.getElementById(containerId) as HTMLElement;

  monaco.editor.defineTheme('gc-dark', {
    base: 'vs-dark',
    inherit: true,
    rules: [
      { token: 'keyword',         foreground: 'C586C0', fontStyle: 'bold' },
      { token: 'keyword.control', foreground: 'C586C0', fontStyle: 'bold' },
      { token: 'string',          foreground: 'CE9178' },
      { token: 'string.escape',   foreground: 'D7BA7D' },
      { token: 'comment',         foreground: '6A9955', fontStyle: 'italic' },
      { token: 'number',          foreground: 'B5CEA8' },
      { token: 'type.identifier', foreground: '4EC9B0' },
      { token: 'delimiter',       foreground: 'D4D4D4' },
      { token: 'operator',        foreground: 'D4D4D4' },
      { token: 'identifier',      foreground: '9CDCFE' },
    ],
    colors: {
      'editor.background':              '#1e1e1e',
      'editor.foreground':              '#D4D4D4',
      'editorLineNumber.foreground':    '#858585',
      'editor.lineHighlightBackground': '#2A2A2A',
      'editorCursor.foreground':        '#AEAFAD',
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
    suggestOnTriggerCharacters: true,
    quickSuggestions: { other: true, comments: false, strings: false },
    parameterHints: { enabled: true },
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

  registerDynamicCompletions().catch(console.error);
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
