import os, json

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
        pass

    def read(self, filename):
        f = open(filename, 'r')
        lines=f.read()
        f.close()
        return lines

    def write(self, dir, text):
        f = open(dir, 'w')
        f.write(text)
        f.close()

    def delete(self, filename):
        cmnd = ['/bin/rm', '-rf', filename]
        p = subprocess.call(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)

class AgentList:
    def __init__(self):
        self.filee = File()

    def get(self):
        message = "Unknow"
        data = None
        status = 500
        try:
            rsp = self.filee.read("/tmp/agent.json")
        except Exception as e:
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
            except:
                data = None
        else:
            message = "Data file not json fortmat"
        json_response = {"status": status, "message": message, "data": data}
        json_response = json.dumps(json_response)
        return json.loads(json_response)

    def seach_by_name(self, key):
        data = self.get()
        message = data["message"]
        status = data["status"]
        data = data["data"]
        origin_list = []
        for agent in data:
            if key in str(agent["name"]).lower():
                origin_list.append(agent)
        json_response = {"status": status, "message": message, "data": origin_list}
        json_response = json.dumps(json_response)
        return json.loads(json_response)

    def get_origin(self):
        return self.seach_by_name("origin")

    def get_4500(self):
        return self.seach_by_name("4500")

class Agent:
    def __init__(self, ip):
        self.al = AgentList()
        self.ip = ip
    def get(self):
        data = al.get()

al = AgentList()

print al.get_origin()