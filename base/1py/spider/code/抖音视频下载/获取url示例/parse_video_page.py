#解析抖音用户主页下某个视频主页示例

from bs4 import BeautifulSoup
import re


filename = "video_page.html"
     

f = open(filename,"r",encoding="utf-8")
soup = BeautifulSoup(f,"html.parser")
# print(soup.prettify())

r = soup.findAll(name="source", attrs={"src" :re.compile(r"v3-web.douyinvod.com")})

print(r[0].attrs["src"])