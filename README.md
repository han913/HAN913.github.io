# 毕业纪念相册网站

这是一个用于展示毕业照片的静态相册网站，支持照片浏览、放大预览、原图下载、同学投稿、后台审核和已通过投稿删除。项目页面部署在 Netlify，图片上传使用 Cloudinary，投稿审核数据使用 Netlify Blobs 保存。

## 功能介绍

### 1. 毕业相册展示

首页展示已有毕业照片，页面加载时使用压缩后的缩略图，点击照片后可以打开大图预览，并支持下载原图。

### 2. 同学照片投稿

用户可以通过 `upload.html` 上传照片，并填写姓名和留言。上传后的照片不会直接显示在首页，而是进入待审核列表。

### 3. 后台照片审核

管理员通过 `admin.html` 输入后台密码后，可以查看待审核照片，并进行：

* 通过：照片进入已通过列表，并显示在首页“同学投稿”区域
* 拒绝：照片从待审核列表移除，不显示在首页

### 4. 已通过投稿管理

后台支持查看已经审核通过的投稿照片，并可以将不需要展示的照片从网站列表中删除。

注意：删除已通过投稿只会从网站展示列表中移除记录，不会删除 Cloudinary 中的原始图片文件。

## 项目结构

```text
HAN913.github.io/
├── index.html                  # 相册首页
├── upload.html                 # 照片上传页面
├── admin.html                  # 照片审核后台
├── style.css                   # 页面样式
├── package.json                # Node 依赖配置
├── package-lock.json
├── photos_v2/                  # 已有照片的缩略图和大图
├── images/                     # 已有照片原图
└── netlify/
    └── functions/
        ├── submit-photo.js     # 投稿保存接口
        ├── list-pending.js     # 获取待审核照片
        ├── approve-photo.js    # 审核通过/拒绝接口
        ├── list-approved.js    # 获取已通过照片
        └── delete-approved.js  # 删除已通过投稿记录
```

## 技术栈

* HTML
* CSS
* JavaScript
* Netlify
* Netlify Functions
* Netlify Blobs
* Cloudinary

## 本地依赖

项目使用 `@netlify/blobs` 保存待审核和已通过投稿数据。

安装依赖：

```bash
npm install
```

如果依赖缺失，可以单独安装：

```bash
npm install @netlify/blobs
```

## Netlify 环境变量

后台审核密码通过 Netlify 环境变量配置。

需要在 Netlify 项目后台添加：

```text
ADMIN_PASS=你的后台审核密码
```

建议设置为：

```text
Same value for all deploy contexts
```

并确保作用范围包含 Functions。

修改环境变量后，需要重新部署 Netlify：

```text
Deploys → Trigger deploy → Deploy site
```

## Cloudinary 配置

照片上传使用 Cloudinary。

当前上传页面需要配置：

```text
Cloud name
Upload preset
```

如果更换 Cloudinary 账号或上传预设，需要在 `upload.html` 中修改对应配置。

投稿流程为：

```text
用户上传图片 → Cloudinary 保存图片 → submit-photo 写入 pending → 管理员审核 → approve-photo 移入 approved → 首页显示
```

## 部署方式

项目通过 GitHub 推送后，由 Netlify 自动部署。

常用提交命令：

```bash
git add .
git commit -m "更新网站功能"
git push origin main
```

Netlify 部署完成后，访问：

```text
https://你的站点域名/
```

后台审核页面：

```text
https://你的站点域名/admin.html
```

上传页面：

```text
https://你的站点域名/upload.html
```

## 常见问题

### 1. 后台提示密码错误或加载失败

检查 Netlify 环境变量是否正确：

```text
Key 必须是 ADMIN_PASS
```

如果刚修改过密码，需要重新部署 Netlify。

### 2. 上传后没有出现在首页

上传后的照片需要先进入后台审核，通过后才会显示在首页。

### 3. 审核通过后首页不显示

检查以下接口是否有数据：

```text
/.netlify/functions/list-approved
```

如果接口有数据但首页不显示，通常是 `index.html` 没有正确加载 `list-approved`。

### 4. 删除已通过照片后 Cloudinary 里还存在

这是正常的。后台删除功能只删除网站展示记录，不删除 Cloudinary 原始文件。

### 5. Netlify 显示 Plugin Error

如果提示 21YunBox 插件错误，但网站状态仍然是 Published，通常不影响 Netlify 网站和 Functions 使用。该插件错误只与额外的中国 CDN 部署有关。

## 后续可优化方向

* 增加投稿照片标题和留言展示样式
* 给后台增加分页
* 增加 Cloudinary 原图删除接口
* 增加上传大小限制提示
* 增加审核操作日志
* 给后台页面增加更明显的状态提示
* 给首页投稿照片增加瀑布流布局
