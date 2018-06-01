import os, json, time
import logging
import subprocess
from subprocess import call


def is_json(text):
    rt = False
    try:
        json.loads(text)
        rt = True
    except:
        pass
    return rt

class File:
    def __init__(self):
        self.logger = logging.getLogger("utils")

    def read(self, filename):
        lines = None
        try:
            f = open(filename, 'r')
            lines=f.read()
            f.close()
        except Exception as e:
            self.logger.error("%s"%(str(e)))
        return lines

    def write(self, dir, text):
        try:
            f = open(dir, 'w')
            f.write(text)
            f.close()
        except Exception as e:
            self.logger.error("%s"%(str(e)))
            return 1
        return 0

    def delete(self, filename):
        self.logger.debug("File.delete: %s"%(filename))
        cmnd = ['/bin/rm', '-rf', filename]
        p = subprocess.call(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)

class AgentList:
    def __init__(self):
        self.logger = logging.getLogger("utils")
        self.filee = File()

    def get(self):
        message = "Unknow"
        data = None
        status = 500
        try:
            rsp = self.filee.read("/tmp/agent.json")
        except Exception as e:
            self.logger.error("%s"%(str(e)))
            message = str(e)
            data = None
            status = 500
            json_response = {"status": status, "message": message, "data": data}
            json_response = json.dumps(json_response)
            return json.loads(json_response)
        if is_json(rsp):
            status = 200
            message = "OK"
            try:
                data = json.loads(rsp)
                data = data['data']
            except Exception as e:
                self.logger.error("%s"%(str(e)))
                data = None
        else:
            message = "Data file not json fortmat"
            self.logger.error("%s"%(message))
        json_response = {"status": status, "message": message, "data": data}
        json_response = json.dumps(json_response)
        return json.loads(json_response)

    def seach_by_name(self, key):
        message = ""
        status = 500
        data = None
        origin_list = []
        try:
            data = self.get()
            message = data["message"]
            status = data["status"]
            data = data["data"]
            for agent in data:
                if key in str(agent["name"]).lower():
                    origin_list.append(agent)
        except Exception as e:
            self.logger.error("Function: AgentList.seach_by_name '%s'"%(str(e)))
        json_response = {"status": status, "message": message, "data": origin_list}
        json_response = json.dumps(json_response)
        return json.loads(json_response)

    def get_origin(self):
        self.logger.info("Get origin agent list.")
        return self.seach_by_name("origin")

    def get_4500(self):
        self.logger.info("Get 4500 agent list.")
        return self.seach_by_name("4500")

    def get_ott(self):
        self.logger.info("Get ott agent list.")
        return self.seach_by_name("ott")

class Agent:
    def __init__(self, ip):
        self.logger = logging.getLogger("utils")
        self.al = AgentList()
        self.ip = ip

    def seach_by_ip(self, ip):
        message = ""
        status = 500
        data = None
        origin_list = []
        try:
            data = self.al.get()
            message = data["message"]
            status = data["status"]
            data = data["data"]
            for agent in data:
                if ip == agent["ip"].strip():
                    origin_list.append(agent)
        except Exception as e:
            self.logger.error("Function: Agent.seach_by_ip '%s'"%(str(e)))
        json_response = {"status": status, "message": message, "data": origin_list}
        json_response = json.dumps(json_response)
        return json.loads(json_response)

    def get(self):
        self.logger.info("Get agent by ip: %s."%(self.ip))
        return self.seach_by_ip(self.ip)
