# 毕业纪念相册网站

这是一个用于展示毕业照的静态网页项目，基于 HTML、CSS 和 JavaScript 编写，部署于 GitHub Pages，并可通过 Netlify 进行二次部署。网站主要用于存放和展示毕业照片，支持缩略图快速浏览、点击放大预览以及下载原始图片。

## 项目介绍

本项目用于搭建一个简洁、美观、适合手机端和电脑端访问的毕业纪念相册网站。网页采用响应式布局设计，在电脑端以瀑布流形式展示照片，在手机端自动适配为更适合浏览的单列布局。图片经过压缩处理后用于网页加载，减少访问等待时间，同时保留原始图片用于下载。

## 主要功能

* 毕业照在线展示
* 响应式页面布局
* 手机端 UI 适配
* 图片懒加载
* 缩略图快速预览
* 点击图片放大查看
* 下载原始大小图片
* 支持 GitHub Pages 部署
* 支持 Netlify 部署

## 项目结构

```text
HAN913.github.io/
├── index.html              # 网站首页
├── style.css               # 页面样式
├── optimize_images.py      # 图片压缩与页面自动生成脚本
├── images/                 # 原始毕业照片
├── photos_v2/
│   ├── thumb/              # 网页缩略图
│   └── large/              # 网页预览大图
└── README.md               # 项目说明文件
```

## 使用方法

### 1. 添加新照片

将新的原始照片复制到 `images` 文件夹中。

建议图片命名使用英文、数字或下划线，避免中文、空格和特殊符号。例如：

```text
DSC5001.JPG
DSC5002.JPG
```

如果照片文件名前面带有 `_`，可以在 PowerShell 中执行以下命令去掉开头的下划线：

```powershell
Get-ChildItem .\images\_*.JPG | ForEach-Object {
    $newName = $_.Name.TrimStart('_')
    $target = Join-Path $_.DirectoryName $newName

    if (Test-Path $target) {
        Write-Host "跳过：$($_.Name)，因为 $newName 已存在"
    } else {
        Rename-Item $_.FullName -NewName $newName
        Write-Host "已改名：$($_.Name) -> $newName"
    }
}
```

### 2. 生成压缩图片和网页内容

运行图片处理脚本：

```powershell
python optimize_images.py
```

脚本会自动完成以下操作：

* 读取 `images` 文件夹中的原始照片
* 生成网页缩略图到 `photos_v2/thumb`
* 生成网页预览图到 `photos_v2/large`
* 自动更新 `index.html` 中的照片列表

### 3. 提交并上传到 GitHub

```powershell
git add images photos_v2 index.html style.css optimize_images.py README.md
git commit -m "更新毕业照相册"
git pull --rebase origin main
git push origin main
```

上传完成后，GitHub Pages 会自动更新网站。

## 图片说明

本项目采用三类图片：

```text
images/        原始图片，用于下载
photos_v2/thumb/   缩略图，用于页面快速加载
photos_v2/large/   预览图，用于点击放大查看
```

这样可以避免网页直接加载原始大图，提高访问速度，同时保留高清原图下载功能。

## 部署方式

### GitHub Pages

本项目可直接通过 GitHub Pages 部署。仓库名为：

```text
HAN913.github.io
```

部署后可通过以下地址访问：

```text
https://HAN913.github.io
```

### Netlify

也可以在 Netlify 中导入该 GitHub 仓库进行部署。

部署设置：

```text
Build command：留空
Publish directory：/
```

部署成功后，可以使用 Netlify 提供的 `.netlify.app` 地址访问网站，也可以绑定自定义域名。

## 注意事项

* 不建议一次上传过多原始照片，容易导致 Git push 速度慢或失败
* 建议每次新增 10～20 张照片后提交一次
* 原始照片较大时，网页加载应使用压缩后的缩略图
* 如果竖版照片方向异常，可在 `optimize_images.py` 中设置手动旋转
* 修改网页样式时主要编辑 `style.css`
* 添加照片后主要运行 `optimize_images.py`，不需要手动逐张修改 HTML

## 项目用途

该网站主要用于毕业照片展示和纪念，可作为班级、个人或团队毕业相册页面使用，方便同学通过网页浏览照片并下载原图保存。
