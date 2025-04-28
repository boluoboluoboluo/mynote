

#### 获取不到数据bug

```js
//增加afterChange方法
<script>
	KindEditor.ready(function(K) {
        window.editor = K.create('#editor_id',{
                afterChange:function(){				// ***注意：数据改变立刻同步
                    this.sync();
                }
            }
        );
	});
</script>
```

