### <u>win11搭建flask站点</u>

#### 1. 环境搭建：

* 安装python环境（`python3.7`以上）

* 创建项目目录`flask-bl`

* 创建应用目录`flaskr`,并且编写项目工厂 `__init__.py`编写hello路由（参见项目代码）

* 控制台`cd`到`flsk-bl`目录，创建虚拟环境，命令如下：

  ```sh
  python -m venv env 		#目录下会创建一个env的目录，即虚拟环境目录
  ```

  ```sh
  env\Scripts\activate		#激活虚拟环境
  ```

  ```sh
  pip install flask			#安装flask
  ```

  ```sh
  flask --app flaskr run --debug		#调试模式启动项目
  ```

* 浏览器，输入`http://localhost:5000/hello`访问

#### 2. 引入H-ui前端框架（前后端不分离）

* 在flaskr目录下创建static目录，static下创建admin目录
* 将h-ui官网下载的H-ui框架的h-ui、h-ui.admin、lib目录拷贝至static/admin目录
* 在flaskr目录下创建templates目录，其下创建test目录，其下新建hello.html，引入h-ui相关样式
* 工厂文件`__init__.py`添加hello路由
* 访问，显示hello world

#### 3. 数据库

* 安装postgresql
* 编写建表sql（菜单，角色，管理员，其他业务表..)
* 在pgsql控制台，将项目根目录`sqlscripts/bl_admin.sql`的内容粘贴运行，完成管理员表的建立，及插入一条管理员数据
* 用户名：admin，密码：123456

#### 4. 编写管理后台（后台控制器统一在admin目录下）

* 编写登录相关模块，控制器为flaskr/admin/base.py
* 编写系统管理模块，控制器为flaskr/admin/sys.py
* python数据库驱动，操作pg数据库(参见相关文档)		#需要安装模块：pip install psycopg2

#### 5. 补充说明

* 日志配置 flask-bl/flaskr/log.py

* 数据库文件 flask-bl/flaskr/db.py

* sql脚本 flask-bl/sqlscripts目录下

* 日志log文件 flask-bl/logs目录下

* **关键词**：

  xss，csrf，缓冲溢出（长度限制）
  sql语句使用预编译写法
  异常处理 ，错误页，响应状态码，缓存

  错误通知，后台通知消息 或 邮箱通知 或微信推送 短信验证码

  国际化

* **注意**：浏览器localhost:5000访问，速度会比较慢，查看网络，发现静态文件每次加载都耗时比较慢
  改成127.0.0.1:5000访问，速度会变快

* 本地环境可通过批处理快速启动服务:(项目目录flask-bl下)

  ```sh
  runflask.bat		//双击启动
  ```

   ```sh
   runflask-debug.bat		//双击启动调试模式
   ```



### <u>vue3环境（用户端业务）</u>

* 使用element-plus编写用户端页面（pc端移动端适配）

* 编写接口与flask交互，前后端分离（token，storage，路由，状态管理，日志等）

  

### <u>打包部署</u>

* 一般部署流程是：
   	1. 开发完成后，使用 pip freeze > requirements.txt 命令将项目的库依赖导出（虚拟环境），作为代码的一部分
   	2. 将代码上传到服务器
   	3. 在服务器上创建一个虚拟环境
   	4. 激活虚拟环境，执行 pip install -r requirements.txt，安装项目依赖

* 版本，包依赖，等

* 服务器：uWSGI（或gunicorn），

* 热部署（原理及对业务的影响）：

  对于单个服务器，优雅地重新启动机制可能会有所帮助。它将启动新的进程来接受新的请求，并保持旧的进程直到旧的请求完成。
   Nginx已经在使用这个，请参见http://wiki.nginx.org/CommandLine#Stopping_or_Restarting_Nginx
   对于多个服务器，使用反向代理是一个很好的实践。示例结构如下所示，可以使用Nginx轻松构建：
   如果某些后端服务器发生故障，反向代理可以将请求发送到其他正常的服务器，并且不会影响用户。
   您可以定制负载平衡策略来进行细粒度控制。您还可以灵活地添加服务器以进行扩展，或者选择服务器进行故障排除或代码更新。

  

### <u>项目可安装化，构建发行文件</u>

* 项目根目录下需要如下描述文件：（可根据实际情况修改）
    `pyproject.toml`
    `MANIFEST.in`

* 当需要把应用部署到其他地方时，需要构建一个 wheel （ .whl ）文件。 构建工作需要安装和使用 build 工具（虚拟环境）。

  ```sh
  pip install build
  ```

  ```sh
  python -m build --wheel
  ```

  执行上面命令后，构建的文件为 dist/flaskr-1.0.0-py3-none-any.whl 。文件名由项目名 称、版本号和一些关于项目安装要求的标记组成，
  形如： {project name}-{version}-{python tag}-{abi tag}-{platform tag} 。

* 复制这个文件到另一台机器， 创建一个新的虚拟环境 ，然后用 pip 安 装这个文件。

  ```sh
  pip install flaskr-1.0.0-py3-none-any.whl
  ```

  pip 会安装项目和相关依赖。



### <u>其他</u>

* 搭建ngxin服务器
* 使用redis缓存
* 虚拟机安装linux服务器（debian）
  部署web
  git
* 数据库配置
* 购买云服务器，ip，域名，部署web
* 注册公司或者个体营业执照
  接入支付相关业务
* 其他功能
