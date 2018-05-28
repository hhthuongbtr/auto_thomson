SYSTEM = {
    'broadcast_time': {
        'TO': 22, 
        'FROM': 6
        }, 
    'HOST': '10.0.0.205', 
    'libery': {
        'FFPROBE': '/usr/bin/ffprobe', 
        'FFMPEG': '/opt/ffmpeg/ffmpeg'
        }, 
    'monitor': {
        'SOURCE': True, 
        'BLACK_SCREEN': False
        }, 
    'BREAK_TIME': 20,
    'list_queue_groups':{
            'ORIGIN': 'origin',
            '4500': '4500',
            'PROBE': 'probe'
        },
    'LOG_QUEUE': 'thomson_log'
    }

API = {
    'master': {
        'URL': '42.117.9.100', 
        'PASSWORD': 'iptv13579', 
        'PORT': 8888, 
        'USER': 'monitor'
        },
    'slave': {
        'ACTIVE': False, 
        'URL': '42.117.9.99', 
        'PASSWORD': 'iptv13579', 
        'PORT': 8888, 
        'USER': 'monitor'
        }
    }

DATABASE = {
    'master': {
        'NAME': 'monitor', 
        'HOST': 'localhost', 
        'USER': 'root', 
        'ACTIVE': True, 
        'PASSWORD': 'root', 
        'PORT': 3306
        },
    'slave': {
        'NAME': 'monitor', 
        'HOST': 'localhost', 
        'USER': 'root', 
        'ACTIVE': False, 
        'PASSWORD': 'root', 
        'PORT': 3306
        }
    }

SUPERVISORD={
    'HOST'                  : 'localhost',
    'PORT'                  : 9001,
    'CONF_DIR'              : '/etc/supervisord/conf.d',
    'CONTROL_DIR'           : '/usr/bin/supervisorctl',
    'CONF_TEMPLATE_DIR'     : 'config/supervisord.template',
    'CONF_EXTENSION'        : '.ini'
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
    "double nodes",     #2
    "no video",         #3
    "no audio",         #4
    "cceror",           #5
    "output overflow",  #6
    "active main",      #7
    "active backup",    #8
    "NTP"               #9
]

ERROR_CODE_CHECK_ORIGIN_LIST = [1,7]
ERROR_CODE_CHECK_4500_LIST = [1,2,7,8]
