import re
import json
import logging
from config import ERROR_LIST

class ThomsonError(object):
    """docstring for ThomsonError"""
    def __init__(self, log):
        self.log = log
        self.logger = logging.getLogger("thomson")
        self.unknow_log_logger = logging.getLogger("unknow_log")
        
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
        if "Stream discontinuity:continuity counter" in self.log:
            return True
        return False

    def is_overflow(self):
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

    def is_active_backup(self):
        if not self.log:
            return None
        if "Active input:backup" in self.log:
            return True
        return False

    def is_NTP(self):
        if not self.log:
            return None
        if "UTC time adjustment" in self.log:
            return True
        return False

    def get_error_code(self):
        error_code = 0
        if self.is_lost_source():
            error_code = 1
        elif self.is_double_node():
            error_code = 2
        elif self.is_no_video():
            error_code = 3
        elif self.is_no_audio():
            error_code = 4
        elif self.is_cceror():
            error_code = 5
        elif self.is_overflow():
            error_code = 6
        elif self.is_returned_main():
            error_code = 7
        elif self.is_active_backup():
            error_code = 8
        elif self.is_NTP():
            error_code = 9
        else:
            self.unknow_log_logger.warning(self.log)
        human_creadeble_error = ERROR_LIST[error_code]
        if error_code == 1 or error_code == 2:
            self.logger.debug("error code: %d, error: %s, log: %s"%(error_code, human_creadeble_error, self.log))
            #print "------------->\n" + "error code: %d, error: %s"%(error_code, human_creadeble_error) + "\n<-------------"
        return error_code

class ThomsonLog(object):
    """docstring for ThomsonLog"""
    def __init__(self):
        self.logger = logging.getLogger("thomson")
        self.unknow_log_logger = logging.getLogger("unknow_log")

    def conver_json_from_plain_text(self, log):
        data = None
        try:
            json_data = json.loads(log)
            if len(json_data) > 1:
                self.unknow_log_logger.error("Error: len=%d>1, log: %s"%(len(json_data), log))
            data = json_data[0]
        except Exception as e:
            log_object = log[log.find("[") : log.find("]")+1]
            try:
                json_data = json.loads(log_object)
                if len(json_data) > 1:
                    self.unknow_log_logger.error("Error: len=%d>1, log: %s"%(len(json_data), log))
                data = json_data[0]
            except Exception as e:
                logger.error("Error: %s, data: %s"%(str(e), log))
        return data

    def get_ip(self, res):
        ip = None
        try:
            ip_pattern=re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
            ip_list = re.findall(ip_pattern, res)
            if not len(ip_list):
                self.logger.warning("Can not find ip from %s"%(res))
            else:
                ip = ip_list[0]
        except Exception as e:
            self.logger.error("Error: %s, log: %s"%(str(e), res))
        return ip

class ThomsonAuto(object):
    """docstring for ThomsonAuto"""
    def __init__(self):
        self.logger = logging.getLogger("thomson")
        self.unknow_log_logger = logging.getLogger("unknow_log")

        
