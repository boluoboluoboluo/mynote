#### js浮点运算实现

```js
<script>
//获取小数位数
function getPrecision(num) {
  const str = num.toString();
  if (str.indexOf('.') === -1) return 0;
  return str.split(".")[1].length;
}

function add(a, b) {
  const p1 = getPrecision(a);
  const p2 = getPrecision(b);
  const m = Math.pow(10, Math.max(p1, p2));
  return (a * m + b * m) / m;
}

function sub(a, b) {
  const p1 = getPrecision(a);
  const p2 = getPrecision(b);
  const m = Math.pow(10, Math.max(p1, p2));
  return (a * m - b * m) / m;
}
function mul(a, b) {
  const s1 = a.toString(), s2 = b.toString();
  let m = 0;
  try { m += s1.split(".")[1].length; } catch (e) {}
  try { m += s2.split(".")[1].length; } catch (e) {}
  return Number(s1.replace(".", "")) * Number(s2.replace(".", "")) / Math.pow(10, m);
}
function div(a, b) {
  const p1 = getPrecision(a);
  const p2 = getPrecision(b);
  const r1 = Number(a.toString().replace(".", ""));
  const r2 = Number(b.toString().replace(".", ""));
  return (r1 / r2) * Math.pow(10, p2 - p1);
}
function mod(a, b) {
  const p1 = getPrecision(a);
  const p2 = getPrecision(b);
  const m = Math.pow(10, Math.max(p1, p2));
  return ((a * m) % (b * m)) / m;
}
</script>
```

