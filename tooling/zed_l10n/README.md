# Zed 编辑器全自动汉化工具链 (Zed Localization Toolchain)

本工具链为 Zed 编辑器（基于 Rust + GPUI）自研的编译期无损源码级汉化方案。

## 核心特性
- **零运行时开销**：在编译前将提取的 UI 字符串无损替换为中文，保留 Zed 的毫秒级启动与 120 FPS 原生渲染性能。
- **一键打补丁与还原**：支持 `--apply` 和 `--restore`，随时一键还原回纯净官方英文源码。
- **支持云端构建**：配置了专属的 GitHub Actions 工作流（`.github/workflows/build-chinese.yml`），无需本地安装庞大的 Visual Studio 与 Rust 环境即可自动编译出 Windows 安装包。

---

## 目录结构
```text
tooling/zed_l10n/
├── extract.py         # 智能提取源码中的菜单、按钮、提示、标签等 UI 字符串
├── generate_dict.py    # 从提取的字符串生成基础中英映射词典
├── enrich_dict.py      # 富化词典（注入高频 IDE / Git / 智能体中文词条）
├── patch.py            # 执行源码汉化替换 / 一键还原
├── build_windows.ps1   # Windows 本地一键汉化构建脚本
└── locales/
    ├── extracted_strings.json   # 扫描提取出的原始字符串数据
    └── zh-CN.json               # 核心简体中文词典
```

---

## 使用指南

### 1. 扫描与提取 UI 字符串
若官方上游更新了代码，运行以下命令即可重新扫描提取所有新词条：
```powershell
python tooling/zed_l10n/extract.py
```

### 2. 更新中英对照词典
运行以下命令更新并补充词条：
```powershell
python tooling/zed_l10n/generate_dict.py
python tooling/zed_l10n/enrich_dict.py
```
你也可以直接打开 `tooling/zed_l10n/locales/zh-CN.json` 手动微调或新增翻译。

### 3. 应用汉化补丁
```powershell
python tooling/zed_l10n/patch.py
```
补丁将自动对所有涉及的 `.rs` 源码文件进行安全的精准替换。

### 4. 一键还原源码（恢复英文）
```powershell
python tooling/zed_l10n/patch.py --restore
```
或直接通过 git 还原：
```powershell
git checkout -- crates/
```

---

## 构建与打包

### 方式 A：GitHub Actions 云端自动构建（推荐 ⭐）
1. 在 GitHub 上新建一个你的个人仓库（例如 `my-zed-chinese`）。
2. 将当前分支推送到你的 GitHub：
   ```powershell
   git remote add origin https://github.com/<你的用户名>/<你的仓库名>.git
   git push -u origin chinese-l10n
   ```
3. 在 GitHub 网页上的 **Actions** 标签页，工作流 `Build Zed Chinese Release (Windows)` 将会自动触发编译，完成后在构建产物中下载 `zed-windows-chinese.zip` 即可直接运行！

### 方式 B：本地编译（需安装 Rust 1.95.0 + MSVC）
```powershell
.\tooling\zed_l10n\build_windows.ps1
```
产物将生成在 `target/release/zed.exe`。
