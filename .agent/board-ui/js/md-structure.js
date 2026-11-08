/** Post-process rendered markdown into Meridian lanes (h2) and fields (h3). */

const LANE_SLUGS = new Set(["intent", "plan", "record", "boundaries"]);

function slug(text) {
  return String(text || "")
    .toLowerCase()
    .replace(/<[^>]+>/g, "")
    .replace(/&[a-z]+;/gi, " ")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

function wrapFieldBlock(parent, h3) {
  const field = slug(h3.textContent);
  h3.classList.add("md-field-title");
  if (field) h3.dataset.field = field;

  const block = document.createElement("div");
  block.className = "md-field";
  if (field) block.dataset.field = field;
  parent.insertBefore(block, h3);
  block.appendChild(h3);

  let sib = block.nextSibling;
  while (sib && sib.tagName !== "H3" && sib.tagName !== "H2") {
    const move = sib;
    sib = sib.nextSibling;
    block.appendChild(move);
  }
}

function wrapFieldsIn(parent) {
  const h3s = [...parent.querySelectorAll(":scope > h3")];
  h3s.forEach((h3) => wrapFieldBlock(parent, h3));
}

function wrapPreamble(doc) {
  const kids = [...doc.children];
  const firstH2 = kids.findIndex((n) => n.tagName === "H2");
  if (firstH2 <= 0) return;

  const pre = document.createElement("div");
  pre.className = "md-preamble";
  for (let i = 0; i < firstH2; i++) {
    const node = kids[i];
    if (node.classList?.contains("meta-grid")) continue;
    pre.appendChild(node);
  }
  if (!pre.childElementCount) return;
  doc.insertBefore(pre, doc.querySelector(":scope > h2"));
}

function wrapLanes(doc) {
  const h2s = [...doc.querySelectorAll(":scope > h2")];
  h2s.forEach((h2) => {
    const lane = slug(h2.textContent);
    h2.classList.add("md-lane-title");
    if (lane) h2.dataset.lane = lane;

    const section = document.createElement("section");
    section.className = "md-lane";
    section.dataset.lane = LANE_SLUGS.has(lane) ? lane : lane || "section";

    doc.insertBefore(section, h2);
    section.appendChild(h2);

    let sib = section.nextSibling;
    while (sib && sib.tagName !== "H2") {
      const move = sib;
      sib = sib.nextSibling;
      section.appendChild(move);
    }

    wrapFieldsIn(section);
  });
}

export function enrichMarkdownStructure(root) {
  const doc = root?.classList?.contains("md-doc") ? root : root?.querySelector?.(".md-doc");
  if (!doc) return;

  wrapPreamble(doc);
  wrapLanes(doc);
  wrapFieldsIn(doc);
}
