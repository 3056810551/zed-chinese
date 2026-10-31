"""
Dictionary Generator for Zed Chinese Localization
Generates a comprehensive zh-CN translation dictionary for all extracted strings.
"""

import json
from pathlib import Path

LOCALES_DIR = Path(__file__).resolve().parent / "locales"
EXTRACTED_FILE = LOCALES_DIR / "extracted_strings.json"
ZH_CN_FILE = LOCALES_DIR / "zh-CN.json"

# Curated high-frequency and domain-specific IDE dictionary
CORE_TRANSLATIONS = {
    # Application & Main Menu
    "About Zed": "关于 Zed",
    "Check for Updates": "检查更新",
    "Check for updates": "检查更新",
    "Settings": "设置",
    "Open Settings": "打开设置",
    "Open Settings File": "打开设置配置文件",
    "Open Project Settings": "打开项目设置",
    "Open Project Settings File": "打开项目设置文件",
    "Open Default Settings": "打开默认设置",
    "Open Keymap": "打开快捷键设置",
    "Open Keymap File": "打开快捷键配置文件",
    "Open Default Key Bindings": "打开默认快捷键",
    "Select Theme...": "选择主题...",
    "Select Icon Theme...": "选择图标主题...",
    "Services": "服务",
    "Extensions": "扩展",
    "Install CLI": "安装命令行工具 (CLI)",
    "Hide Zed": "隐藏 Zed",
    "Hide Others": "隐藏其他",
    "Show All": "显示全部",
    "Quit Zed": "退出 Zed",

    # File Menu
    "File": "文件",
    "New": "新建",
    "New Window": "新建窗口",
    "Open File...": "打开文件...",
    "Open Folder...": "打开文件夹...",
    "Open…": "打开…",
    "Open Recent…": "打开最近项目…",
    "Open Remote…": "打开远程…",
    "Add Folder to Project…": "添加文件夹到项目…",
    "Add Folders to Project…": "添加文件夹到项目…",
    "Save": "保存",
    "Save As…": "另存为…",
    "Save All": "保存全部",
    "Close Editor": "关闭编辑器",
    "Close Project": "关闭项目",
    "Close Window": "关闭窗口",
    "Reopen Closed Editor": "重新打开关闭的编辑器",

    # Edit Menu
    "Edit": "编辑",
    "Undo": "撤销",
    "Redo": "重做",
    "Cut": "剪切",
    "Copy": "复制",
    "Copy and Trim": "复制并修剪空白",
    "Paste": "粘贴",
    "Find": "查找",
    "Find in Project": "在项目中查找",
    "Toggle Line Comment": "切换行注释",
    "Toggle Block Comment": "切换块注释",

    # Selection Menu
    "Selection": "选择",
    "Select All": "全选",
    "Expand Selection": "扩大选择范围",
    "Shrink Selection": "缩小选择范围",
    "Select Next Sibling": "选择下一个兄弟节点",
    "Select Previous Sibling": "选择上一个兄弟节点",
    "Add Cursor Above": "在上方添加光标",
    "Add Cursor Below": "在下方添加光标",
    "Select Next Occurrence": "选择下一个匹配项",
    "Select Previous Occurrence": "选择上一个匹配项",
    "Select All Occurrences": "选择所有匹配项",
    "Move Line Up": "向上移动行",
    "Move Line Down": "向下移动行",
    "Duplicate Selection": "向下复制选择行",

    # View Menu
    "View": "视图",
    "Zoom In": "放大",
    "Zoom Out": "缩小",
    "Reset Zoom": "重置缩放",
    "Reset All Zoom": "重置所有窗口缩放",
    "Toggle Left Dock": "切换左侧停靠区",
    "Toggle Right Dock": "切换右侧停靠区",
    "Toggle Bottom Dock": "切换底部停靠区",
    "Toggle All Docks": "切换所有停靠区",
    "Toggle Fullscreen": "切换全屏",
    "Toggle Centered Layout": "切换居中布局",
    "Editor Layout": "编辑器布局",
    "Split Up": "向上拆分",
    "Split Down": "向下拆分",
    "Split Left": "向左拆分",
    "Split Right": "向右拆分",
    "Project Panel": "项目面板",
    "Outline Panel": "大纲面板",
    "Collab Panel": "协作面板",
    "Terminal Panel": "终端面板",
    "Debugger Panel": "调试器面板",
    "Diagnostics": "诊断信息",
    "Toggle GPUI Inspector": "切换 GPUI 检查器",

    # Go Menu
    "Go": "转到",
    "Back": "后退",
    "Forward": "前进",
    "Command Palette...": "命令面板...",
    "Go to File...": "转到文件...",
    "Go to Symbol in Project": "转到项目中的符号",
    "Go to Symbol in Editor...": "转到编辑器中的符号...",
    "Go to Line/Column...": "转到行/列...",
    "Go to Definition": "转到定义",
    "Go to Declaration": "转到声明",
    "Go to Type Definition": "转到类型定义",
    "Go to Implementation": "转到实现",
    "Find All References": "查找所有引用",
    "Next Problem": "下一个问题",
    "Previous Problem": "上一个问题",

    # Run & Debug Menu
    "Run": "运行",
    "Spawn Task": "运行任务",
    "Start Debugger": "启动调试器",
    "Edit tasks.json...": "编辑 tasks.json...",
    "Edit debug.json...": "编辑 debug.json...",
    "Continue": "继续",
    "Step Over": "单步跳过",
    "Step Into": "单步进入",
    "Step Out": "单步跳出",
    "Toggle Breakpoint": "切换断点",
    "Edit Breakpoint": "编辑断点",
    "Clear All Breakpoints": "清除所有断点",

    # Window Menu
    "Window": "窗口",
    "Minimize": "最小化",
    "Zoom": "缩放窗口",

    # Help Menu
    "Help": "帮助",
    "View Release Notes Locally": "查看本地版本说明",
    "View Telemetry": "查看遥测日志",
    "View Dependency Licenses": "查看依赖开源协议",
    "Show Welcome": "显示欢迎页面",
    "File Bug Report...": "提交缺陷反馈...",
    "Request Feature...": "提交功能建议...",
    "Email Us...": "发送邮件给官方...",
    "Documentation": "官方文档",
    "Zed Repository": "Zed GitHub 仓库",
    "Zed Twitter": "Zed 官方 Twitter",
    "Join the Team": "加入 Zed 团队",

    # Project Panel Context Menu
    "Search Inside": "在文件夹中搜索",
    "New File": "新建文件",
    "New Folder": "新建文件夹",
    "Reveal in File Manager": "在资源管理器中显示",
    "Reveal in Finder": "在访达中显示",
    "Open in Default App": "在默认应用中打开",
    "Open in Terminal": "在集成终端中打开",
    "Find in Folder…": "在文件夹中查找…",
    "Unfold Directory": "展开目录",
    "Fold Directory": "折叠目录",
    "Compare Marked Files": "对比已标记的文件",
    "Duplicate": "复制副本",
    "Delete": "删除",
    "Rename": "重命名",
    "Copy Path": "复制绝对路径",
    "Copy Relative Path": "复制相对路径",
    "Copy Name": "复制名称",
    "Collapse All": "全部折叠",
    "Expand All": "全部展开",
    "Add to .gitignore": "添加到 .gitignore",
    "Add to .git/info/exclude": "添加到 .git/info/exclude",

    # Git & Source Control
    "Git": "Git",
    "Stage All": "暂存所有更改",
    "Unstage All": "取消暂存所有更改",
    "Stage": "暂存",
    "Unstage": "取消暂存",
    "Commit": "提交",
    "Commit Message": "提交说明",
    "Amend": "修补提交 (Amend)",
    "Push": "推送 (Push)",
    "Pull": "拉取 (Pull)",
    "Fetch": "抓取 (Fetch)",
    "Discard": "放弃更改",
    "Discard All Changes": "放弃所有更改",
    "Branches": "分支",
    "New Branch": "新建分支",
    "Checkout": "切换分支",
    "Stash": "贮藏 (Stash)",
    "Pop Stash": "应用并弹出贮藏",
    "Changes": "更改",
    "Staged Changes": "已暂存的更改",
    "Unstaged Changes": "未暂存的更改",
    "File History": "文件历史记录",
    "Blame": "Git 追溯 (Blame)",
    "Toggle Git Blame": "切换 Git 追溯信息",

    # Assistant & Agent UI
    "Assistant": "AI 助手",
    "Agent": "智能体 Agent",
    "New Chat": "新建对话",
    "New Thread": "新建对话线程",
    "Clear Chat": "清空对话",
    "Inline Assist": "行内智能辅助",
    "Generate": "生成代码",
    "Accept": "接受更改",
    "Reject": "拒绝更改",
    "Apply": "应用更改",
    "Model": "模型",
    "Provider": "服务商",
    "Add Provider": "添加服务商",
    "Add Model": "添加模型",
    "Add Server": "添加服务器",
    "Temperature": "采样温度",
    "Max Tokens": "最大 Token 数",
    "Tokens": "Token",

    # Terminal UI
    "Terminal": "终端",
    "New Terminal": "新建终端",
    "Split Terminal": "拆分终端",
    "Close Terminal": "关闭终端",
    "Close Terminal Tab": "关闭终端标签页",
    "Clear Terminal": "清空终端",
    "Scroll to Top": "滚动到顶部",
    "Scroll to Bottom": "滚动到底部",

    # Common Dialogs & Buttons
    "OK": "确定",
    "Ok": "确定",
    "Cancel": "取消",
    "Close": "关闭",
    "Done": "完成",
    "Apply Changes": "应用更改",
    "Don't Save": "不保存",
    "Do you want to save?": "是否保存所做更改？",
    "Save Changes": "保存更改",
    "Yes": "是",
    "No": "否",
    "Retry": "重试",
    "Reload": "重新加载",
    "Restart": "重启",
    "Confirm": "确认",
    "Filter": "过滤",
    "Filter...": "过滤...",
    "Search": "搜索",
    "Search...": "搜索...",
    "Clear": "清除",
    "Reset": "重置",
    "Remove": "移除",
    "Install": "安装",
    "Uninstall": "卸载",
    "Update": "更新",
    "Enable": "启用",
    "Disable": "禁用",
    "Configure": "配置",
    "Refresh": "刷新",
    "Loading...": "加载中...",
    "Saving...": "保存中...",
    "Connecting...": "连接中...",
    "Connected": "已连接",
    "Disconnected": "已断开",
    "Error": "错误",
    "Warning": "警告",
    "Info": "提示",
    "Success": "成功",
}

# Suffix and prefix rules for automatic handling
PUNCT_MAP = {
    "...": "...",
    "…": "…",
    ":": "：",
    "?": "？",
    "!": "！",
}

def generate_dictionary():
    if not EXTRACTED_FILE.exists():
        print("Error: extracted_strings.json does not exist. Run extract.py first.")
        return

    with open(EXTRACTED_FILE, "r", encoding="utf-8") as fp:
        extracted = json.load(fp)

    existing_dict = {}
    if ZH_CN_FILE.exists():
        try:
            with open(ZH_CN_FILE, "r", encoding="utf-8") as fp:
                existing_dict = json.load(fp)
        except Exception:
            pass

    full_dict = {}
    translated_count = 0
    missing_count = 0

    for en_text in extracted.keys():
        # 1. Existing translated dictionary takes precedence
        if en_text in existing_dict and existing_dict[en_text].strip():
            full_dict[en_text] = existing_dict[en_text]
            translated_count += 1
            continue

        # 2. Curated core dictionary
        if en_text in CORE_TRANSLATIONS:
            full_dict[en_text] = CORE_TRANSLATIONS[en_text]
            translated_count += 1
            continue

        # 3. Check trimmed punctuation variations
        stripped = en_text.rstrip(".…:?! ")
        suffix = en_text[len(stripped):]
        if stripped in CORE_TRANSLATIONS:
            zh_trans = CORE_TRANSLATIONS[stripped] + suffix
            full_dict[en_text] = zh_trans
            translated_count += 1
            continue

        # Untranslated entries
        full_dict[en_text] = ""
        missing_count += 1

    ZH_CN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(ZH_CN_FILE, "w", encoding="utf-8") as fp:
        json.dump(full_dict, fp, indent=2, ensure_ascii=False)

    print(f"Generated zh-CN dictionary: {len(full_dict)} total keys.")
    print(f"  - Translated: {translated_count} ({translated_count / len(full_dict) * 100:.1f}%)")
    print(f"  - Missing: {missing_count}")
    print(f"Saved to: {ZH_CN_FILE}")

if __name__ == "__main__":
    generate_dictionary()
