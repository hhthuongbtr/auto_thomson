#!/usr/bin/python
import re
import logging
import logging.config
import logging.handlers
import os, sys, time, json
from optparse import OptionParser
from config import SYSTEM, SUPERVISORD
from utils import File

with open("config/python_logging_configuration.json", 'r') as configuration_file:
    config_dict = json.load(configuration_file)
logging.config.dictConfig(config_dict)
# Create the Logger
logger = logging.getLogger("auto_thomson")

def get_ip(source):
    ip_pattern=re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    ip = re.findall(ip_pattern, source)
    ip = ip[0]
    return ip

if __name__ == "__main__":
    time.sleep(600)
    # Parsing argurments
    parser = OptionParser()
    parser.add_option("-s", "-S", dest="ip", type="string",
                      help="ip ip multicast(Ex: 225.1.1.1).", metavar=' ')

    (options, args) = parser.parse_args()

    #Check argurments
    if not getattr(options, 'ip'):
        print 'Option %s not specified'%(ip)
        self.logger.error('Option %s not specified'%(ip))
        parser.print_help()
    else:
        sa = SyncAlam()
        ip = get_ip_from_ip_multicast(options.ip)
        profile = sa.update_data(ip)
        if not profile:
            raise ValueError('could not find %s' % (options.ip))
        else:
            sa.check(profile)
