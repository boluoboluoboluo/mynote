### css加号代码

```css
.add_ele {
    display:inline-block;
    border: 1px solid;
    width: 12px;
    height: 12px;
    color: #555555;
    position: relative;
}
.add_ele::before {
 content: '';
 position: absolute;
 left: 50%;
 top: 50%;
 width: 8px;
 margin-left: -4px;
 margin-top: -0.5px;
 border-top: 1px solid;
}
.add_ele::after{
  content: '';
  position: absolute;
  left: 50%;
  top: 50%;
  height: 8px;
  margin-left: -0.5px;
  margin-top: -4px;
  border-left: 1px solid;
}
```

### 细表格样式



```css
table.gridtable {
    width:60%;
    margin-left:100px;
    font-size:11px;
    color:#333333;
    border-width: 1px;
    border-top-style: solid;
    border-right-style: solid;
    border-color: #666666;
    border-collapse: separate;
}
table.gridtable th {
    /*border-width: 1px;
    padding: 8px;
    border-style: solid;
    border-color: #666666;
    background-color: #dedede;*/
}
table.gridtable td {
    border-width: 1px;
    padding: 5px;
    border-style: solid;
    border-top-style: none;
    border-right-style: none;
    border-color: #666666;
    background-color: #ffffff;
}
```

```css
/* 边框合并 */
.gc-table{
    border-collapse: collapse;
}
.gc-table td{
    border: 1px solid gray;
}
```

### 页面图片置灰

```css
<style>
    html{
    filter: grayscale(100%);
    -webkit-filter: grayscale(100%);
    -moz-filter: grayscale(100%);
    -ms-filter: grayscale(100%);
    -o-filter: grayscale(100%);
    filter:progid:DXImageTransform.Microsoft.BasicImage(grayscale=1);
    }
</style>
```

