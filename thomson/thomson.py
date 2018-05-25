import re
import json
import logging
from config import ERROR_LIST

class ThomsonError(object):
    """docstring for ThomsonError"""
    def __init__(self, log):
        self.log = log
        self.logger = logging.getLogger("thomson")
        
    def is_double_node(self):
        if not self.log:
            return None
        double_node_pattern = re.compile("\:\ \d{1,2}\ and\ \d{1,2}")
        double_node = re.findall(double_node_pattern, self.log)
        if double_node:
            return True
        return False

    def is_lost_source(self):
        if not self.log:
            return None
        if "Loss of TS synchro" in self.log:
            return True
        return False

    def is_no_video(self):
        if not self.log:
            return None
        if "No component:on video" in self.log:
            return True
        return False

    def is_no_audio(self):
        if not self.log:
            return None
        if "No component:on audio":
            return True
        return False

    def is_cceror(self):
        if not self.log:
            return None
        if "continuity counter" in self.log:
            return True
        return False

    def overflow(self):
        if not self.log:
            return None
        if "overflow" in self.log:
            return True
        return False

    def is_returned_main(self):
        if not self.log:
            return None
        if "Active input:main" in self.log:
            return True
        return False

    def get_error_code(self):
        error_code = 0
        if self.is_lost_source():
            error_code = 1
        elif self.is_double_node():
            error_code = 2
        human_creadeble_error = ERROR_LIST[error_code]
        if error_code != 0:
            self.logger.debug("error code: %d, error: %s, log: %s"%(error_code, human_creadeble_error, self.log))
        return error_code

