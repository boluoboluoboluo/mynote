### 快速上手：播放器初始化

Video.js 的初始化主要有两种方式，都非常简单。

#### 1. 数据属性方式

最省事的方法，只需在 `<video>` 标签上添加 `data-setup` 属性，Video.js 会自动扫描并初始化。

html

```html
<!DOCTYPE html>
<html>
<head>
  <link href="https://unpkg.com/video.js/dist/video-js.css" rel="stylesheet">
  <script src="https://unpkg.com/video.js/dist/video.min.js"></script>
</head>
<body>
  <!-- 关键：添加 data-setup 属性，Video.js 会自动将其转换为功能丰富的播放器 -->
  <video id="my-video" class="video-js vjs-default-skin" controls preload="auto" 
         width="640" height="264" data-setup="{}">
    <source src="path/to/video.mp4" type="video/mp4">
    <!-- 只需正确设置 type，Video.js 就能自动识别并处理 -->
    <source src="https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8" type="application/x-mpegURL">
    <!-- 也可以播放 DASH 流，只需提供 .mpd 文件并设置 type 为 application/dash+xml -->
    <!-- <source src="https://example.com/manifest.mpd" type="application/dash+xml"> -->
    <p class="vjs-no-js">您的浏览器不支持HTML5视频，请升级或使用其他浏览器。</p>
  </video>
</body>
</html>
```



#### 2. JavaScript 方式

如果你需要更精细的控制，可以在页面加载完成后，通过 JavaScript 来初始化。

html

```
<!-- HTML 部分 -->
<video id="my-video" class="video-js vjs-default-skin" controls preload="auto" width="640" height="264">
  <source src="path/to/video.mp4" type="video/mp4">
</video>

<script>
  // JavaScript 初始化
  var player = videojs('my-video', {
    // 在这里配置播放器选项
    autoplay: false,
    controls: true,
    preload: 'auto'
  }, function onPlayerReady() {
    console.log('播放器已准备就绪');
    // 播放器准备好后可以在这里执行操作，例如开始播放
    // this.play();
  });
</script>
```



###  核心配置

Video.js 提供了很多配置项，可以让你定制播放器的行为。下面表格中是一些常用的配置项及其说明：

| 配置项 (Option)    | 类型 (Type)      | 说明 (Description)                                           |
| :----------------- | :--------------- | :----------------------------------------------------------- |
| `autoplay`         | boolean / string | 是否自动播放。由于浏览器的策略，通常需要配合 `muted: true` 或用户交互才能生效。 |
| `controls`         | boolean          | 是否显示播放控制栏。默认为 `true`。                          |
| `preload`          | string           | 预加载策略，可选值 `'auto'`、`'metadata'`、`'none'`。        |
| `width` / `height` | number / string  | 设置播放器的宽度和高度，单位是像素。                         |
| `fluid`            | boolean          | 是否启用流式（响应式）布局。设置为 `true` 时，播放器会根据父容器宽度自适应，并保持设定的宽高比。 |
| `aspectRatio`      | string           | 指定播放器的宽高比，如 `'16:9'` 或 `'4:3'`。                 |
| `poster`           | string           | 视频封面图的 URL。                                           |
| `muted`            | boolean          | 是否默认静音。                                               |
| `loop`             | boolean          | 是否循环播放。                                               |
| `playbackRates`    | array            | 设置播放速度选项，例如 `[0.5, 1, 1.5, 2]`。                  |
| `language`         | string           | 设置播放器界面语言，如 `'zh-CN'`。                           |
| `techOrder`        | array            | 指定回放技术的顺序，例如 `['html5', 'youtube']`。            |
| `sources`          | array            | 以数组形式配置多个视频源，用于自动切换。                     |
| `plugins`          | object           | 用于初始化和管理插件。                                       |
| `controlBar`       | object           | 用来定制控制栏的具体组件，比如显示/隐藏某些按钮。            |

### 核心 API 方法

在获取到 `player` 对象后，你可以通过它提供的方法来控制视频播放。

| 方法名 (Method)          | 说明 (Description)                                           |
| :----------------------- | :----------------------------------------------------------- |
| `play()`                 | 开始播放视频。                                               |
| `pause()`                | 暂停播放视频。                                               |
| `src(newSource)`         | 获取或设置视频源。如果需要切换视频，可以调用 `player.src(newUrl)`。 |
| `currentTime([seconds])` | 获取或设置当前播放进度（单位：秒）。                         |
| `duration()`             | 获取视频总时长（单位：秒）。                                 |
| `volume([percent])`      | 获取或设置音量（0 到 1 之间）。                              |
| `muted([value])`         | 获取或设置静音状态。                                         |
| `requestFullscreen()`    | 请求全屏模式。                                               |
| `exitFullscreen()`       | 退出全屏模式。                                               |
| `dispose()`              | 销毁播放器实例，释放资源。                                   |
| `reset()`                | 重置播放器的状态。                                           |

下面是一个简单的示例，展示了如何播放和暂停视频：

javascript

```
var player = videojs('my-video');

// 播放视频
player.play();

// 5秒后暂停
setTimeout(function() {
  player.pause();
}, 5000);
```



###  事件系统

Video.js 支持丰富的事件，方便你监听播放器的各种状态变化，并执行自定义逻辑。

| 事件名 (Event)   | 触发时机 (Trigger)                               |
| :--------------- | :----------------------------------------------- |
| `play`           | 视频**开始**播放时（包括从暂停恢复）。           |
| `pause`          | 视频被**暂停**时。                               |
| `playing`        | 视频因缓冲或延迟而暂停后，**恢复**播放时。       |
| `ended`          | 视频**播放结束**时。                             |
| `waiting`        | 因数据不足而**等待缓冲**时。                     |
| `timeupdate`     | 播放进度**更新**时（通常每秒触发 4 次）。        |
| `seeking`        | 用户**正在拖动**进度条，进行跳转时。             |
| `seeked`         | 用户**完成**进度条拖拽，跳转动作**完成**时。     |
| `canplay`        | 浏览器**可以开始播放**视频时（但可能还需缓冲）。 |
| `loadedmetadata` | 视频的元数据（如时长、尺寸）**加载完成**时。     |
| `error`          | 播放器**发生错误**时。                           |

你可以通过 `player.on()` 方法来监听事件。

javascript

```
player.on('play', function() {
  console.log('视频开始播放！');
});

player.on('ended', function() {
  console.log('播放结束，准备播放推荐视频...');
});
```



###  插件生态

插件是 Video.js 的一大优势，社区提供了丰富的插件来扩展功能。

- **清晰度切换**：常用的有 `videojs-resolution-switcher`、`videojs-hls-quality-selector` 或 `videojs-resolution-switcher-v7` 等。
- **移动端优化**：`videojs-mobile-ui` 插件可以针对移动设备增加双击快进/快退、滑动控制手势、横屏自动全屏等优化，提升用户体验。
- **缩略图预览**：`videojs-sprite-thumbnails` 插件可以在进度条悬停时显示预览图。
- **广告集成**：`videojs-ads` 和 `videojs-ima` 是官方支持的广告插件，方便插入广告。
- **播放技术扩展**：通过 `videojs-youtube`、`videojs-vimeo` 等插件，可以让 Video.js 直接播放 YouTube、Vimeo 等平台的视频。
- **自定义插件**：Video.js 也支持开发自己的插件来满足特定需求。随着版本迭代，插件写法也从简单的函数演进到了更规范的 ES6 Class 模式。

### 移动端适配

在移动端使用 Video.js 时，需要注意以下几点：

1. **响应式布局**：为了让视频播放器能适应不同屏幕尺寸，可以设置播放器宽度为百分比，并利用 `padding-bottom` 来固定宽高比，实现自适应。最简单的方法是将 `fluid` 选项设置为 `true`，或通过 CSS 将播放器宽度设为 100%。
2. **处理自动播放限制**：在 iOS 等移动设备上，未静音的视频无法自动播放。如果希望自动播放，可以设置 `autoplay: true` 和 `muted: true`。
3. **处理 iOS 默认全屏**：在 iOS 上，播放视频可能会自动进入原生全屏模式。可以在 `<video>` 标签中添加 `playsinline` 属性，防止这种行为。

### 性能优化

要保证视频播放流畅，可以从几个方面入手。

- **利用 CDN**：将视频文件存放在内容分发网络（CDN）上，可以显著加快视频加载速度。
- **调整缓冲策略**：Video.js 提供了 `bufferTime` 等配置选项，用于控制缓冲区的大小。需要根据实际场景调优，避免因缓冲过小导致卡顿，或缓冲过大增加首屏等待时间。
- **监控缓冲状态**：可以通过监听 `waiting` 和 `canplay` 等事件来了解播放器的缓冲状态，从而实现自定义的缓冲提示。
- **启用流式传输**：对于长视频，推荐使用 HLS 或 DASH 等流式协议。这些协议能根据网络状况动态调整码率，实现自适应传输，减少卡顿和加载时间，提升播放体验。

### 常见问题与解决方案

1. **视频源切换问题**：直接修改 `src` 属性可能导致加载失败。最佳实践是先调用 `player.dispose()` 销毁旧实例，再创建新实例。
2. **浏览器兼容性问题**：为确保旧版浏览器（如 IE 11）的支持，需要提供 MP4 格式的视频源，并确保服务器正确配置了 MIME 类型。
3. **MIME 类型配置**：服务器需要为 `.m3u8` 文件返回 `application/vnd.apple.mpegurl` 或 `application/x-mpegURL`，为 `.ts` 文件返回 `video/MP2T`。
4. **跨域资源共享（CORS）**：如果视频资源和前端页面在不同域名下，服务器需要配置 CORS 响应头。
5. **缓冲与性能问题**：如果播放卡顿，可以检查网络连接情况，并尝试调整 `bufferTime` 等参数。
6. **错误处理**：应该监听 `error` 事件，并进行相应的提示或尝试重试，以提升用户体验。

