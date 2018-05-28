import os, sys, re
import json
import threading
import logging
import logging.config
import logging.handlers
from rabbit import PushUnicast, Rabbit
from thomson import ThomsonError, ThomsonLog
from config import SYSTEM, ERROR_LIST, ERROR_CODE_CHECK_ORIGIN_LIST, ERROR_CODE_CHECK_4500_LIST

with open("config/python_logging_configuration.json", 'r') as configuration_file:
    config_dict = json.load(configuration_file)
logging.config.dictConfig(config_dict)
# Create the Logger
logger = logging.getLogger("auto_thomson")

def set_schedule_auto(log):
    pass

def match_case(log):
    te = ThomsonError(log)
    error_code = te.get_error_code()
    logger.debug("-------------> Error code:%d, %s <-------------"%(error_code, ERROR_LIST[error_code]))
    tl = ThomsonLog()
    data = tl.conver_json_from_plain_text(log)
    """
    Check source on Monitor system
    """
    if error_code in ERROR_CODE_CHECK_ORIGIN_LIST:
        ip = tl.get_ip(data["res"])
        logger.info("Error code: %d, error: %s ,Check %s on ogigin group."%(error_code, ERROR_LIST[error_code],ip))
        pu = PushUnicast()
        pu.push_to_origin_group(ip)
    if error_code in ERROR_CODE_CHECK_4500_LIST:
        ip = tl.get_ip(data["res"])
        logger.info("Error code: %d, error: %s ,Check %s on 4500 group."%(error_code, ERROR_LIST[error_code],ip))
        pass
    """
    update data
    """
    return 0

def callback(ch, method, properties, body):
    print "------------->\n" + body + "\n<-------------"
    logger.info("received " + body)
    if not body:
        logger.warning("received " + body + "empty!")
        return 1
    t = threading.Thread(target=match_case,
                        args=(body,))
    t.start()

if __name__ == "__main__":
    rb = Rabbit(SYSTEM["LOG_QUEUE"])
    rb.connect()
    rb.channel.basic_consume(callback,
                          queue=rb.routing_key,
                          no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    rb.channel.start_consuming()