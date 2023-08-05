# coding:utf-8
# 程序配置项 声明日志输出类
# Modified by zhangzixiao
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

from MDCLogger.Tests.LoggerConfig import logger
from MDCLogger.JournalLogModel import JournalLog
from MDCLogger import MDCLoggerImpl


def do_some_work():
    logger.debug("这是debug日志==%s", "测试的内容")
    logger.trace("这是trace日志可以填充扩展属性在extra", extra={"key_name": "很重要的信息"})
    logger.warn("这是个warn日志")
    logger.error("这是个 error 日志")
    logger.info("抱歉 info日志已降级为debug日志", extra={"real_level": "INFO"})
    in_log = JournalLog("2020-09-15 17:26:27", "2020-09-15 17:26:36", "http:test.com", "post")
    logger.internal_log(json_data=in_log.json(), extra={"key_name": "内部流水中其他想打印到日志里的信息"})
    out_log = JournalLog("2020-09-15 17:26:27", "2020-09-15 17:26:36", "http:test.com", "post", dialog_type="out")
    logger.external_log(out_log.json(), extra={"key_name": "这里可以是外部流水中其他想扩展的内容"})


@MDCLoggerImpl.with_log_trace()
def support_parent_trace():
    logger.debug("这里已经不是最初的溯源id了==%s", "support_parent_trace")


@MDCLoggerImpl.with_log_trace(False)
def restart_trace():
    logger.debug("这里重新开始了溯源id==%s", "restart_trace")
    support_parent_trace()
    return "我已经脱离了最初的溯源新启动的id=%s" % MDCLoggerImpl.getTraceId()


@MDCLoggerImpl.with_log_trace(support_parent_trace=False)
def trace_test_start():
    logger.debug("这是溯源开始的地方，每次traceid都不会相同==%s", "trace_test_start")
    do_some_work()
    res = restart_trace()
    print(res)


from concurrent.futures import ThreadPoolExecutor
if __name__ == "__main__":
    logger.debug("这个地方和溯源无关，traceid还没有设置,接下来将开启20个线程，来验证单个线程溯源id是相同的")
    t = ThreadPoolExecutor()
    for i in range(20):
        t.submit(trace_test_start)
    logger.debug("溯源验证已结束了，trace已再trace_test_start结束时清除了")





