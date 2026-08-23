##### 安装后的设置

settings.json 设置:

`打开方式: 设置->settings-> 右上角 open settings(json) `

```json
{
    "window.commandCenter": false,		//顶部搜索隐藏

    // ==========================================
    // 不必要的后台联网与自动扫描功能
    // ==========================================
    "telemetry.telemetryLevel": "off",               // 关闭隐私数据上报
    "update.mode": "none",                           // 关闭软件自动检查更新
    "extensions.autoUpdate": "none",                 // 关闭插件自动更新
    "extensions.autoCheckUpdates": false,            // 关闭插件联网检查
    "extensions.ignoreRecommendations": true,        // 关闭烦人的联网插件推荐
    "workbench.activityBar.location": "hidden",

    "git.enabled": false,                            // 彻底关闭自带的 Git 自动扫描
    "git.autoRepositoryDetection": false,            // 彻底关闭 Git 仓库自动侦测
    "npm.autoDetect": "off",                         // 关闭自带的 npm 脚本自动扫描
    "gulp.autoDetect": "off",                        // 关闭 gulp 自动扫描
    "grunt.autoDetect": "off",                       // 关闭 grunt 自动扫描
    "workbench.welcomePage.walkthroughs.openOnInstall": false,  // 禁用安装后的欢迎向导
    "workbench.enableExperiments": false, 

    "editor.minimap.enabled": false,
    "chat.titleBar.signIn.enabled": false,
    "workbench.editor.enablePreview": false,
    "workbench.colorTheme": "Dark+"
}
```



##### 去掉黄色波浪线

在代码中添加类型提示注释：

```py
import bencode  # type: ignore
```

##### 卸载

```sh
1.控制面板卸载
2.win+r,输入%USERPROFILE%,删除.vscode文件夹	# 插件删除
3.win+r,输入%APPDATA%,删除Code文件夹			# 设置,项目记录,缓存
```

##### 其他

```sh
# 安装python 语法高亮和提示插件
插件: 搜索 python ,第1个,安装

# 安装ai插件 cline
1.搜索cline,第1个
2.点左侧栏机器人,配置模型api	#deepseek,需官网创建apikey,充值
3.显示不友好,右键机器人,move to -> second side bar
```

