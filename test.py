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

log = """[{"sev": "Critical", "nid": 20, "host": "172.29.70.189", "opdate": 1527842173809, "cldate": 1527842173863, "lid": 5736985386316242, "jid": 31412, "res": "LAN100, DEST_IP 225.1.5.165, PORT 30120", "cat": "Communication", "jname": "Australia Plus-HTVC.Test", "desc": "Loss of TS synchro"}]"""

ta = ThomsonAuto()
ta.auto(log)
