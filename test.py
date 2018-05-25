import os, sys, re
import json
import threading
import logging
import logging.config
import logging.handlers
from rabbit import PushUnicast, Rabbit
from thomson import ThomsonError
from config import SYSTEM, ERROR_LIST

with open("config/python_logging_configuration.json", 'r') as configuration_file:
    config_dict = json.load(configuration_file)
logging.config.dictConfig(config_dict)
# Create the Logger
logger = logging.getLogger("auto_thomson")

def match_case(log):
    te = ThomsonError(log)
    error_code = te.get_error_code()    

def callback(ch, method, properties, body):
    print "-------------> " + body + " <-------------"
    logger.info("received " + body)
    if not body:
        logger.warning("received " + body + "empty!")
        return 1
    t = threading.Thread(target=match_case,
                        args=(body,))
    t.start()
    match_case(log=body)

if __name__ == "__main__":
    rb = Rabbit(SYSTEM["LOG_QUEUE"])
    rb.connect()
    rb.channel.basic_consume(callback,
                          queue=rb.routing_key,
                          no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    rb.channel.start_consuming()