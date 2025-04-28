import requests
from tqdm import tqdm
import time
from bs4 import BeautifulSoup


# #博主主页url示例
# USER_URL = "https://www.douyin.com/user/MS4wLjABAAAAPqCLgR9_pfXmR8mCggcgPLmiLXUCvy1qh9JhoANMcNU"
# #视频地址示例
# DOWN_URL = "https://www.douyin.com/video/7320965214248127795"

#视频下载地址示例
DOWN_URL = "https://v3-web.douyinvod.com/6dde215e6e0c258631f4c72666a6972d/65ee0bbd/video/tos/cn/tos-cn-ve-15/oYxPQfbQDAGlFsXAzZEVUMIEmBCEezwg7h92sA/?a=6383&ch=26&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=1062&bt=1062&cs=2&ds=6&ft=t8IwoxyERR0si0C4kDn2Ncy3kIXbvLrOAGNgx4kCHVYnYvjThW&mime_type=video_mp4&qs=11&rc=NzQ4aDU7OmU6NTg7ZTgzPEBpanV5N3c5cmZucDMzNGkzM0BfMzMtL19gXi4xYDFeYC0tYSNtLS9zMmRzamBgLS1kLS9zcw%3D%3D&btag=e00030000&cquery=100a&dy_q=1710095407&feature_id=e585bce62f14c124a0ac1450c3a95af2&l=202403110230077496CED5B3441B870410"

dir_file = "tmp/"


def down(url,dst_file):
    total_size=0
    chunk_size=1024
    try:
        r = requests.get(url,stream=True)
        # print(r.headers.get('content-length', 0))       #可能获取不到该值

        total_size = int(r.headers.get('content-length', 0))
        bar = tqdm(desc="下载",total=total_size,unit='B',unit_scale=True,unit_divisor=chunk_size,ncols=50)
        fout = open(dst_file,"wb")

        for d in r.iter_content(chunk_size):
            # time.sleep(0.3)
            fout.write(d)
            bar.update(chunk_size)
        bar.close()
        print("下载完成。")
    except Exception as e:
        print("下载出错："+e)
    finally:
        fout.close()
        

def main():

    url = DOWN_URL

    urls = []
    urls.append(url)
    # urls.append(url)
    index = 1
    for i in urls:
        tmp_file = dir_file+"down"+str(index)+".mp4"
        down(url,tmp_file)
        index = index+1

# main()








