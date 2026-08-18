import { readFileSync, writeFileSync, mkdirSync, readdirSync, cpSync, rmSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { marked } from "marked";

const __dirname = dirname(fileURLToPath(import.meta.url));
const BASE = process.env.SITE_BASE ?? "/medicine-packaging-merged/";
const postsDir = join(__dirname, "posts");
const publicDir = join(__dirname, "public");
const distDir = join(__dirname, "dist");

marked.use({ gfm: true, breaks: false });

function parseFrontmatter(raw, file) {
  const m = raw.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!m) throw new Error(`missing frontmatter: ${file}`);
  const fm = {};
  for (const line of m[1].split("\n")) {
    const i = line.indexOf(":");
    if (i === -1) continue;
    const k = line.slice(0, i).trim();
    let v = line.slice(i + 1).trim();
    if (
      (v.startsWith('"') && v.endsWith('"')) ||
      (v.startsWith("'") && v.endsWith("'"))
    ) {
      v = v.slice(1, -1);
    }
    fm[k] = k === "order" ? Number(v) : v;
  }
  for (const need of ["title", "date", "dek", "order"]) {
    if (fm[need] === undefined || fm[need] === "") {
      throw new Error(`${file}: missing ${need}`);
    }
  }
  return { ...fm, body: m[2] };
}

function rewriteAssets(html) {
  return html.replace(
    /(src|href)="(?:\.\.\/|\.\/|\/)(eval|charts|assets)\//g,
    `$1="${BASE}$2/`
  );
}

function keepMermaid(html) {
  return html.replace(
    /<pre><code class="language-mermaid">([\s\S]*?)<\/code><\/pre>/g,
    "<pre class=\"mermaid\">$1</pre>"
  );
}

function wrapFigures(html) {
  return html.replace(
    /<p><img([^>]*)><\/p>(?:\s*<p><em>([\s\S]*?)<\/em><\/p>)?/g,
    (_, attrs, cap) => {
      const caption = cap ? `<figcaption>${cap}</figcaption>` : "";
      return `<figure><img${attrs}>${caption}</figure>`;
    }
  );
}

function esc(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function formatDate(iso) {
  const [y, mo, d] = iso.split("-");
  return `${y}년 ${Number(mo)}월 ${Number(d)}일`;
}

function layout({ title, dek, date, bodyHtml, slug, prev, next, isHome }) {
  const pageTitle = isHome ? "약 상자 — 의약품 포장 객체감지" : `${title} — 약 상자`;
  const desc = dek || "의약품 포장 객체감지 데이터셋을 합치고 접어 학습한 기록.";
  const canonical = isHome ? BASE : `${BASE}posts/${slug}/`;
  const navPrev = prev
    ? `<a class="pn-link" href="${BASE}posts/${prev.slug}/"><span class="pn-dir">이전</span><span class="pn-title">${esc(prev.title)}</span></a>`
    : `<span class="pn-link is-empty"></span>`;
  const navNext = next
    ? `<a class="pn-link pn-next" href="${BASE}posts/${next.slug}/"><span class="pn-dir">다음</span><span class="pn-title">${esc(next.title)}</span></a>`
    : `<span class="pn-link is-empty"></span>`;
  const articleHead = isHome
    ? ""
    : `<header class="post-head">
        <p class="dateline">${formatDate(date)}</p>
        <h1>${esc(title)}</h1>
        <p class="dek">${esc(dek)}</p>
      </header>`;
  const pager = isHome
    ? ""
    : `<nav class="pager" aria-label="글 이동">${navPrev}${navNext}</nav>`;

  return `<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${esc(pageTitle)}</title>
  <meta name="description" content="${esc(desc)}">
  <link rel="canonical" href="https://jae-hun-cho.github.io${canonical}">
  <link rel="stylesheet" href="${BASE}assets/site.css">
  <link rel="icon" href="${BASE}assets/favicon.svg" type="image/svg+xml">
</head>
<body>
  <a class="skip" href="#main">본문으로</a>
  <header class="mast">
    <div class="wrap">
      <p class="mast-kicker"><a href="${BASE}">medicine-packaging-merged</a></p>
      <p class="mast-title"><a href="${BASE}">약 상자</a></p>
      <p class="mast-sub">상자 · 블리스터 · 병 — 포장 객체감지 노트</p>
    </div>
  </header>
  <main id="main" class="wrap">
    ${articleHead}
    <div class="article">${bodyHtml}</div>
    ${pager}
  </main>
  <footer class="colophon">
    <div class="wrap">
      <p>숫자는 레포 <code>docs/</code> · <code>data/</code> · <code>versions/</code>와 같습니다. 지어내지 않았습니다.</p>
      <p><a href="https://app.roboflow.com/toyproject1/medicine-packaging-merged-v2">Roboflow 프로젝트</a>
      · <a href="https://github.com/jae-hun-cho/medicine-packaging-merged">GitHub</a>
      · 라이선스는 이미지별 원본이 우선</p>
    </div>
  </footer>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
  <script src="${BASE}assets/diagrams.js"></script>
</body>
</html>
`;
}

function homeHtml(posts) {
  const items = posts
    .map(
      (p) => `<li>
      <a href="${BASE}posts/${p.slug}/">
        <time datetime="${p.date}">${formatDate(p.date)}</time>
        <span class="home-title">${esc(p.title)}</span>
        <span class="home-dek">${esc(p.dek)}</span>
      </a>
    </li>`
    )
    .join("\n");
  const body = `
    <header class="home-head">
      <h1>포장을 본다</h1>
      <p>상업용으로 쓸 수 있는 의약품 <em>포장</em> 객체감지 데이터셋 14개를 합치고, 758개 클래스 이름을 75개 중분류로 접어 RF-DETR Medium을 학습한 기록입니다. 알약이 아니라 상자·블리스터·병입니다.</p>
      <p>원본 28,297장, 758 클래스, 51,520 박스. 학습 버전 v3는 28,119장 · 75 클래스 · 22,715 / 2,983 / 2,421. 테스트 mAP50 83.8, mAP50-95 69.0, precision 84.9, recall 79.5.</p>
    </header>
    <section class="gallery-block" aria-label="그림">
      <h2>그림</h2>
      <div class="gallery">
        <figure>
          <a href="${BASE}posts/sources/"><img src="${BASE}charts/chart-sources.png" alt="소스 14개의 이미지 수"></a>
          <figcaption>소스 14개 장수. 합 28,297.</figcaption>
        </figure>
        <figure>
          <a href="${BASE}posts/taxonomy/"><img src="${BASE}charts/chart-majors.png" alt="대분류 14개의 인스턴스 수"></a>
          <figcaption>대분류 14개 박스. 합 49,242.</figcaption>
        </figure>
        <figure>
          <a href="${BASE}posts/eval/"><img src="${BASE}charts/chart-eval-f1.png" alt="재확인한 클래스의 F1과 mAP50"></a>
          <figcaption>재확인한 클래스 F1 · mAP50. 75개 전체가 아님.</figcaption>
        </figure>
        <figure>
          <a href="${BASE}posts/eval/"><img src="${BASE}eval/sitagliptin.jpg" alt="Januvia 상자, sitagliptin phosphate 100 mg"></a>
          <figcaption>Sitagliptin — Januvia 100 mg</figcaption>
        </figure>
        <figure>
          <a href="${BASE}posts/eval/"><img src="${BASE}eval/tylol-hot.jpg" alt="TYLOLHOT 상자"></a>
          <figcaption>TYLOLHOT — 종합감기인데 Paracetamol계</figcaption>
        </figure>
        <figure>
          <a href="${BASE}posts/eval/"><img src="${BASE}eval/i20.jpg" alt="Asthalin-4 블리스터 앞뒤"></a>
          <figcaption>은박 블리스터 — Asthalin-4</figcaption>
        </figure>
        <figure>
          <a href="${BASE}posts/eval/"><img src="${BASE}eval/paracetamol26.jpg" alt="PARACIP-650 블리스터"></a>
          <figcaption>Paracetamol계 — PARACIP-650</figcaption>
        </figure>
      </div>
    </section>
    <ol class="home-list">
      ${items}
    </ol>
  `;
  return layout({
    title: "약 상자",
    dek: "의약품 포장 객체감지 데이터셋을 합치고 접어 학습한 기록.",
    date: posts[0]?.date ?? "2026-08-14",
    bodyHtml: body,
    slug: "",
    isHome: true,
  });
}

function loadPosts() {
  const files = readdirSync(postsDir)
    .filter((f) => f.endsWith(".md"))
    .sort();
  if (files.length === 0) throw new Error("no posts in site/posts");
  return files
    .map((file) => {
      const raw = readFileSync(join(postsDir, file), "utf8");
      const fm = parseFrontmatter(raw, file);
      const slug = file.replace(/\.md$/, "");
      const html = wrapFigures(keepMermaid(rewriteAssets(marked.parse(fm.body))))
        .replace(/<table>/g, "<div class=\"table-wrap\"><table>")
        .replace(/<\/table>/g, "</table></div>");
      return { ...fm, slug, html, file };
    })
    .sort((a, b) => a.order - b.order || a.date.localeCompare(b.date));
}

function build() {
  if (existsSync(distDir)) rmSync(distDir, { recursive: true, force: true });
  mkdirSync(distDir, { recursive: true });
  if (existsSync(publicDir)) {
    cpSync(publicDir, distDir, { recursive: true });
  }

  const posts = loadPosts();
  writeFileSync(join(distDir, "index.html"), homeHtml(posts), "utf8");

  for (let i = 0; i < posts.length; i++) {
    const post = posts[i];
    const prev = i > 0 ? posts[i - 1] : null;
    const next = i < posts.length - 1 ? posts[i + 1] : null;
    const dir = join(distDir, "posts", post.slug);
    mkdirSync(dir, { recursive: true });
    writeFileSync(
      join(dir, "index.html"),
      layout({
        title: post.title,
        dek: post.dek,
        date: post.date,
        bodyHtml: post.html,
        slug: post.slug,
        prev,
        next,
        isHome: false,
      }),
      "utf8"
    );
  }

  console.log(`base ${BASE}`);
  console.log(`wrote ${posts.length} posts + index → ${distDir}`);
  for (const p of posts) console.log(`  ${p.order}  ${p.slug}  ${p.title}`);
}

build();
