#### 说明

在PDF中，使用JavaScript时必须通过特定的对象来调用函数。例如，**为了使用alert()函数，需要使用APP对象进行调用，这样可以限制通过JavaScript进行攻击时的功能范围。**这种特性使得在PDF内嵌入JavaScript时，其安全性得到了一定程度的保障。

除了将JavaScript嵌入PDF文件中执行，**还有可能利用基于DOM的方法来执行PDF XSS**。这种技术由Stefano Di Paola和Giorgio Fedon在第23届CCC安全会议中提出，并详细阐述了其原理。他们将PDF中的DOM XSS称为**UXSS（Universal Cross-Site Scripting）**。值得一提的是，**任何提供PDF文件在线浏览的网站**都可能面临这种安全风险。

#### 写入javascript

code:

```python
from PyPDF2 import PdfWriter		#pip install PyPDF2
import io

#创建pdf
writer = PdfWriter()
#添加javascript
js_code = """
app.alert('hello from javascript')
"""
writer.add_js(js_code)

# 创建一页（可选）
from PyPDF2 import PageObject
page = PageObject.create_blank_page(width=200, height=200)
writer.add_page(page)

with open("output.pdf","wb") as f:
	writer.write(f)

print("PDF文件已创建并添加JavaScript代码")
```

####  在pdf文件添加javascript

code:

```python
from PyPDF2 import PdfWriter,PdfReader		#pip install PyPDF2
import io

# 读取现有PDF
input_pdf = PdfReader(open('output.pdf', 'rb'))

#创建pdf
writer = PdfWriter()

# 复制所有页面
for page in input_pdf.pages:
    writer.add_page(page)

# 添加JavaScript
js_code = """
function showMessage() {
    app.alert('Hello from Python!');
}

// 文档打开时执行
showMessage();
"""
writer.add_js(js_code)

# 创建一页（可选）
from PyPDF2 import PageObject
page = PageObject.create_blank_page(width=200, height=200)
writer.add_page(page)

with open("output_with_js.pdf","wb") as f:
	writer.write(f)

print("JavaScript已添加到现有PDF")
```



#### 查看

```sh
#查看pdf文件的javascript:
# 1.下载pdf-parser.py
wget https://didierstevens.com/files/software/pdf-parser_V0_7_5.zip
# 2.解压并运行
python pdf-parser.py -a your_document.pdf
# 3.搜索JavaScript
python pdf-parser.py -s JavaScript your_document.pdf
```

