##### ios的问题

描述：ios系统，在app里发起微信h5支付，支付完成后没有返回app，而是打开了safari浏览器

解决办法：在微信支付中间页的回调地址`redirect_url`采用`urlscheme`形式

```php
//回调地址示例
$re = 'https://wx.tenpay.com/cgi-bin/mmpayweb-bin/checkmweb?xxxx=xxx&xxx=x..........'.
    '&redirect_url=xxx.h5支付域名.com://xxx.xxx.com/shop/payCallBack?orderId=xxxxx';
//说明xxx.h5支付域名.com为微信商户后台配置的支付域名，同时该域名也必须配置到app的urlscheme中去
```



##### 安卓问题

描述：安卓系统，内嵌H5，在app里发起微信h5支付，支付完成后返回app，出现空白页面

分析：微信支付的中间页的回调地址`redirect_url`掉用了2次，第一次发起支付之前就已经调用，这其中和app

的相关调用方法有关。解决方法未知

思路：不设置`redirect_url`，在支付页面设置定时器，每隔2秒查询支付结果，支付完成则跳转