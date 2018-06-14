import re
import json
import logging
from thomsonapi import Job, JobDetail
from config import THOMSON_HOST
from supervisord import Supervisord, ScheduleAuto
from rabbit import PushUnicast, Rabbit
from config import SYSTEM, ERROR_LIST, ERROR_CODE_CHECK_ORIGIN_LIST, ERROR_CODE_CHECK_4500_LIST, ERROR_CODE_AUTO_RETURN_MAIN

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
        if "No component:on audio" in self.log:
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

    def is_switch_backup(self):
        if not self.log:
            return None
        if "Active input switch:backup is active" in self.log:
            return True
        return False

    def get_error_code(self):
        error_code = 0
        if self.is_lost_source():
            error_code = 1
        elif self.is_active_backup():
            error_code = 2
        elif self.is_returned_main():
            error_code = 3
        elif self.is_double_node():
            error_code = 4
        elif self.is_no_video():
            error_code = 5
        elif self.is_no_audio():
            error_code = 6
        elif self.is_cceror():
            error_code = 7
        elif self.is_overflow():
            error_code = 8
        elif self.is_NTP():
            error_code = 9
        elif self.is_switch_backup():
            error_code = 10
        else:
            self.unknow_log_logger.warning(self.log)
        human_creadeble_error = ERROR_LIST[error_code]
        if error_code == 1 or error_code == 2 or error_code == 4:
            self.logger.debug("error code: %d, error: %s, log: %s"%(error_code, human_creadeble_error, self.log))
            #print "------------->\n" + "error code: %d, error: %s"%(error_code, human_creadeble_error) + "\n<-------------"
        return error_code

class ThomsonLog(object):
    """docstring for ThomsonLog"""
    def __init__(self):
        self.logger = logging.getLogger("thomson")
        self.unknow_log_logger = logging.getLogger("unknow_log")

    def conver_json_from_plain_text(self, log):
        log = str(log)
        data = None
        try:
            json_data = json.loads(log)
            if len(json_data) > 1:
                self.unknow_log_logger.error("Error: len=%d>1, log: %s"%(len(json_data), log))
            data = json_data[0]
        except Exception as e:
            log_object = log[log.find("{") : log.find("}")+1]
            try:
                json_data = json.loads(log_object)
                if len(json_data) > 1:
                    self.unknow_log_logger.error("Error: len=%d>1, log: %s"%(len(json_data), log))
                data = json_data
            except Exception as e:
                self.logger.error("Error: %s, data: %s"%(str(e), log))
        return data

    def get_ip(self, res):
        ip = None
        try:
            ip_pattern=re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
            ip_list = re.findall(ip_pattern, res)
            if not len(ip_list):
                self.logger.debug("Can not find ip from %s"%(res))
            else:
                ip = ip_list[0]
        except Exception as e:
            self.logger.error("Error: %s, log: %s"%(str(e), res))
        return ip

    def get_job_name(self, log_data):
        name = ""
        if not type(log_data).__name__ in ["list", "dict"]:
            json_data = self.conver_json_from_plain_text(log_data)
        else:
            json_data = log_data
        if not json_data:
            self.logger.error(log_data)
            return 1
        name = json_data["host"] + "_" + json_data["jname"]
        name = name.replace(" ", "")
        name = name.replace("@", "")
        name = name.replace("#", "")
        name = name.replace("/", "")
        name = name.replace("*", "")
        name = name.replace("&", "")
        name = name.replace("%", "")
        name = name.replace("$", "")
        return name

    def get_ip_out_list(self, log_data):
        ip_out_list = []
        if not type(log_data).__name__ in ["list", "dict"]:
            log_data = self.conver_json_from_plain_text(log_data)
        jid = int(log_data["jid"])
        target_host = log_data["host"]
        account = None
        for i in THOMSON_HOST:
            if THOMSON_HOST[i]["host"] == target_host:
                account = THOMSON_HOST[i]
                break
        if not account:
            print "Host: %s not found!"%(target_host)
            return 1
        jd = JobDetail(account["host"], account["user"], account["passwd"], jid)
        job_data = jd.get_param()
        job_data = json.loads(job_data)
        ip_out_list = []
        try:
            param_list = job_data[0]["params"]
            for param in param_list:
                name = str(param["name"]).upper()
                if "IP OUT" in name or "IPOUT" in name or "IP  OUT" in name:
                    ip_out = param["value"]
                    ip_out_list.append(ip_out[:ip_out.find("#")])
        except Exception as e:
            self.logger.error(sre(e))
        return ip_out_list

class ThomsonAuto(object):
    """docstring for ThomsonAuto"""
    def __init__(self):
        self.logger = logging.getLogger("thomson")
        self.unknow_log_logger = logging.getLogger("unknow_log")

    """
    Check source on Monitor system
    """
    def check_source(self, data, error_code):
        tl = ThomsonLog()
        if error_code in ERROR_CODE_CHECK_ORIGIN_LIST:
            ip = tl.get_ip(data["res"])
            self.logger.info("Error code: %d, error: %s ,Check %s on ogigin group."%(error_code, ERROR_LIST[error_code],ip))
            pu = PushUnicast()
            pu.push_to_origin_group(ip)
        if error_code in ERROR_CODE_CHECK_4500_LIST:
            ip_out_list = tl.get_ip_out_list(data)
            for ip_out in ip_out_list:
                pu = PushUnicast()
                pu.push_to_4500_group(ip_out)
        return 0

    """
    Monitor source and auto restart job on thomson
     - Check active is on --> set schedule auto on supervisord
    """
    def return_main(self, data, error_code):
        if error_code not in ERROR_CODE_AUTO_RETURN_MAIN:
            self.logger.debug("Error code = %d --> not monitor or auto. data: %s"%(error_code, str(data)))
            return 0
        if data["cldate"]:
            self.logger.debug("Close log --> not monitor or auto")
            return 0
        tl = ThomsonLog()
        ip = tl.get_ip(data["res"])
        name = tl.get_job_name(data)
        self.logger.info("Error code: %d, error: %s ,Monitor source %s %s and auto restart job on thomson."%(error_code, ERROR_LIST[error_code],name,ip))
        sa = ScheduleAuto()
        sa.set_supervisord_schedule(host=data["host"], jid=int(data["jid"]), name=name, ip=ip)
        spvs = Supervisord()
        spvs.sa.start_job(name)
        return 0


    def set_auto(self, log):
        te = ThomsonError(log)
        error_code = te.get_error_code()
        self.logger.debug("-------------> Error code:%d, %s <-------------"%(error_code, ERROR_LIST[error_code]))
        tl = ThomsonLog()
        data = tl.conver_json_from_plain_text(log)
        self.check_source(data, error_code)
        self.return_main(data, error_code)

