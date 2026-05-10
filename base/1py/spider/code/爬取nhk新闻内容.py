import requests
from bs4 import BeautifulSoup,Tag,NavigableString
# from bs4 import NavigableString

'''
爬取nhk 网站日文内容,并去除日文顶部假名发音
'''


url = "https://news.web.nhk/news/easy/ne2026021211457/ne2026021211457.html"		#示例url
headers = {
	"Cookie":""		#此处需补充cookie
}
r = requests.get(url,headers=headers)
r.encoding = "utf-8"

soup = BeautifulSoup(r.text,"html.parser")
# print(soup.prettify())	#格式化展示
tag = soup.select(".article-body")		#内容节点
# print(tag)
content = tag[0]
re_lines = ""

print("===============================")
for i in content.children:		# p节点
	if isinstance(i,Tag):		# 通过此处过滤 NavigableString 内容
		for ii in i.children:	# span节点
			if ii.ruby:
				s = "".join(ii.ruby.find_all(string=True,recursive=False))	#此方法只获取标签内容(不用管子节点)
				s2 = "".join(ii.find_all(string=True,recursive=False))
				re_lines = re_lines + s + s2
			else:
				re_lines = re_lines + ii.string 	#ii.string:获取标签内容(无子节点时此方法可用)

	re_lines = re_lines + "\n"

print(re_lines)