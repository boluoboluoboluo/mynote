##### 说明

解决不通机型情况下div的位置始终与背景图一致，使用`margin-top: xx%`

```html
<!-- 假设背景图在body上 -->
<body style="background-image: url('/.../test.jpg');background-size:100%;">
    <!-- 通过margin-top设置相对位置固定，值必须为百分比 -->
    <div style="width:30%;height:30px;margin-top:50%;">
		这是div
    </div>
</body>
```

