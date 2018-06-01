import re
import json
import threading
import logging
import logging.config
import logging.handlers
from rabbit import Rabbit
from thomson import ThomsonAuto
from config import SYSTEM
from supervisord import Supervisord

with open("config/python_logging_configuration.json", 'r') as configuration_file:
    config_dict = json.load(configuration_file)
logging.config.dictConfig(config_dict)
# Create the Logger
logger = logging.getLogger("auto_thomson")

def get_ip(source):
    ip_pattern=re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    ip = re.findall(ip_pattern, source)
    try:
        ip = ip[0]
    except Exception as e:
        ip = None
    return ip

def callback(ch, method, properties, body):
    print "------------->\n" + body + "\n<-------------"
    logger.info("received " + body)
    if not body:
        logger.warning("received " + body + "empty!")
        return 1
    try:
        spvs_code = int(body)
        if spvs_code == 100:
            logger.info("Supervisord error code = %d --> remove supervisord EXITED job."%(spvs_code))
            spvs = Supervisord()
            t = threading.Thread(target=spvs.remove_exited_job)
            t.start()
    except:
        ta = ThomsonAuto()
        t = threading.Thread(target=ta.auto,
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