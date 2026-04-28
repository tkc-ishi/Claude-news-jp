// Claude Updates JP - フロントエンド (改修版)
// data.json を読み込み、両言語タイトル + フィルタ + 検索 を実装

const state = {
  items: [],
  categories: [],
  activeCategory: "all",
  query: "",
};

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

function fmtDate(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  if (isNaN(d)) return "";
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}.${m}.${day}`;
}

function escapeHtml(s) {
  return (s ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

// 検索クエリでハイライト (大文字小文字無視・日本語OK)
function highlight(text, query) {
  const safe = escapeHtml(text);
  if (!query) return safe;
  const q = query.trim();
  if (!q) return safe;
  // 正規表現メタ文字をエスケープ
  const re = new RegExp(q.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "gi");
  return safe.replace(re, (m) => `<mark>${m}</mark>`);
}

function matchesQuery(it, query) {
  if (!query) return true;
  const q = query.toLowerCase();
  const ja = (it.title_ja || "").toLowerCase();
  const en = (it.title_en || "").toLowerCase();
  return ja.includes(q) || en.includes(q);
}

function render() {
  const feed = $("#feed");
  const empty = $("#empty");
  feed.innerHTML = "";

  const filtered = state.items.filter((it) => {
    const inCat = state.activeCategory === "all" || it.category === state.activeCategory;
    return inCat && matchesQuery(it, state.query);
  });

  if (filtered.length === 0) {
    empty.hidden = false;
    return;
  }
  empty.hidden = true;

  const frag = document.createDocumentFragment();

  for (const it of filtered) {
    const li = document.createElement("li");
    li.className = "card";

    li.innerHTML = `
      <div class="card-head">
        <span class="source-badge" style="background:${escapeHtml(it.color)}">
          ${escapeHtml(it.source_name)}
        </span>
        <span class="date">${fmtDate(it.published)}</span>
      </div>
      <h2 class="title-ja">${highlight(it.title_ja || it.title_en, state.query)}</h2>
      <p class="title-en">${highlight(it.title_en, state.query)}</p>
      <div class="cta-row">
        <a class="cta" href="${escapeHtml(it.link)}" target="_blank" rel="noopener">
          公式記事を読む
        </a>
      </div>
    `;
    frag.appendChild(li);
  }
  feed.appendChild(frag);
}

function buildFilters() {
  const wrap = $("#filters");
  // カテゴリと色を抽出
  const seen = new Map();
  for (const it of state.items) {
    if (!seen.has(it.category)) seen.set(it.category, it.color);
  }
  state.categories = Array.from(seen.entries()).map(([category, color]) => ({ category, color }));

  for (const c of state.categories) {
    const b = document.createElement("button");
    b.className = "chip";
    b.dataset.filter = c.category;
    b.textContent = c.category;
    b.style.borderColor = c.color;
    wrap.appendChild(b);
  }

  wrap.addEventListener("click", (e) => {
    const t = e.target.closest("button.chip");
    if (!t) return;
    state.activeCategory = t.dataset.filter;
    $$(".chip").forEach((el) => el.classList.toggle("active", el === t));
    render();
  });
}

function bindSearch() {
  const input = $("#search");
  let timer;
  input.addEventListener("input", () => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      state.query = input.value;
      render();
    }, 120);
  });
}

async function init() {
  try {
    const res = await fetch("./data.json", { cache: "no-cache" });
    const data = await res.json();
    state.items = data.items || [];
    $("#updated-at").textContent = `最終更新 ${fmtDate(data.updated_at)}`;
    $("#item-count").textContent = `${data.items.length}件`;
  } catch (e) {
    $("#updated-at").textContent = "データを読み込めませんでした";
    return;
  }
  buildFilters();
  bindSearch();
  render();
}

init();
