DBUtils
=======

DBUtils is a suite of tools providing solid, persistent and pooled connections
to a database that can be used in all kinds of multi-threaded environments
like Webware for Python or other web application servers. The suite supports
DB-API 2 compliant database interfaces and the classic PyGreSQL interface.

The current version of DBUtils supports Python versions 2.6, 2.7 and 3.4 - 3.7.

The DBUtils home page can be found here: https://cito.github.io/DBUtils/



# CDBUtils

CDBUtils is since [DBUtils 1.3](https://cito.github.io/DBUtils/)

The CDBUtils home page can be found here:https://gitee.com/ctec/CDBUtils/

基于DBUtils-1.3实现，扩展DBUtils中PooledDB.py， 实现定时清理连接池中多余的空闲连接，释放连接资源。

## 新增参数说明

1. test_on_borrow：在连接池中获取新连接时，是否检查连接可用性。取值 范围：True或False。默认值False:不检测。开启检测需要配合参数`“max_wait_time”`，检查连接可用性会稍微消耗一定性能，需视实际需要考虑是否开启。 

1. test_idle： 是否开启空闲连接检查，取值范围（True、False）默认True：检查。需要配合`“idle_check_time”`使用。设置为True时，会通过threading.Timer开启延迟线程定时  检查连接池中空闲连接，将池中多余`mincached` 的空闲连接断开并移除缓存池。

2. validation_sql：校验数据有效性使用的sql语句默认`“SELECT 1 FROM DUAL”`

3. idle_check_time： 空闲连接检测时间间隔，单位秒，默认60s，当`“idle_check_time”`>0时， `“test_idle”`配置有效。

4. validate_timeout：执行校验sql语句的最大超时时间秒，默认1s， 取值范围>0，当传入值小于等于0时将一直等待校验sql执行完成。

5. max_wait_time：在连接池中获取连接的最大等待时间（秒），默认5s。`“max_wait_time”`>0时

   ​				  `“test_on_borrow”`配置有效。获取新连接时，超过`max_wait_time`设置时间时会抛出`InvalidConnection` 或`PooledDBError`异常。

## 使用方法：

安装CDBUtils：

pip install CDBUtils

参考样例代码见：

1、CDBUtils\Examples\CheckedConnPoolExample.py

2、CDBUtils\Tests\TestValidatedPooledDB.py

示例如下：

```python
import threading
import sys
from CDBUtils.ValidatedPooledDB import PooledDB
import cx_Oracle


# TNS = cx_Oracle.makedsn("127.0.0.1", '1521',"orcl")
# TNS = 127.0.0.1:1521/orcl
TNS = "LOCALORCL"


pool = PooledDB(cx_Oracle,
                user="zhangzx",
                password="Pwdasc123",
                dsn=TNS,
                mincached=3,
                maxcached=20,
                blocking=True,
                test_on_borrow=True,
                test_idle = True,
                maxconnections=50,
                max_wait_time=10
                )


def test_fun(sql, params=[]):
    try:
        conn = pool.connection()
        cus = conn.cursor()
        print("test-sql"+sql)
        print("test-params" + str(params), "现在的连接数", pool._connections)
        result_db = cus.execute(sql, params)
        result = result_db.fetchall()
        return_result = list()
        if len(result) > 0:
            key_list = [key[0] for key in result_db.description]
            for value in result:
                return_result.append(dict(zip(key_list, value)))
        return return_result
    except Exception as e:
        raise e
    finally:
        cus.close()


if __name__ == '__main__':
    sql = """select username,count(username) as u_size from v$session where 
    PROGRAM='python.exe' and username is not null  group by username"""
    params = []
    for i in range(10):
        print("test_resut=%s" % test_fun(sql, params))

```
# 目录说明：
```
CDBUtils
│  .gitattributes               .............................................   git文件的属性描述性说明
│  .gitignore                   .............................................   .git同步时忽略的文件说明
│  .travis.yml                  .............................................   Travis CI(Github持续集成工具) 配置文件
│  .pylintrc                    .............................................   pylint检查python代码质量输出的文件
│  LICENSE                      .............................................   开源协议说明
│  MANIFEST.in                  .............................................   打包上传pypi时必须的配置文件
│  README.md                    .............................................   项目说明
│  README.rst                   .............................................   用于在pypi仓库中,项目首页显示的说明
│  Release.md                   .............................................   发布新版本时的操作说明
│  buildhtml.py                 .............................................   生成docsRelNotes-xx.html
│  setversion.py                .............................................   更新项目版本用
│  setup.py                     .............................................   打包发布新版本到pypi时运行的文件
│  tox.ini                       ............................................   自动测试配置文件
└─CDBUtils                      ............................................   主程序目录
    ├─Docs                      ............................................   api说明文件目录
    ├─Examples                  ............................................   样例代码
    ├─Tests                     ............................................   测试代码
    ├─__init__.py               ............................................   CDBUtils package
    ├─Properties.py             ............................................   配置性文件
    └─ValidatedPooledDB.py      ............................................   扩展DBUTils.PooledDB针对检查连接池防空闲的实现
     
```
