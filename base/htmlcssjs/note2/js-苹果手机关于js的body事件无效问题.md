### 苹果手机js的body事件点击无效的问题

关于`$('body').on('click',selector,function(){})`点击无效

解决方案：选择器selector设置样式即可
```css
selector {
    cursor: pointer;
}
```

