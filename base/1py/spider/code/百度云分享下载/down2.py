import requests
import json
from datetime import datetime
import re
import urllib

###
#功能说明：根据百度云分享链接，进行下载
###

############################################################################################################
#1.验证：
#share_url：分享的百度云链接
#code：提取码
#说明：验证成功返回名为randsk的随机串，以及cookie，需要cookie中的内容进行后续操作
def verify(share_url,code):
    verify_url = "https://pan.baidu.com/share/verify"       #验证url
    index = share_url.rfind("/")    #分享链接尾部随机码
    url_code = share_url[index+2:]    #分享链接尾部随机码

    stamp = datetime.now().timestamp()
    t = int(round(stamp * 1000))        #当前毫秒

    params = {
        "t": t,
        "surl": url_code,
        "channel": "chunlei",
        "web": 1,
        "bdstoken": "",
        "clienttype": 0,
    }

    data={
        "pwd":code,
        "vcode":"",
        "vcode_str":""
    }
    headers={
        "content-type":"application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "host":"pan.baidu.com",
        "origin":"https://pan.baidu.com",
        "referer":"https://pan.baidu.com/share/init?surl="
    }

    r = requests.post(verify_url,params=params,data=data,headers=headers)

    #解析
    d = json.loads(r.content)
    verify_res_cookie = r.headers["Set-Cookie"]
    # print(verify_res_cookie)
    # print(d)

    # 解析cookie获取BAIDUID
    bdtemp = re.search(r"BAIDUID.*?;",verify_res_cookie).group()
    verify_data = {}
    verify_data["baiduid"] = bdtemp[8:len(bdtemp)-1]
    verify_data["bdclnd"] = d["randsk"]

    return verify_data

######################################################
#2.获取页面数据（验证之后才能进入）
#获取分享的文件id,名称，大小等
def get_page(share_url,bdclnd):

    headers2 = {
        "content-type":"application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Host":"pan.baidu.com",
    }
    cookies = {
        "BDCLND":bdclnd
    }

    r = requests.get(share_url,headers=headers2,cookies=cookies)
    html = r.text

    page_data = {}
    #解析数据
    reg = r"window.yunData=\{.*\}"
    m = re.search(reg,html)
    s1 = m.group()
    share_uk = re.search(r"share_uk:\"(.*?)\"",s1).group()      # .*? 表示非贪婪匹配
    shareid = re.search(r"shareid:\"(.*?)\"",s1).group()
    page_data["uk"] = share_uk[10:len(share_uk)-1]
    page_data["sid"] = shareid[9:len(shareid)-1]

    fs_id = re.search(r"\"fs_id\".*?,",html).group()
    # print(fs_id)
    page_data["fid"] = fs_id[8:len(fs_id)-1]        #文件id
    # print(fid)
    
    filename_tmp = re.search(r"\"server_filename\".*?,",html).group()
    page_data["filename"] = filename_tmp[len("server_filename")+4:len(filename_tmp)-2]

    filesize_tmp = re.search(r"file_size.*?\"",html).group()
    page_data["filesize"] = filesize_tmp[len("file_size")+1:len(filesize_tmp)-1]

    return page_data

############################################################################################################
#3.配置，用于获取签名(拿到签名才能进行下一步操作)
def tplconf(share_url,verify_data):
    index = share_url.rfind("/")    #分享链接尾部随机码
    url_code = share_url[index+1:]    #分享链接尾部随机码(！注意：这个多一位，和验证方法里获取的不一致)

    headers2 = {
        "content-type":"application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "host":"pan.baidu.com",
        "origin":"https://pan.baidu.com",
        "referer":"https://pan.baidu.com/s/",
    }
    cookies = {
        # "BAIDUID":"5922352EF7661222C8832395C96FDB52:FG=1",
        # "BDCLND":"TzHQLsAA8ALX3C2qNYTNtmwuwpfFWSZpu%2BF%2BPMIZRWI%3D",
        "BAIDUID":verify_data["baiduid"],
        "BDCLND":verify_data["bdclnd"]
    }
    params = {
        # "surl":"1PIhUGXaO4CEzA_jO_CuybQ",
        "surl":url_code,
        "fields":"sign,timestamp",
        "channel": "chunlei",
        "web": 1,
        "clienttype": 0,
    }

    url = "https://pan.baidu.com/share/tplconfig"
    r2 = requests.get(url,headers=headers2,params=params,cookies=cookies)
    json_str = json.loads(r2.content)

    tplconf_data = {}
    tplconf_data["sign"] = json_str["data"]["sign"]
    tplconf_data["timestamp"] = json_str["data"]["timestamp"]
    # print(tplconf_data)

    return tplconf_data

############################################################################################################
# 4.获取分享的文件下载链接
def get_downlink(verify_data,page_data,tplconf_data):
    url = "https://pan.baidu.com/api/sharedownload"

    headers2 = {
        "content-type":"application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "host":"pan.baidu.com",
        "origin":"https://pan.baidu.com",
        "referer":"https://pan.baidu.com/s/",
    }
    cookies = {
        # "BAIDUID":"5922352EF7661222C8832395C96FDB52:FG=1",
        # "BDCLND":"TzHQLsAA8ALX3C2qNYTNtmwuwpfFWSZpu%2BF%2BPMIZRWI%3D",
        "BAIDUID":verify_data["baiduid"],                       #验证方法返回cookie中获取
        "BDCLND":verify_data["bdclnd"]                          #验证方法返回cookie中获取，或者验证方法返回
    }
    params = {
        # "sign": "66f172bcaa2046ead0d7c207c0caec7fa8e6cc74",
        "sign":tplconf_data["sign"],                                #配置方法中返回的签名
        "channel":"chunlei",
        # "timestamp":"1731194954",
        "timestamp":tplconf_data["timestamp"],                         #配置方法中返回的时间戳
        "web":"1",
        "clienttype":0,
    }

    fid_list = "[" + page_data["fid"] + "]"         #数据格式
    bdclnd2 = urllib.parse.unquote(verify_data["bdclnd"])                    #未url编码的BDCLND
    extrakey = '{"sekey":"' + bdclnd2 + '"}'          #数据格式    

    data = {
        "encrypt":0,
        "product":"share",
        # "extra":'{"sekey":"TzHQLsAA8AJZzbeFQxdHbyVQe8Khc91jdJuh4knh6gU="}',
        "extra":extrakey,
        "primaryid":"56585796828",
        "uk":"3594736151",
        # "fid_list":'[1063342666924389]',
        "fid_list":fid_list,
        "path_list":"",
        "vip":0
    }
    # print(data)

    r2 = requests.post(url,headers=headers2,params=params,data=data,cookies=cookies)

    json_str = json.loads(r2.content)
    # print(json_str)
    down_link = json_str["list"][0]["dlink"]

    return down_link

############################################################################################################
# 5.下载文件
def down(down_link,page_data):
    r = requests.get(down_link,stream=True)     #stream=True表示开启流下载，(不立即下载)
    print(r.headers)
    # fout = open(page_data["filename"],"wb")
    # fout.write(r.content)
    # fout.close()






############################################################################################################
# 测试开始...

print("开始分析...")
share_url = "https://pan.baidu.com/s/1PIhUGXaO4CEzA_jO_CuybQ"     #分享链接
# share_url = "https://pan.baidu.com/s/1Gimrx90G5-icdtrpmmzVpg"     #2
code = "1111"       #提取码

verify_data = verify(share_url,code)  #验证
print("verify_data:")
print(verify_data)

page_data = get_page(share_url,verify_data["bdclnd"])    #获取页面数据
print("page_data:")
print(page_data)

tplconf_data = tplconf(share_url,verify_data)           #配置
print("tplconf_data:")
print(tplconf_data)

down_link = get_downlink(verify_data,page_data,tplconf_data)    #获取下载链接
print("down_link:")
print(down_link)

down(down_link,page_data)     #下载 	如下载异常，可能次数频繁导致页面过期








