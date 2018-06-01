#!/usr/bin/python
import re
import logging
import logging.config
import logging.handlers
import os, sys, time, json
from optparse import OptionParser
from config import SYSTEM, SUPERVISORD
from utils import File
from supervisord import Supervisord
from rabbit import Rabbit

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

if __name__ == "__main__":
    # Parsing argurments
    parser = OptionParser()
    parser.add_option("-s", "-S", dest="ip", type="string",
                      help="Ip source EX: 225.1.1.1", metavar=' ')
    parser.add_option("-H", dest="host", type="string",
                      help="Thomson host", metavar=' ')
    parser.add_option("-j", "-J", dest="jid", type="string",
                      help="Job id", metavar=' ')
    parser.add_option("-n", "-N", dest="Name", type="string",
                      help="Name", metavar=' ')

    (options, args) = parser.parse_args()

    #Check argurments
    for option in ['ip']:
        if not getattr(options, option):
            message = 'Option %s not specified' % option
            logger.error(message)
            parser.print_help()
            sys.exit(1)

    ip = get_ip(options.ip)
    if not ip:
        message = "Invalid ip source input: %s"%(options.ip)
        print message
        logger.error(message)
        sys.exit(1)
    host = options.host
    if not host:
        message = "Invalid host: %s"%(options.host)
        print message
        logger.error(message)
        sys.exit(1)
    jid = options.jid
    if not jid:
        message = "Invalid job id: %s"%(options.jid)
        print message
        logger.error(message)
        sys.exit(1)
    """
    Process monitor source and return main
    """
    time.sleep(10)
    """
    clear supervisord job config
    """
    rb = Rabbit(SYSTEM["LOG_QUEUE"])
    rb.push("100")

