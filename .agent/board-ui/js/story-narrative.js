/** Compact As / I want / so that for board cards (no H1, no markdown). */
export function compactStoryNarrative(preamble) {
  if (!preamble?.trim()) return null;
  let text = preamble.trim();
  text = text.replace(/^#\s+US-\d{4}\s*[—-]\s*.+\n?/i, "");
  text = text.replace(/\*\*/g, "");
  text = text.replace(/\s+/g, " ").trim();
  if (!text) return null;
  if (text.length > 140) return `${text.slice(0, 137)}…`;
  return text;
}
