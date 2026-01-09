
'''说明
Flask扩展是一个Python模块，它向Flask应用程序添加了特定类型的支持。
Flask Extension Registry（Flask扩展注册表）是一个可用的扩展目录。
可以通过pip实用程序下载所需的扩展名。
Flask常用扩展包：
Flask-SQLalchemy：操作数据库；
Flask-script：插入脚本；
Flask-migrate：管理迁移数据库；
Flask-Session：Session存储方式指定；
Flask-WTF：表单；
Flask-Mail：邮件；
Flask-Bable：提供国际化和本地化支持，翻译；
Flask-Login：认证用户状态；
Flask-OpenID：认证；
Flask-RESTful：开发REST API的工具；
Flask-Bootstrap：集成前端Twitter Bootstrap框架；
Flask-Moment：本地化日期和时间；
Flask-Admin：简单而可扩展的管理接口的框架

每种类型的扩展通常提供有关其用法的大量文档。
由于扩展是一个Python模块，因此需要导入它才能使用它。
Flask 的扩展通常命名为“ Flask-Foo ”或者“ Foo-Flask ” 。可以在 PyPI 搜索 标记为 Framework :: Flask 扩展包。
'''

from flask import Flask
from flask_foo import Foo		#需安装	,暂且不知道这个扩展是干嘛的	（需要查看具体扩展的文档）

foo = Foo()

app = Flask(__name__)
app.config.update(
    FOO_BAR='baz',
    FOO_SPAM='eggs',
)

foo.init_app(app)