from PIL import Image, ImageOps
from pathlib import Path

src_dir = Path("images")
thumb_dir = Path("photos_v2/thumb")
large_dir = Path("photos_v2/large")

thumb_dir.mkdir(parents=True, exist_ok=True)
large_dir.mkdir(parents=True, exist_ok=True)

# 如果某些照片依旧方向不对，把文件名填到这里
# 例如：FORCE_ROTATE_90 = {"DSC4853.JPG", "DSC4861.JPG"}
FORCE_ROTATE_90 = set()

valid_suffix = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}

for img_path in src_dir.iterdir():
    if img_path.suffix not in valid_suffix:
        continue

    name = img_path.stem

    img = Image.open(img_path)

    # 读取 EXIF 方向
    try:
        exif = img.getexif()
        orientation = exif.get(274, None)
    except Exception:
        orientation = None

    print(f"{img_path.name} 原始尺寸: {img.size}, EXIF方向: {orientation}")

    # 按 EXIF 自动修正方向
    img = ImageOps.exif_transpose(img)

    # 如果 EXIF 没用，手动强制旋转
    if img_path.name in FORCE_ROTATE_90:
        img = img.rotate(90, expand=True)

    img = img.convert("RGB")

    print(f"{img_path.name} 修正后尺寸: {img.size}")

    # 大图预览
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

    print(f"已生成: {name}_thumb.webp / {name}_large.webp\n")