import { enrichMarkdownStructure } from "./md-structure.js";

function stripFrontmatter(raw) {
  if (!raw.startsWith("---")) return { meta: "", body: raw };
  const end = raw.indexOf("\n---", 3);
  if (end === -1) return { meta: "", body: raw };
  const meta = raw.slice(0, end + 4);
  const body = raw.slice(end + 4).replace(/^\s+/, "");
  return { meta, body };
}

function escape(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function frontmatterGrid(meta) {
  const inner = meta.replace(/^---\s*/, "").replace(/\s*---\s*$/, "");
  const rows = inner
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => {
      const i = line.indexOf(":");
      if (i === -1) return "";
      return `<dt>${escape(line.slice(0, i).trim())}</dt><dd>${escape(line.slice(i + 1).trim())}</dd>`;
    })
    .join("");
  return rows ? `<dl class="meta-grid">${rows}</dl>` : "";
}

export function renderMarkdown(target, raw) {
  const { meta, body } = stripFrontmatter(raw || "");
  const marked = window.marked;
  const purify = window.DOMPurify;
  let html;
  if (marked && purify) {
    const parsed = marked.parse(body, { gfm: true, breaks: false });
    html = purify.sanitize(parsed, { USE_PROFILES: { html: true } });
  } else {
    html = `<pre>${escape(body)}</pre>`;
  }
  target.innerHTML = `<article class="md-doc">${frontmatterGrid(meta)}${html}</article>`;
  enrichMarkdownStructure(target);
  target.querySelectorAll("table").forEach((table) => {
    const wrap = document.createElement("div");
    wrap.className = "table-wrap";
    table.parentNode.insertBefore(wrap, table);
    wrap.appendChild(table);
  });
  renderMermaid(target);
}

function renderMermaid(root) {
  const mermaid = window.mermaid;
  root.querySelectorAll("pre code.language-mermaid, pre code.mermaid").forEach((code) => {
    const wrap = document.createElement("div");
    wrap.className = "md-mermaid";
    wrap.textContent = code.textContent || "";
    const pre = code.closest("pre");
    pre?.replaceWith(wrap);
  });
  const nodes = root.querySelectorAll(".md-mermaid");
  if (!nodes.length || !mermaid) return;
  mermaid
    .run({ nodes })
    .catch(() => {
      nodes.forEach((node) => {
        const pre = document.createElement("pre");
        pre.textContent = node.textContent || "";
        node.replaceWith(pre);
      });
    });
}
