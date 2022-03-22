import logging
from logging import handlers
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
Base_url = "http://user-p2p-test.itheima.net"
DB_URL = "user-p2p-test.itheima.net"
DB_username = "root"
DB_password = "Itcast_p2p_20191228"
DB_member = "czbk_member"
DB_finance = "czbk_finance"


#初始化日志配置
def init_log_config():
    #1、初始化日志对象
    logger = logging.getLogger()
    #2、设置日志级别
    logger.setLevel(logging.INFO)
    #3、创建控制台日志处理器
    sh = logging.StreamHandler()
    #3.1文件日志处理器
    # logfile = base_dir + "log" + os.sep + "p2p_log{}+log".format("%Y%M%D %H%M%S")
    logfile = base_dir + "\log" + os.sep + "p2p_log.log"
    fh = logging.handlers.TimedRotatingFileHandler(logfile, when='M', interval=5, backupCount=5, encoding='UTF-8')
    #4、设置日志格式，创建格式化器
    fmt = '%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s'
    formatter = logging.Formatter(fmt)
    #5、将格式化器设置到日志器中
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)
    #6、将日志处理器添加到日志对象
    logger.addHandler(sh)
    logger.addHandler(fh)