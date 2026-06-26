let output: HTMLElement | null = null;

export function initConsole(elementId: string): void {
  output = document.getElementById(elementId);
}

export function consoleClear(): void {
  if (output) output.textContent = '';
}

export function consoleLog(text: string): void {
  if (!output) return;
  const span = document.createElement('span');
  span.textContent = text + '\n';
  output.appendChild(span);
  output.scrollTop = output.scrollHeight;
}

export function consoleError(text: string): void {
  if (!output) return;
  const span = document.createElement('span');
  span.className = 'error';
  span.textContent = text + '\n';
  output.appendChild(span);
  output.scrollTop = output.scrollHeight;
}
