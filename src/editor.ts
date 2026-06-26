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

  // Override Python tokenizer to classify function/method calls separately from plain identifiers.
  // Lookahead (?=\s*\() detects calls; uppercase-starting names without () become type.identifier.
  monaco.languages.setMonarchTokensProvider('python', {
    defaultToken: '',
    tokenPostfix: '.python',
    keywords: [
      'False', 'None', 'True', '_', 'and', 'as', 'assert', 'async', 'await',
      'break', 'case', 'class', 'continue', 'def', 'del', 'elif', 'else',
      'except', 'exec', 'finally', 'for', 'from', 'global', 'if', 'import',
      'in', 'is', 'lambda', 'match', 'nonlocal', 'not', 'or', 'pass', 'print',
      'raise', 'return', 'try', 'type', 'while', 'with', 'yield',
      'int', 'float', 'long', 'complex', 'hex', 'abs', 'all', 'any', 'apply',
      'basestring', 'bin', 'bool', 'buffer', 'bytearray', 'callable', 'chr',
      'classmethod', 'cmp', 'coerce', 'compile', 'delattr', 'dict', 'dir',
      'divmod', 'enumerate', 'eval', 'execfile', 'file', 'filter', 'format',
      'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'id',
      'input', 'intern', 'isinstance', 'issubclass', 'iter', 'len', 'locals',
      'list', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct',
      'open', 'ord', 'pow', 'property', 'reversed', 'range', 'raw_input',
      'reduce', 'reload', 'repr', 'round', 'self', 'set', 'setattr', 'slice',
      'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'unichr',
      'unicode', 'vars', 'xrange', 'zip',
      '__dict__', '__methods__', '__members__', '__class__', '__bases__',
      '__name__', '__mro__', '__subclasses__', '__init__', '__import__',
    ],
    brackets: [
      { open: '{', close: '}', token: 'delimiter.curly' },
      { open: '[', close: ']', token: 'delimiter.bracket' },
      { open: '(', close: ')', token: 'delimiter.parenthesis' },
    ],
    tokenizer: {
      root: [
        { include: '@whitespace' },
        { include: '@numbers' },
        { include: '@strings' },
        [/[,:;]/, 'delimiter'],
        [/[{}\[\]()]/, '@brackets'],
        [/@[a-zA-Z_]\w*/, 'tag'],
        // function/method calls — lookahead for opening paren
        [/[a-zA-Z_]\w*(?=\s*\()/, { cases: { '@keywords': 'keyword', '@default': 'entity.name.function' } }],
        // ALL_CAPS identifiers — Python constant convention (no lowercase letters in the name)
        [/[A-Z][A-Z0-9_]*\b/, { cases: { '@keywords': 'keyword', '@default': 'constant' } }],
        // class-like names (PascalCase — uppercase start, has lowercase chars)
        [/[A-Z]\w*/, { cases: { '@keywords': 'keyword', '@default': 'type.identifier' } }],
        // general identifiers
        [/[a-zA-Z_]\w*/, { cases: { '@keywords': 'keyword', '@default': 'identifier' } }],
      ],
      whitespace: [
        [/\s+/, 'white'],
        [/(^#.*$)/, 'comment'],
        [/'''/, 'string', '@endDocString'],
        [/"""/, 'string', '@endDblDocString'],
      ],
      endDocString: [
        [/[^']+/, 'string'],
        [/\\'/, 'string'],
        [/'''/, 'string', '@popall'],
        [/'/, 'string'],
      ],
      endDblDocString: [
        [/[^"]+/, 'string'],
        [/\\"/, 'string'],
        [/"""/, 'string', '@popall'],
        [/"/, 'string'],
      ],
      numbers: [
        [/-?0x([abcdef]|[ABCDEF]|\d)+[lL]?/, 'number.hex'],
        [/-?(\d*\.)?\d+([eE][+\-]?\d+)?[jJ]?[lL]?/, 'number'],
      ],
      strings: [
        [/'$/, 'string.escape', '@popall'],
        [/f'{1,3}/, 'string.escape', '@fStringBody'],
        [/'/, 'string.escape', '@stringBody'],
        [/"$/, 'string.escape', '@popall'],
        [/f"{1,3}/, 'string.escape', '@fDblStringBody'],
        [/"/, 'string.escape', '@dblStringBody'],
      ],
      fStringBody: [
        [/[^\\'\{\}]+$/, 'string', '@popall'],
        [/[^\\'\{\}]+/, 'string'],
        [/\{[^\}':!=]+/, 'identifier', '@fStringDetail'],
        [/\\./, 'string'],
        [/'/, 'string.escape', '@popall'],
        [/\\$/, 'string'],
      ],
      stringBody: [
        [/[^\\']+$/, 'string', '@popall'],
        [/[^\\']+/, 'string'],
        [/\\./, 'string'],
        [/'/, 'string.escape', '@popall'],
        [/\\$/, 'string'],
      ],
      fDblStringBody: [
        [/[^\\"\{\}]+$/, 'string', '@popall'],
        [/[^\\"\{\}]+/, 'string'],
        [/\{[^\}':!=]+/, 'identifier', '@fStringDetail'],
        [/\\./, 'string'],
        [/"/, 'string.escape', '@popall'],
        [/\\$/, 'string'],
      ],
      dblStringBody: [
        [/[^\\"]+$/, 'string', '@popall'],
        [/[^\\"]+/, 'string'],
        [/\\./, 'string'],
        [/"/, 'string.escape', '@popall'],
        [/\\$/, 'string'],
      ],
      fStringDetail: [
        [/[:][^}]+/, 'string'],
        [/[!][ars]/, 'string'],
        [/=/, 'string'],
        [/\}/, 'identifier', '@pop'],
      ],
    },
  } as monaco.languages.IMonarchLanguage);

  monaco.editor.defineTheme('gc-dark', {
    base: 'vs-dark',
    inherit: true,
    rules: [
      { token: 'keyword',              foreground: 'C586C0', fontStyle: 'bold' },
      { token: 'keyword.control',      foreground: 'C586C0', fontStyle: 'bold' },
      { token: 'entity.name.function', foreground: 'DCDCAA' },
      { token: 'constant',             foreground: '569CD6' },
      { token: 'type.identifier',      foreground: '4EC9B0' },
      { token: 'identifier',           foreground: '9CDCFE' },
      { token: 'string',               foreground: 'CE9178' },
      { token: 'string.escape',        foreground: 'CE9178' },
      { token: 'comment',              foreground: '6A9955', fontStyle: 'italic' },
      { token: 'number',               foreground: 'B5CEA8' },
      { token: 'delimiter',            foreground: 'D4D4D4' },
      { token: 'operator',             foreground: 'D4D4D4' },
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
