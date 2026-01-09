### 安卓微信h5支付refer丢失问题

下面两种方式 android WebView 中不会丢失referer：

```js
//方式一： js提交表单
<script>
    document.form.method= "post";     
    document.form.action= "https://wx.tenpay.com/cgi-bin/mmpayweb-bin/checkmweb?支付信息 ";
    document.form.submit(); 
</script>
```

```js
//方式二： jquery动态创建表单
var action='https://wx.tenpay.com/cgi-bin/mmpayweb-bin/checkmweb?支付信息 ' 
    var form = $("<form></form>")
    form.attr('action', action)
    form.attr('method', 'post')
    //追加到body，不显示，然后提交
    form.appendTo("body")
    form.css('display', 'none')
    form.submit()
```

