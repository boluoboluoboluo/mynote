### beautifulsoup

> 2024-03

+ 安装命令

```sh
pip install beautifulsoup4
```

+ 示例代码

```py
import requests
from bs4 import BeautifulSoup

url = "https://www.baidu.com"

r = requests.get(url)
r.encoding="utf-8"
# print(r.text)

soup = BeautifulSoup(r.text,"html.parser")
# soup = BeautifulSoup(open("d:/demo.html"),"html.parser")	#打开一个html文件

# print(soup.prettify())	#格式化展示

print(soup.title)	#打印标题

tag = soup.a 	#获取第一个a标签
print(tag)
print(tag.name)
print(tag.parent.name)	#父标签
print(tag.attrs)	#打印标签属性
print(tag.attrs["class"])	#class属性
print(tag.string)	#标签内容

# soup = BeautifulSoup("<p><!--commemt--></p>","html.parser")
# tag2 = soup.p
# print(tag2.string)
# print(type(tag2.string))	#标签内容为注释类型

# soup.select("#id")	#根据id查找
# soup.select(".class")	#根据类名查找
# soup.select("p #id")	#组合查找
# soup.select("p[class='xx'")	#组合查找2
# soup.select("head > title")	#子标签查找
# tags = soup.select("tag")	#获取所有tag标签
# print(tags)


# tag = soup.body
# content = tag.contents	#子节点，列表类型
# print(content)
# print(tag.children)		#子节点，iterator类型
# for i in tag.children:
# 	print(i)
# print(tag.descendants)		#子孙节点，iterator类型

# print(tag.parent)	#父亲节点
# print(tag.parents)	#父亲节点，iterator类型

# print(tag.next_sibling)	#下一个节点
# print(tag.next_siblings)	#下一个平行节点，iterator类型

# print(tag.previout_sibling)	#上一个节点
# print(tag.previout_sibling)	#上一个节点，iterator类型
```

#### find_all函数

```py
find_all(name,attrs,recursive,string,**kwargs)
返回列表类型
name:标签名称
attrs：标签属性
string:字符串
recursive:是否对子孙全部检索，默认true

r = find_all('a',string="hello")	#查找a标签，内容包含hello的信息

引申方法：
find()		#只返回一个结果，string类型
find_parent()
find_parents()
find_next_siblings()
find_next_sibling()
find_previous_siblings()
find_previous_sibling()
```

示例：

```py
#根据标签属性查找
#<div data-name="user-post-list"
r = soup.findAll(name="div", attrs={"data-name" :"user-post-list"})
print(r[0])		#取第一个

#返回第一个子节点的第一个子节点
r = soup.find().find()
print(r.attrs["href"])	#href的值

#正则查找
#查找image标签的src属性值包含字符串"v3-web.douyinvod.com"
r = soup.findAll(name="image", attrs={"src" :re.compile(r"v3-web.douyinvod.com")})
```

