from PIL import Image, ImageOps
from pathlib import Path
import json

# ============================================================
# 老仓库 HAN913.github.io 专用图片优化脚本
# 作用：
# 1. 从 images/ 读取原图
# 2. 生成手机端更快的缩略图 photos_v2/thumb
# 3. 生成点击预览用的大图 photos_v2/large
# 4. 生成首页封面 photos_v2/cover
# 5. 自动重建 index.html：默认只加载前 24 张，点击“加载更多”再继续加载
# ============================================================

src_dir = Path("images")
thumb_dir = Path("photos_v2/thumb")
large_dir = Path("photos_v2/large")
cover_dir = Path("photos_v2/cover")

thumb_dir.mkdir(parents=True, exist_ok=True)
large_dir.mkdir(parents=True, exist_ok=True)
cover_dir.mkdir(parents=True, exist_ok=True)

# ===== 参数配置：手机端速度主要看这里 =====
THUMB_MAX_SIZE = (480, 480)       # 相册缩略图，手机端加载快
THUMB_QUALITY = 70

LARGE_MAX_SIZE = (1500, 1500)     # 点击预览图，不用 2200 那么大
LARGE_QUALITY = 82

COVER_PC_SIZE = (1600, 900)
COVER_MOBILE_SIZE = (760, 1050)
COVER_QUALITY = 76

INITIAL_COUNT = 24                # 首次只渲染前 24 张
LOAD_MORE_COUNT = 18              # 每次点击继续加载 18 张

# ===== 如果某些竖图方向还是不对，在这里手动加文件名 =====
FORCE_ROTATE_90 = set()
FORCE_ROTATE_NEG90 = set()
FORCE_ROTATE_180 = set()

valid_suffix = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG", ".webp", ".WEBP"}

image_files = sorted(
    [p for p in src_dir.iterdir() if p.suffix in valid_suffix],
    key=lambda p: p.name
)

if not image_files:
    print("images 文件夹中没有找到图片")
    raise SystemExit(1)

print(f"共找到 {len(image_files)} 张图片，开始处理...\n")

def load_fixed_image(path: Path) -> Image.Image:
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)

    if path.name in FORCE_ROTATE_90:
        img = img.rotate(90, expand=True)
    if path.name in FORCE_ROTATE_NEG90:
        img = img.rotate(-90, expand=True)
    if path.name in FORCE_ROTATE_180:
        img = img.rotate(180, expand=True)

    return img.convert("RGB")

def save_webp(img: Image.Image, output_path: Path, max_size, quality: int):
    out = img.copy()
    out.thumbnail(max_size, Image.Resampling.LANCZOS)
    out.save(
        output_path,
        "WEBP",
        quality=quality,
        method=6,
        optimize=True
    )

gallery_items = []

for idx, img_path in enumerate(image_files, start=1):
    name = img_path.stem
    img = load_fixed_image(img_path)

    w, h = img.size
    orientation = "portrait" if h > w * 1.12 else "landscape" if w > h * 1.12 else "square"

    thumb_path = thumb_dir / f"{name}_thumb.webp"
    large_path = large_dir / f"{name}_large.webp"

    save_webp(img, large_path, LARGE_MAX_SIZE, LARGE_QUALITY)
    save_webp(img, thumb_path, THUMB_MAX_SIZE, THUMB_QUALITY)

    gallery_items.append({
        "title": f"毕业照{idx}",
        "thumb": f"photos_v2/thumb/{name}_thumb.webp",
        "preview": f"photos_v2/large/{name}_large.webp",
        "original": f"images/{img_path.name}",
        "orientation": orientation,
        "w": w,
        "h": h
    })

    print(f"处理完成：{img_path.name}  {w}x{h}  {orientation}")

# ===== 生成封面图：不用 large 当首屏背景，手机端会快很多 =====
cover_src = load_fixed_image(image_files[0])

cover_pc = ImageOps.fit(
    cover_src,
    COVER_PC_SIZE,
    method=Image.Resampling.LANCZOS,
    centering=(0.5, 0.5)
)
cover_pc.save(
    cover_dir / "cover_pc.webp",
    "WEBP",
    quality=COVER_QUALITY,
    method=6,
    optimize=True
)

cover_mobile = ImageOps.fit(
    cover_src,
    COVER_MOBILE_SIZE,
    method=Image.Resampling.LANCZOS,
    centering=(0.5, 0.5)
)
cover_mobile.save(
    cover_dir / "cover_mobile.webp",
    "WEBP",
    quality=COVER_QUALITY,
    method=6,
    optimize=True
)

gallery_json = json.dumps(gallery_items, ensure_ascii=False)

html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>毕业纪念相册</title>
  <link rel="stylesheet" href="style.css">
  <style>
    .hero {{
      background-image:
        linear-gradient(135deg, rgba(18, 18, 18, 0.72), rgba(18, 18, 18, 0.24)),
        url("photos_v2/cover/cover_pc.webp");
    }}

    @media (max-width: 640px) {{
      .hero {{
        background-image:
          linear-gradient(135deg, rgba(18, 18, 18, 0.72), rgba(18, 18, 18, 0.24)),
          url("photos_v2/cover/cover_mobile.webp");
      }}
    }}

    .gallery-toolbar {{
      width: min(1180px, calc(100% - 28px));
      margin: 0 auto 28px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .load-more-btn {{
      min-width: 180px;
      height: 46px;
      padding: 0 24px;
      border: none;
      border-radius: 999px;
      cursor: pointer;
      font: inherit;
      font-weight: 800;
      color: #3a2c1d;
      background: #ffd891;
      box-shadow: 0 12px 30px rgba(70, 45, 20, 0.14);
    }}

    .load-more-btn:disabled {{
      opacity: 0.58;
      cursor: not-allowed;
    }}

    .gallery figure {{
      background: #f6efe4;
    }}

    .gallery figure img {{
      width: 100%;
      height: auto;
      display: block;
    }}
  </style>
</head>
<body>

  <header class="hero">
    <div class="hero-mask"></div>
    <div class="hero-content">
      <p class="eyebrow">GRADUATION · ALBUM</p>
      <h1>毕业纪念相册</h1>
      <p class="subtitle">把青春留在镜头里，把这一刻留给未来。</p>
      <a href="#gallery" class="hero-button">进入相册</a>
    </div>
  </header>

  <main>
    <section class="intro">
      <p class="section-tag">Photos</p>
      <h2>我们的毕业瞬间</h2>
      <p>页面会先加载一部分照片，继续浏览时可点击加载更多；点击照片可查看预览图并下载原始图片。</p>
    </section>

    <section class="gallery" id="gallery"></section>

    <div class="gallery-toolbar">
      <button id="loadMoreBtn" class="load-more-btn" type="button">加载更多照片</button>
    </div>
  </main>

  <div class="lightbox" id="lightbox">
    <button class="close" id="closeBtn">×</button>
    <img id="lightboxImg" src="" alt="照片预览">
    <a id="downloadBtn" class="download-btn" href="" download>下载原图</a>
  </div>

  <footer>
    <p>Graduation Album · 2026</p>
  </footer>

  <script>
    const GALLERY_ITEMS = {gallery_json};

    const INITIAL_COUNT = {INITIAL_COUNT};
    const LOAD_MORE_COUNT = {LOAD_MORE_COUNT};

    const gallery = document.getElementById('gallery');
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightboxImg');
    const closeBtn = document.getElementById('closeBtn');
    const downloadBtn = document.getElementById('downloadBtn');

    let renderedCount = 0;

    function openLightbox(previewUrl, originalUrl, filename) {{
      lightboxImg.src = previewUrl;
      downloadBtn.href = originalUrl;
      downloadBtn.setAttribute('download', filename || 'photo.jpg');
      lightbox.classList.add('show');
      document.body.style.overflow = 'hidden';
    }}

    function closeLightbox() {{
      lightbox.classList.remove('show');
      lightboxImg.src = '';
      downloadBtn.href = '';
      document.body.style.overflow = '';
    }}

    function renderMore(count) {{
      const nextItems = GALLERY_ITEMS.slice(renderedCount, renderedCount + count);

      nextItems.forEach((item, i) => {{
        const figure = document.createElement('figure');
        figure.className = 'photo-item ' + item.orientation;

        const img = document.createElement('img');
        img.src = item.thumb;
        img.dataset.preview = item.preview;
        img.dataset.original = item.original;
        img.alt = item.title;
        img.loading = renderedCount + i < 4 ? 'eager' : 'lazy';
        img.decoding = 'async';
        img.width = item.w;
        img.height = item.h;

        img.addEventListener('click', () => {{
          openLightbox(
            item.preview,
            item.original,
            item.original.split('/').pop()
          );
        }});

        figure.appendChild(img);
        gallery.appendChild(figure);
      }});

      renderedCount += nextItems.length;

      if (renderedCount >= GALLERY_ITEMS.length) {{
        loadMoreBtn.textContent = '已经到底啦';
        loadMoreBtn.disabled = true;
      }} else {{
        loadMoreBtn.textContent = `加载更多照片（${{renderedCount}} / ${{GALLERY_ITEMS.length}}）`;
      }}
    }}

    closeBtn.addEventListener('click', closeLightbox);

    lightbox.addEventListener('click', e => {{
      if (e.target === lightbox) {{
        closeLightbox();
      }}
    }});

    document.addEventListener('keydown', e => {{
      if (e.key === 'Escape') {{
        closeLightbox();
      }}
    }});

    loadMoreBtn.addEventListener('click', () => {{
      renderMore(LOAD_MORE_COUNT);
    }});

    renderMore(INITIAL_COUNT);
  </script>

</body>
</html>
'''

Path("index.html").write_text(html_content, encoding="utf-8")

print("\n全部完成！")
print("已生成：photos_v2/thumb  手机端缩略图")
print("已生成：photos_v2/large  点击预览图")
print("已生成：photos_v2/cover  首页封面图")
print("已更新：index.html，默认只加载前 24 张，点击加载更多继续显示")
