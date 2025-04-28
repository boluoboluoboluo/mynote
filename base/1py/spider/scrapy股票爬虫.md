#### 步骤1：建立工程

```sh
#操作命令
scrapy startproject baiduStock
cd baiduStock
scrapy genspider stocks baidu.com
#修改spiders/stocks.py文件
```

#### 步骤2：编写Spider

```sh
配置stocks.py文件
修改对返回页面的处理
修改对新增url爬取请求的处理

#stocks.py参见源码
```

#### 步骤3：编写Pipelines

```sh
#配置pipelines.py文件
	定义对爬取项（Scraped Item）的处理类：BaidustocksInfoPipeline	#参见源码
#在settings.py中配置ITEM_PIPELINES选项
	ITEM_PIPELINES = {'baiduStocks.pipelines.BaidustocksInfoPipeline'}
```

#### 步骤4：执行爬虫

```sh
scrapy crawl stocks
```

#### 优化相关

`settings.py`文件

| 选项                           | 说明                                         |
| ------------------------------ | -------------------------------------------- |
| CONCURRENT_REQUESTS            | Downloader最大并发下载数量，默认32           |
| CONCURRENT_ITEMS               | Item Pipeline最大并发item处理数量，默认100   |
| CONCURRENT_REQUESTS_PER_DOMAIN | 每个目标域名最大的并发请求数量，默认8        |
| CONCURRENT_REQUESTS_PER_IP     | 每个目标ip最大的并发请求数量，默认0，非0有效 |

