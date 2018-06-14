import xmlrpclib
import os, time
import logging
import threading
from config import SUPERVISORD, SYSTEM
from supervisordapi import SupervisordApi
from utils import File

class Supervisord:
    def __init__(self):
        self.logger = logging.getLogger("supervisord")
        self.sa = SupervisordApi(SUPERVISORD["HOST"], SUPERVISORD["PORT"])

    def delete_job(self, name):
        self.logger.debug("Supervisord: delete job %s Stop_job --> remove_process_group --> delete_config_file --> reload_config"%(name))
        filee = File()
        conf_dir = SUPERVISORD["CONF_DIR"] + "/" + name + SUPERVISORD["CONF_EXTENSION"]
        filee.delete(conf_dir)
        time.sleep(1)
        self.sa.stop_process(name)
        self.sa.remove_process_group(name)
        return 0

    def remove_exited_job(self):
        job_list = self.sa.get_all_process_info()
        if not job_list:
            self.logger.warning("Error: %s"%(str(job_list)))
            return 1
        if not type(job_list).__name__  == "list":
            self.logger.warning("Error, data type is not list: %s"%(str(job_list)))
            return 1
        for job in job_list:
            if job["state"] == 100:
                t = threading.Thread(target=self.delete_job,
                    args=(job["name"],)
                )
                t.start()
        time.sleep(3)
        return 0

class ScheduleAuto(object):
    """docstring for ScheduleAuto"""
    def __init__(self):
        self.logger = logging.getLogger("supervisord")

    def create_config_file(self,host=None, jid=None, name=None, ip=None):
        try:
            filee = File()
            supervisord_config_template = filee.read(SUPERVISORD["CONF_TEMPLATE_DIR"])
        except Exception as e:
            self.logger.error(str(e))
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        supervisord_config = supervisord_config_template.replace('{name}', name)
        supervisord_config = supervisord_config.replace('{base_dir}', base_dir)
        supervisord_config = supervisord_config.replace('{host}', host)
        supervisord_config = supervisord_config.replace('{jid}', str(jid))
        supervisord_config = supervisord_config.replace('{ip}', ip)
        return supervisord_config
    
    def set_supervisord_schedule(self,host=None, jid=None, name=None, ip=None):
        if not (host and jid and name and ip):
            print 'Missing options: host=%s, jid=%d, name=%s, ip=%s'%(host, jid, name, ip)
            self.logger.warning('Missing options: host=%s, jid=%d, name=%s, ip=%s'%(host, jid, name, ip))
        supervisord_config = self.create_config_file(host=host, jid=jid, name=name, ip=ip)
        full_dir = SUPERVISORD["CONF_DIR"] + '/' + name + SUPERVISORD["CONF_EXTENSION"]
        filee = File()
        print filee.write(dir = full_dir, text = supervisord_config)
        self.logger.info("config file: %s, content: %s"%(full_dir, supervisord_config))
        return 0
