#!/usr/bin/python
import re
import logging
import logging.config
import logging.handlers
import sys, time, json
from optparse import OptionParser
from services import AsRequiredCheck
from BLL.profile import Profile as ProfileBLL
from supervisord import Supervisord
from config import SYSTEM

def get_ip(source):
    ip_pattern=re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    ip = re.findall(ip_pattern, source)
    ip = ip[0]
    return ip


if __name__ == "__main__":
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
