
#解析抖音用户主页示例

from bs4 import BeautifulSoup



filename = "user_page.html"
     

f = open(filename,"r",encoding="utf-8")
soup = BeautifulSoup(f,"html.parser")
# print(soup.prettify())

r = soup.findAll(name="div", attrs={"data-e2e" :"user-post-list"})

print(r[0].find().find().find().find().attrs["href"])










