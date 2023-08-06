CDBUtils

CDBUtils is one extension copy from DBUtils 2.0

The CDBUtils home page can be found here:https://gitee.com/ctec/CDBUtils/

*Extension parameter descriptions:*


- test_on_borrow: check availability of the connection fetched from the pool (True = check,False = default = never check)
- test_idle: Check connection availability on idle(True = check,False = default = never check)
- validation_sql: the sql for validate the connection (default is "SELECT 1 FROM DUAL")
- idle_check_time: the seconds for Check and remove the idle connection interval, it will be start one Thread to check the idle connection in the pool, whenever "idleCheckTime" greater than 0 and "testIdle" is True,default is 60 seconds.
- validate_timeout: the max seconds to execute the validation Sql,default is 1. if "validateTimeOut" Less than 1, it will  Wait until to return the result
- max_wait_time: the max wait time for fetch one connection from the pool, if "maxWaitTime" greater than 0 ,it will be start a lock for the function "connection " with in the time, and throw one exception when the timeout, default is 5s
