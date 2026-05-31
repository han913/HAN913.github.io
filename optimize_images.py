from PIL import Image, ImageOps
from pathlib import Path

# ===== 文件夹配置 =====
src_dir = Path("images")
thumb_dir = Path("photos_v2/thumb")
large_dir = Path("photos_v2/large")

thumb_dir.mkdir(parents=True, exist_ok=True)
large_dir.mkdir(parents=True, exist_ok=True)

# ===== 如果某些竖图方向还是不对，在这里手动加文件名 =====
# 顺时针旋转90度
FORCE_ROTATE_90 = set()

# 逆时针旋转90度
FORCE_ROTATE_NEG90 = set()

# 旋转180度
FORCE_ROTATE_180 = set()

# 支持的图片格式
valid_suffix = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}

# 获取所有原图
image_files = sorted(
    [p for p in src_dir.iterdir() if p.suffix in valid_suffix],
    key=lambda p: p.name
)

if not image_files:
    print("images 文件夹中没有找到图片")
    exit()

print(f"共找到 {len(image_files)} 张图片，开始处理...\n")

# ===== 生成压缩图片 =====
for img_path in image_files:
    name = img_path.stem

    img = Image.open(img_path)

    # 关键：修正相机照片EXIF方向，防止竖图变横图
    img = ImageOps.exif_transpose(img)

    # 如果EXIF无效，可手动强制旋转
    if img_path.name in FORCE_ROTATE_90:
        img = img.rotate(90, expand=True)

    if img_path.name in FORCE_ROTATE_NEG90:
        img = img.rotate(-90, expand=True)

    if img_path.name in FORCE_ROTATE_180:
        img = img.rotate(180, expand=True)

    img = img.convert("RGB")

    # 网页预览大图
    large = img.copy()
    large.thumbnail((2200, 2200))
    large.save(
        large_dir / f"{name}_large.webp",
        "WEBP",
        quality=88,
        method=6
    )

    # 缩略图
    thumb = img.copy()
    thumb.thumbnail((800, 800))
    thumb.save(
        thumb_dir / f"{name}_thumb.webp",
        "WEBP",
        quality=78,
        method=6
    )

    print(f"处理完成：{img_path.name}")

# ===== 自动生成 HTML 中的图片列表 =====
figures_html = ""

for idx, img_path in enumerate(image_files, start=1):
    name = img_path.stem
    original_path = f"images/{img_path.name}"
    thumb_path = f"photos_v2/thumb/{name}_thumb.webp"
    large_path = f"photos_v2/large/{name}_large.webp"

    figures_html += f'''      <figure>
        <img src="{thumb_path}" data-preview="{large_path}" data-original="{original_path}" alt="毕业照{idx}" loading="lazy" decoding="async">
      </figure>

'''

# 首页背景图默认用第一张照片
first_name = image_files[0].stem
hero_image = f"photos_v2/large/{first_name}_large.webp"

# ===== 生成完整 index.html =====
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
        linear-gradient(135deg, rgba(18, 18, 18, 0.72), rgba(18, 18, 18, 0.22)),
        url("{hero_image}");
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
      <p>点击照片可以放大查看，预览图经过压缩以提升加载速度；如需保存高清版本，可在预览界面下载原始图片。</p>
    </section>

    <section class="gallery" id="gallery">
{figures_html}    </section>
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
    const galleryImages = document.querySelectorAll('.gallery img');
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightboxImg');
    const closeBtn = document.getElementById('closeBtn');
    const downloadBtn = document.getElementById('downloadBtn');

    galleryImages.forEach(img => {{
      img.addEventListener('click', () => {{
        lightboxImg.src = img.dataset.preview;
        downloadBtn.href = img.dataset.original;
        downloadBtn.setAttribute('download', img.dataset.original.split('/').pop());
        lightbox.classList.add('show');
        document.body.style.overflow = 'hidden';
      }});
    }});

    function closeLightbox() {{
      lightbox.classList.remove('show');
      lightboxImg.src = '';
      downloadBtn.href = '';
      document.body.style.overflow = '';
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
  </script>

</body>
</html>
'''

Path("index.html").write_text(html_content, encoding="utf-8")

print("\n全部完成！")
print("已自动生成 photos_v2 压缩图片")
print("已自动更新 index.html 图片列表")