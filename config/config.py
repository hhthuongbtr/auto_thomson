SYSTEM = {
    "list_queue_groups":{
            "ORIGIN": "origin",
            "4500": "4500",
            "PROBE": "probe"
        },
    "LOG_QUEUE": "thomson_log",
    "RUNNING_BACKUP_QUEUE" : "running_backup",
    "auto": {
        "DOUBLE_NODE": True,
        "RETURN_MAIN": True
        },
    "REPEAT_LIMIT": 10
    }

API = {
    "master": {
        "URL": "42.117.9.100", 
        "PASSWORD": "iptv13579", 
        "PORT": 8888, 
        "USER": "monitor"
        },
    "slave": {
        "ACTIVE": False, 
        "URL": "42.117.9.99", 
        "PASSWORD": "iptv13579", 
        "PORT": 8888, 
        "USER": "monitor"
        }
    }

DATABASE = {
    "master": {
        "NAME": "monitor", 
        "HOST": "localhost", 
        "USER": "root", 
        "ACTIVE": True, 
        "PASSWORD": "root", 
        "PORT": 3306
        },
    "slave": {
        "NAME": "monitor", 
        "HOST": "localhost", 
        "USER": "root", 
        "ACTIVE": False, 
        "PASSWORD": "root", 
        "PORT": 3306
        }
    }

SUPERVISORD={
    "HOST"                  : "localhost",
    "PORT"                  : 9001,
    "CONF_DIR"              : "/etc/supervisord/conf.d",
    "CONTROL_DIR"           : "/usr/bin/supervisorctl",
    "CONF_TEMPLATE_DIR"     : "config/supervisord.template",
    "CONF_EXTENSION"        : ".ini"
    }

SOCKET = {
    "HOST"                  :"42.117.9.99",
    "PORT"                  :5672,
    "USER"                  :"monitor",
    "PASSWD"                :"iptv13579"
    }

ERROR_LIST=[
    "Unknow",           #0 
    "lost source",      #1
    "active backup",    #2
    "active main",      #3
    "double nodes",     #4
    "no video",         #5
    "no audio",         #6
    "cceror",           #7
    "output overflow",  #8
    "NTP",              #9
    "switch backup",    #10
    "Modify",           #11
    "PID",              #12
    "ServiceId",        #13
    "stop job",         #14
    "start job"         #15
]

ERROR_CODE_CHECK_ORIGIN_LIST = [1, 2]
ERROR_CODE_CHECK_4500_LIST = [1,2,3,4]
ERROR_CODE_AUTO_RETURN_MAIN = [2]
ERROR_CODE_AUTO_DOUBLE_NODE = [4]

THOMSON_HOST={
    "thomson-hcm":
    {
        "user" : "iptv_tool",
        "passwd" : "123456",
        "host"  :   "172.29.3.189",
        "url" : "http://%s/services/Maltese" % ("172.29.3.189"),
        "ident": "hcm",
    },
    "thomson-hni":
    {
        "user" : "iptv_tool",
        "passwd" : "123456",
        "host"  :   "172.29.70.189",
        "url" : "http://%s/services/Maltese" % ("172.29.70.189"),
        "ident": "hni",
    },
    "thomson-lab":
    {
        "user" : "iptv_tool",
        "passwd" : "123456",
        "host"  : "172.17.5.110",
        "url" : "http://%s/services/Maltese" % ("172.17.5.110"),
        "ident": "lab",
    }
}


