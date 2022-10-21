# FlaskExample Web Framework ![CI status](https://img.shields.io/badge/build-passing-brightgreen.svg)

基于Flask Web框架的微服务骨架，后续的应用开发需要遵循此框架的示例规范

**Code structure：**

```text
├── bin                      # 可执行的脚本程序
├── conf                     # 应用配置
│   ├── uwsgi.ini            # uWSGI 网关配置
│   └── config.py            # 通用配置
├── docs                     # 应用相关文档
│   ├── example                  # API 接口
│   │   │   └── user_2022-10-21.py  # user 接口文档
│   │   │   └── version.py  # user 接口版本
└── apis                  # API 文档
│   ├── example                  # API 接口
│   │   │   └── __init__.py  # 注册路由和蓝图
│   │   │   └── user.py  # user handler
│   │   └── __init__.py      # API配置
│   ├── models               # 数据库模型
│   ├── schemas              # schema 数据结构
│   ├── tasks                # 任务目录
│   └── __init__.py          # 初始化应用
├── common                   # 公共和辅助函数库
|   └── consul               # consul 类库
│   └── healthcheck.py       # 服务健康检测
│   └── helpers.py           # 帮助类
│   └── log_handler.py       # 日志自定义模块
│   └── mixins.py            # 上下文管理
│   └── utils.py             # 通用工具类
├── migrations               # 数据库迁移脚本
└── tests                    # 单元测试集合
│   ├── example                  # API 接口单元测试
│   │   │   └── user_test.py  # user 接口单元测试
├── middleware                   # 中间件
│   └── global_middleware.py          # 中间件使用示例
```

## Quick start

- 说明: 该项目示例镜像已经push到dockerhub.com[镜像地址](https://hub.docker.com/repository/docker/lifangjunone/flask_example)
   + 运行项目:
      - ```shell
        sudo docker-compose -f deploy/docker-compose.yaml up
        ```
   + 浏览器访问 http://{ip/domain}:8000/api/example_api/version
      - 返回示例: 
          - ```json
              {
                "api_version": "v1",
                "production": "FlaskExample",
                "app_version": "",
                "application": "FlaskExample",
                "platform": "Linux-5.10.18-amd64-desktop-x86_64-with-glibc2.31"
               }
             ```




## Run in local
- pip install -r requirements.txt
- 运行项目
- 浏览器访问： http://ip:port/api/v1/version
- 返回值：
  + ```json
    {
    "api_version": "v1",
    "production": "MicroservicePlatform",
    "app_version": "v0.0.1",
    "application": "flask-example",
    "platform": "Linux-5.10.18-amd64-desktop-x86_64-with-Deepin-20.2.1-apricot"
    }
    ```
## Install

### 环境要求
* Linux
* Python 3.5.2 and up


## Usage
### 环境变量
本服务应用的大部分配置都是通过环境变量和 Consul-K/V 来进行配置的，本地调试启动需要自行设定如下环境变量：

- HOST_ADAPTER # 指定网卡适配器，用于服务启动 IP 绑定
- ENVIRONMENT # 指定服务当前运行的环境（production、development、testing）
- CONSUL_HOST # Consul 服务注册中心的 IP 地址

### CLI
`$ python manage.py runserver`  
`$ python manage.py create_db`  
`$ python manage.py db`  
`$ python manage.py shell`  
`$ celery worker -A manage.celery --loglevel=debug`


`$ make install`         # 安装依赖模块（运行必须优先执行）  
`$ make test`            # 单元测试(必须先启动服务)  
`$ make test-html`       # 生成单元测试报告  
`$ make coverage-report` # 生成覆盖率报告  
`$ make docker-doc`      # 文档镜像构建  

### Docker
**主程序：**
```bash
$  sudo docker build -f ./deploy/Dockerfile  -t flask_example:v1.0.0 .
$ docker run --rm -p 8000:8000  -e "ENVIRONMENT=testing"   flask_example:v1.0.0
```

**redis：**
```bash
$ docker run --rm -p 6379:6379 --name my-redis redis
```

### Interface test
```
$ http http://127.0.0.1:8000/api/example_api/version

# 异步任务
$ http http://127.0.0.1:8000/api/example_api/task/add
```

### Database migration
**创建数据库:**
- `create database if not exists 'db_name' default character set utf8 collate utf8_general_ci;`

**数据库迁移的目的：**

1. 初始化并创建数据库和数据库表
2. 对数据库进行升级或回滚，保存不同数据库的版本
3. 修改数据库表，同时保留原始数据

- `$ python manage.py db init`    # 创建迁移仓库 migrations
- `$ python manage.py db migrate -m "initial migration"` # 创建迁移脚本
- `$ python manage.py prepare_migrate"` # 修改迁移脚本 过滤删除表的命令
- `$ python manage.py db upgrade` # 更新数据库
- `$ python manage.py db history` # 获取 History ID
- `$ python manage.py db downgrade <history_id>` # 回滚到某个 history 版本

**自动检测配置：**
```python
def create_app():
    ...
    # compare_type 设置为 True 会开启检测字段数据变化的功能，比如：字段长度的变更。注意：SQLite 还不支持 drop column 操作。
    # migrate.init_app(app, db, compare_type=True)
    ...
```

**参考资料：**
- [自动生成迁移检测机制](http://alembic.zzzcomputing.com/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect)
- [sqlite-alter-table](http://www.sqlitetutorial.net/sqlite-alter-table/)

## Development and debugging
```bash
$ virtualenv idl-venv
$ . idl-venv/bin/activate
$ make install
$ python manage.py runserver
```

# Unit test
## pytest
**测试样例发现规则:**  
- 测试文件以 test_ 开头
- 测试类以 Test 开头，并且不能带有 `__init__` 方法
- 测试函数以 test_ 开头
- 断言使用基本的 assert 即可

### 常用命令
- `py.test -s -v` 显示运行的函数和内部的打印信息
- `py.test -s -v --html=./test_report.html` 生成 HTML 报告
- `py.test [file_or_dir] [file_or_dir] [...]` 指定一个或多个文件/目录测试

### setup和teardown
- 模块级（setup_module/teardown_module）开始于模块始末
- 类级（setup_class/teardown_class）开始于类的始末
- 类里面的（setup/teardown）（运行在调用函数的前后）
- 功能级（setup_function/teardown_function）开始于功能函数始末（不在类中）
- 方法级（setup_method/teardown_method）开始于方法始末（在类中）

### fixture scope
使用 @pytest.fixture(scope='module') 来定义框架，scope 的范围参数有以下几种

- function   每一个用例都执行
- class        每个类执行
- module     每个模块执行(函数形式的用例)
- session     每个 session 只运行一次，在自动化测试时，登录步骤可以使用该 session


## celery run
`celery -A  manage.celery worker --loglevel=debug`
- [前台运行] celery worker -A manage.celery --loglevel=debug
- [后台运行] celery multi start w1 -A manage.celery --loglevel=debug


## Deploy service
### 启动后端服务

```shell script
sh ./deploy/start_server.sh
```





