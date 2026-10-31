use collab_ui::collab_panel;
use gpui::{App, Menu, MenuItem, OsAction};
use project::DisableAiSettings;
use release_channel::ReleaseChannel;
use settings::Settings;
use terminal_view::terminal_panel;
use zed_actions::{Quit, assistant, debug_panel, dev, git_panel, project_panel};

pub fn app_menus(cx: &mut App) -> Vec<Menu> {
    let mut view_items = vec![
        MenuItem::action(
            "Zoom In",
            zed_actions::IncreaseBufferFontSize { persist: false },
        ),
        MenuItem::action(
            "Zoom Out",
            zed_actions::DecreaseBufferFontSize { persist: false },
        ),
        MenuItem::action(
            "Reset Zoom",
            zed_actions::ResetBufferFontSize { persist: false },
        ),
        MenuItem::action(
            "Reset All Zoom",
            zed_actions::ResetAllZoom { persist: false },
        ),
        MenuItem::separator(),
        MenuItem::action("切换左侧停靠区", workspace::ToggleLeftDock),
        MenuItem::action("切换右侧停靠区", workspace::ToggleRightDock),
        MenuItem::action("切换底部停靠区", workspace::ToggleBottomDock),
        MenuItem::action("切换所有停靠区", workspace::ToggleAllDocks),
        MenuItem::submenu(Menu {
            name: "编辑器布局".into(),
            disabled: false,
            items: vec![
                MenuItem::action("向上拆分", workspace::SplitUp::default()),
                MenuItem::action("向下拆分", workspace::SplitDown::default()),
                MenuItem::action("向左拆分", workspace::SplitLeft::default()),
                MenuItem::action("向右拆分", workspace::SplitRight::default()),
            ],
        }),
        MenuItem::separator(),
        MenuItem::action("项目面板", project_panel::ToggleFocus),
        MenuItem::action("大纲面板", outline_panel::ToggleFocus),
        MenuItem::action("协作面板", collab_panel::ToggleFocus),
        MenuItem::action("终端面板", terminal_panel::Toggle),
        MenuItem::action("调试器面板", debug_panel::ToggleFocus),
    ];

    if !DisableAiSettings::get_global(cx).disable_ai {
        view_items.push(MenuItem::action("Agent Panel", assistant::ToggleFocus));
    }

    view_items.extend([
        MenuItem::action("Git 面板", git_panel::ToggleFocus),
        MenuItem::separator(),
        MenuItem::action("诊断信息", diagnostics::Deploy),
        MenuItem::separator(),
    ]);

    if ReleaseChannel::try_global(cx) == Some(ReleaseChannel::Dev) {
        view_items.push(MenuItem::action(
            "Toggle GPUI Inspector",
            dev::ToggleInspector,
        ));
        view_items.push(MenuItem::separator());
    }

    vec![
        Menu {
            name: "Zed".into(),
            disabled: false,
            items: vec![
                MenuItem::action("关于 Zed", zed_actions::About),
                MenuItem::action("检查更新", auto_update::Check),
                MenuItem::separator(),
                MenuItem::submenu(Menu::new("设置").items([
                    MenuItem::action("打开设置", zed_actions::OpenSettings),
                    MenuItem::action("打开设置配置文件", super::OpenSettingsFile),
                    MenuItem::action("打开项目设置", zed_actions::OpenProjectSettings),
                    MenuItem::action("打开项目设置文件", super::OpenProjectSettingsFile),
                    MenuItem::action("打开默认设置", super::OpenDefaultSettings),
                    MenuItem::separator(),
                    MenuItem::action("打开快捷键设置", zed_actions::OpenKeymap),
                    MenuItem::action("打开快捷键配置文件", zed_actions::OpenKeymapFile),
                    MenuItem::action("打开默认快捷键", zed_actions::OpenDefaultKeymap),
                    MenuItem::separator(),
                    MenuItem::action(
                        "Select Theme...",
                        zed_actions::theme_selector::Toggle::default(),
                    ),
                    MenuItem::action(
                        "Select Icon Theme...",
                        zed_actions::icon_theme_selector::Toggle::default(),
                    ),
                ])),
                MenuItem::separator(),
                #[cfg(target_os = "macos")]
                MenuItem::os_submenu("Services", gpui::SystemMenuType::Services),
                MenuItem::separator(),
                MenuItem::action("扩展插件", zed_actions::Extensions::default()),
                #[cfg(not(target_os = "windows"))]
                MenuItem::action("安装命令行工具 (CLI)", install_cli::InstallCliBinary),
                MenuItem::separator(),
                #[cfg(target_os = "macos")]
                MenuItem::action("隐藏 Zed", super::Hide),
                #[cfg(target_os = "macos")]
                MenuItem::action("隐藏其他", super::HideOthers),
                #[cfg(target_os = "macos")]
                MenuItem::action("显示全部", super::ShowAll),
                MenuItem::separator(),
                MenuItem::action("退出 Zed", Quit),
            ],
        },
        Menu {
            name: "文件".into(),
            disabled: false,
            items: vec![
                MenuItem::action("新建", workspace::NewFile),
                MenuItem::action("新建窗口", workspace::NewWindow),
                MenuItem::separator(),
                #[cfg(not(target_os = "macos"))]
                MenuItem::action("打开文件...", workspace::OpenFiles),
                MenuItem::action(
                    if cfg!(not(target_os = "macos")) {
                        "Open Folder..."
                    } else {
                        "Open…"
                    },
                    workspace::Open::default(),
                ),
                MenuItem::action("打开最近项目…", zed_actions::OpenRecent::default()),
                MenuItem::action("打开远程…", zed_actions::OpenRemote::default()),
                MenuItem::separator(),
                MenuItem::action("添加文件夹到项目…", workspace::AddFolderToProject),
                MenuItem::separator(),
                MenuItem::action("保存", workspace::Save { save_intent: None }),
                MenuItem::action("另存为…", workspace::SaveAs),
                MenuItem::action("保存全部", workspace::SaveAll { save_intent: None }),
                MenuItem::separator(),
                MenuItem::action(
                    "Close Editor",
                    workspace::CloseActiveItem {
                        save_intent: None,
                        close_pinned: true,
                    },
                ),
                MenuItem::action("关闭项目", workspace::CloseProject),
                MenuItem::action("关闭窗口", workspace::CloseWindow),
            ],
        },
        Menu {
            name: "编辑".into(),
            disabled: false,
            items: vec![
                MenuItem::os_action("撤销", editor::actions::Undo, OsAction::Undo),
                MenuItem::os_action("重做", editor::actions::Redo, OsAction::Redo),
                MenuItem::separator(),
                MenuItem::os_action("剪切", editor::actions::Cut, OsAction::Cut),
                MenuItem::os_action("复制", editor::actions::Copy, OsAction::Copy),
                MenuItem::action("复制并修剪空白", editor::actions::CopyAndTrim),
                MenuItem::os_action("粘贴", editor::actions::Paste, OsAction::Paste),
                MenuItem::separator(),
                MenuItem::action("查找", search::buffer_search::Deploy::find()),
                MenuItem::action("在项目中查找", workspace::DeploySearch::default()),
                MenuItem::separator(),
                MenuItem::action(
                    "Toggle Line Comment",
                    editor::actions::ToggleComments::default(),
                ),
            ],
        },
        Menu {
            name: "选择".into(),
            disabled: false,
            items: vec![
                MenuItem::os_action(
                    "Select All",
                    editor::actions::SelectAll,
                    OsAction::SelectAll,
                ),
                MenuItem::action("扩大选择范围", editor::actions::SelectLargerSyntaxNode),
                MenuItem::action("缩小选择范围", editor::actions::SelectSmallerSyntaxNode),
                MenuItem::action("选择下一个兄弟节点", editor::actions::SelectNextSyntaxNode),
                MenuItem::action(
                    "Select Previous Sibling",
                    editor::actions::SelectPreviousSyntaxNode,
                ),
                MenuItem::separator(),
                MenuItem::action(
                    "Add Cursor Above",
                    editor::actions::AddSelectionAbove {
                        skip_soft_wrap: true,
                    },
                ),
                MenuItem::action(
                    "Add Cursor Below",
                    editor::actions::AddSelectionBelow {
                        skip_soft_wrap: true,
                    },
                ),
                MenuItem::action(
                    "Select Next Occurrence",
                    editor::actions::SelectNext {
                        replace_newest: false,
                    },
                ),
                MenuItem::action(
                    "Select Previous Occurrence",
                    editor::actions::SelectPrevious {
                        replace_newest: false,
                    },
                ),
                MenuItem::action("选择所有匹配项", editor::actions::SelectAllMatches),
                MenuItem::separator(),
                MenuItem::action("向上移动行", editor::actions::MoveLineUp),
                MenuItem::action("向下移动行", editor::actions::MoveLineDown),
                MenuItem::action("向下复制选择行", editor::actions::DuplicateLineDown),
            ],
        },
        Menu {
            name: "视图".into(),
            disabled: false,
            items: view_items,
        },
        Menu {
            name: "转到".into(),
            disabled: false,
            items: vec![
                MenuItem::action("后退", workspace::GoBack),
                MenuItem::action("前进", workspace::GoForward),
                MenuItem::separator(),
                MenuItem::action("命令面板...", zed_actions::command_palette::Toggle),
                MenuItem::separator(),
                MenuItem::action("转到文件...", workspace::ToggleFileFinder::default()),
                // MenuItem::action("转到项目中的符号", project_symbols::Toggle),
                MenuItem::action(
                    "Go to Symbol in Editor...",
                    zed_actions::outline::ToggleOutline,
                ),
                MenuItem::action("转到行/列...", editor::actions::ToggleGoToLine),
                MenuItem::separator(),
                MenuItem::action(
                    "Go to Definition",
                    editor::actions::GoToDefinition::default(),
                ),
                MenuItem::action(
                    "Go to Declaration",
                    editor::actions::GoToDeclaration::default(),
                ),
                MenuItem::action(
                    "Go to Type Definition",
                    editor::actions::GoToTypeDefinition::default(),
                ),
                MenuItem::action(
                    "Find All References",
                    editor::actions::FindAllReferences::default(),
                ),
                MenuItem::action("Show Incoming Calls", call_hierarchy::ShowIncomingCalls),
                MenuItem::action("Show Outgoing Calls", call_hierarchy::ShowOutgoingCalls),
                MenuItem::separator(),
                MenuItem::action("下一个问题", editor::actions::GoToDiagnostic::default()),
                MenuItem::action(
                    "Previous Problem",
                    editor::actions::GoToPreviousDiagnostic::default(),
                ),
            ],
        },
        Menu {
            name: "运行".into(),
            disabled: false,
            items: vec![
                MenuItem::action(
                    "Spawn Task",
                    zed_actions::Spawn::ViaModal {
                        reveal_target: None,
                    },
                ),
                MenuItem::action("启动调试器", debugger_ui::Start),
                MenuItem::separator(),
                MenuItem::action("Edit tasks.json…", zed_actions::OpenProjectTasks),
                MenuItem::action("Edit debug.json…", zed_actions::OpenProjectDebugTasks),
                MenuItem::separator(),
                MenuItem::action("继续", debugger_ui::Continue),
                MenuItem::action("单步跳过", debugger_ui::StepOver),
                MenuItem::action("单步进入", debugger_ui::StepInto),
                MenuItem::action("单步跳出", debugger_ui::StepOut),
                MenuItem::separator(),
                MenuItem::action("切换断点", editor::actions::ToggleBreakpoint),
                MenuItem::action("编辑断点", editor::actions::EditLogBreakpoint),
                MenuItem::action("清除所有断点", debugger_ui::ClearAllBreakpoints),
            ],
        },
        Menu {
            name: "窗口".into(),
            disabled: false,
            items: vec![
                MenuItem::action("最小化", super::Minimize),
                MenuItem::action("缩放窗口", super::Zoom),
                MenuItem::separator(),
            ],
        },
        Menu {
            name: "帮助".into(),
            disabled: false,
            items: vec![
                MenuItem::action(
                    "View Release Notes Locally",
                    auto_update_ui::ViewReleaseNotesLocally,
                ),
                MenuItem::action("查看遥测日志", zed_actions::OpenTelemetryLog),
                MenuItem::action("查看依赖开源协议", zed_actions::OpenLicenses),
                MenuItem::action("显示欢迎页面", onboarding::ShowWelcome),
                MenuItem::separator(),
                MenuItem::action("提交缺陷反馈...", zed_actions::feedback::FileBugReport),
                MenuItem::action("提交功能建议...", zed_actions::feedback::RequestFeature),
                MenuItem::action("发送邮件给官方...", zed_actions::feedback::EmailZed),
                MenuItem::separator(),
                MenuItem::action(
                    "Documentation",
                    super::OpenBrowser {
                        url: "https://zed.dev/docs".into(),
                    },
                ),
                MenuItem::action("Zed GitHub 仓库", feedback::OpenZedRepo),
                MenuItem::action(
                    "Zed Twitter",
                    super::OpenBrowser {
                        url: "https://twitter.com/zeddotdev".into(),
                    },
                ),
                MenuItem::action(
                    "Join the Team",
                    super::OpenBrowser {
                        url: "https://zed.dev/jobs".into(),
                    },
                ),
            ],
        },
    ]
}
