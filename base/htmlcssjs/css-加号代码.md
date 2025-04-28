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

