import json
import threading
import logging
import logging.config
import logging.handlers
from rabbit import Rabbit
from thomson import ThomsonAuto
from config import SYSTEM

with open("config/python_logging_configuration.json", 'r') as configuration_file:
    config_dict = json.load(configuration_file)
logging.config.dictConfig(config_dict)
# Create the Logger
logger = logging.getLogger("auto_thomson")


def callback(ch, method, properties, body):
    print "------------->\n" + body + "\n<-------------"
    logger.info("received " + body)
    if not body:
        logger.warning("received " + body + "empty!")
        return 1
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