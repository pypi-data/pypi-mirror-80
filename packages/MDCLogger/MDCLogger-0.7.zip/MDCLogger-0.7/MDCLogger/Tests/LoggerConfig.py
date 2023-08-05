# coding:utf-8
# 程序配置项 声明日志输出类
# Modified by zhangzixiao

import platform
from MDCLogger import LoggerPrintImpl
# 需要禁用debug输出,并需要重置handle的第三方依赖模块
# 设置后会将对应依赖包输出的日志，输出到error级别日志文件中
reset_error_logs = ["kafka", "tornado.access", "tornado.application", "tornado.general"]
APP_NAME = "demo"

LOG_BASE_PATH = ""
if platform.system() == 'Windows':
    LOG_BASE_PATH = r'E:/LOG/JOB/%s' % APP_NAME
else:
    LOG_BASE_PATH = '/opt/logs/%s' % APP_NAME


logger = LoggerPrintImpl.get_logger(APP_NAME, True, reset_error_logs, LOG_BASE_PATH)