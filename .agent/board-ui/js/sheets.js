export function setSheetOpen(sheetId, open, openBtnId) {
  const sheet = document.getElementById(sheetId);
  if (!sheet) return;
  sheet.hidden = !open;
  sheet.setAttribute("aria-hidden", open ? "false" : "true");
  if (openBtnId) {
    const btn = document.getElementById(openBtnId);
    btn?.classList.toggle("on", open);
    btn?.setAttribute("aria-expanded", open ? "true" : "false");
  }
}

export function isSheetOpen(sheetId) {
  const sheet = document.getElementById(sheetId);
  return Boolean(sheet && !sheet.hidden);
}

export function closeTopSheet() {
  if (isSheetOpen("detail-sheet")) {
    setSheetOpen("detail-sheet", false);
    return true;
  }
  if (isSheetOpen("filter-sheet")) {
    setSheetOpen("filter-sheet", false, "open-filters");
    return true;
  }
  return false;
}
