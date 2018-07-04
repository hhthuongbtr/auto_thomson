import re
import time
import json
import threading
import logging
import logging.config
import logging.handlers
from rabbit import Rabbit
from config import SYSTEM, THOMSON_HOST, DATABASE
from elastic.elastic import *
from thomsonapi import JobDetail
import MySQLdb as mdb
from utils import DateTime

with open("config/python_logging_configuration.json", 'r') as configuration_file:
    config_dict = json.load(configuration_file)
logging.config.dictConfig(config_dict)
# Create the Logger
logger = logging.getLogger("return_main")
times_limit = 3

def get_ip(source):
    ip_pattern=re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    ip = re.findall(ip_pattern, source)
    try:
        ip = ip[0]
    except Exception as e:
        ip = None
    return ip

def is_json(data):
    try:
        json.loads(data)
        return True
    except:
        return False

def is_auto_return_main(data):
    is_auto = False
    query = """select auto from job_auto where jid = %d and host = '%s';"""%(data["jid"], data["host"])
    host = DATABASE["master"]["HOST"]
    port = DATABASE["master"]["PORT"]
    user = DATABASE["master"]["USER"]
    passwd = DATABASE["master"]["PASSWORD"]
    name = DATABASE["master"]["NAME"]
    session = mdb.connect(host=host, port=port, user=user, passwd=passwd, db=name, charset='utf8')
    row = None
    if not query:
        print 'No query!'
    try:
        cur=session.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        session.close()
    except Exception as e:
        print e
        logger.error("ERROR durring excute querry: %s"%(str(e)))
        session.close()
        return is_auto
    if len(rows):
        row = rows[0]
        is_auto = True if row[0] else False
        logger.info("Job(%s) auto setting is: %s --> return %s"%(str(data), str(row[0]), str(is_auto)))
    return is_auto


def is_running_backup_on_thomson(data):
    is_running_backup = False
    log_list = get_the_last_active_backup_log_by_jobid(data["host"], data["jid"])
    if not len(log_list):
        logger.info("Job(%s) Not found active backup log or lager than 2 days --> return %s"%(str(data), is_running_backup))
    else:
        log = str(log_list[0]["_source"]["message"])
        log_object = log[log.find("{"):]
        log_object = json.loads(log_object)
        if not log_object["cldate"]:
            is_running_backup = True
        logger.info("Job(%s) clearning date |%s| --> return %s"%(str(data), log_object["cldate"], str(is_running_backup)))
    return is_running_backup

def get_job_status(job_detail_object):
    job_status = ""
    job_info = job_detail_object.get_info()
    if not job_info:
        logger.error("Can not file job: %s on host %s"%(str(job_detail_object.jid), str(job_detail_object.host)))
        return job_status
    job_info = json.loads(job_info)
    job_status = job_info["status"]
    return job_status

def is_not_overworked(data):
    is_over = False
    history = get_history_auto_return_main(data["host"], data["jid"])
    times = len(history)
    is_over = times >= SYSTEM["REPEAT_LIMIT"]
    logger.info("Job (%s) auto return main %d/%d on 5 minute --> over worked(%s)"%(str(data), times+1, SYSTEM["REPEAT_LIMIT"], str(is_over)))
    return not is_over

def get_job_backup_info(job_detail_object):
    ip = None
    port = None
    job_param_list = job_detail_object.get_param()
    if not job_param_list:
        logger.error("Can not find job: %s on host %s"%(str(job_detail_object.jid), str(job_detail_object.host)))
        return ip, port
    job_param_list = json.loads(job_param_list)
    param_list = job_param_list[0]["params"]
    for param in param_list:
        if str(param["name"]).upper() == "BACKUP INPUT IP ADDRESS":
            ip = param["value"]
            continue
        elif str(param["name"]).upper() == "BACKUP INPUT UDP PORT":
            port = int(param["value"])
            continue
        elif ip and port:
            break
    return ip, port

def stop_job(job_detail_object):
    times = 1
    stop = "NotOK"
    while times <= times_limit:
        stop = job_detail_object.abort()
        logger.info("Job(id: %s from thomson: %s) STOP --> %s"%(str(job_detail_object.jid), job_detail_object.host, stop))
        if stop.upper() == "OK":
            break
        times += 1
        time.sleep(1)
    return stop
   

def start_job(job_detail_object):
    times = 1
    start = "NotOK"
    while times <= times_limit:
        start = job_detail_object.start()
        logger.info("Job(id: %s from thomson: %s) START --> %s"%(str(job_detail_object.jid), job_detail_object.host, start))
        if start.upper() == "OK":
            break
        times += 1
        time.sleep(1)
    return start

def active_backup(job_detail_object):
    times = 1
    enable_backup = "NotOK"
    while times <= times_limit:
        enable_backup = job_detail_object.set_backup("true")
        logger.info("Job(id: %s from thomson: %s) enable active backup --> %s times %d"%(str(job_detail_object.jid), job_detail_object.host, enable_backup, times))
        if enable_backup.upper() == "OK":
            break
        times += 1
        time.sleep(2)
    return enable_backup


def deactive_backup(job_detail_object):
    times = 1
    disable_backup = "NotOK"
    while times <= times_limit:
        disable_backup = job_detail_object.set_backup("false")
        logger.info("Job(id: %s from thomson: %s) disable active backup --> %s times %d"%(str(job_detail_object.jid), job_detail_object.host, disable_backup, times))
        if disable_backup.upper() == "OK":
            break
        times += 1
        time.sleep(2)
    return disable_backup

def set_backup_ip(job_detail_object, ip):
    times = 1
    set_backup = "NotOK"
    while times <= times_limit:
        set_backup = job_detail_object.set_backup_ip_address(ip)
        logger.info("Job(id: %s from thomson: %s) thomson tool change value ip backup to %s --> %s"%(str(job_detail_object.jid), job_detail_object.host, ip, set_backup))
        if set_backup.upper() == "OK":
            break
        times += 1
        time.sleep(2)
    return set_backup
 
def set_backup_udp_port(job_detail_object, port):
    port = str(port)
    times = 1
    set_backup_port = "NotOK"
    time.sleep(2)
    while times <= times_limit:
        set_backup_port = job_detail_object.set_backup_udp_port(str(port))
        logger.info("Job(id: %s from thomson: %s) thomson tool change value udp port backup to %s --> %s"%(str(job_detail_object.jid), job_detail_object.host, port, set_backup_port))
        if set_backup_port.upper() == "OK":
            break
        times += 1
        time.sleep(2)
    return set_backup_port


def return_main(body):
    if not is_json(body):
        logger.error("Recieve: %s not json fortmat --> break"%(str(body)))
        print "Not json %s"%(str(body))
        return 1
    data = json.loads(body)
    if data["status"] != 1:
        logger.warning("Job(%s)single status is %s --> not ok --> not return main"%(str(data)))
    jid = int(data["jid"])
    target_host = data["host"]
    account = None
    for i in THOMSON_HOST:
        if THOMSON_HOST[i]["host"] == target_host:
            account = THOMSON_HOST[i]
            break
    if not account:
        logger.error("Host %s not found on setting list: %s"%(target_host, str(THOMSON_HOST)))
        print "Host: %s not found!"%(target_host)
        return 1
    jd = JobDetail(account["host"], account["user"], account["passwd"], jid)
    is_auto = is_auto_return_main(data)
    is_not_overwork = is_not_overworked(data)
    is_running_backup = is_running_backup_on_thomson(data)
    if not is_running_backup:
        time.sleep(10)
        is_running_backup = is_running_backup_on_thomson(data)
    if not is_running_backup:
        time.sleep(10)
        is_running_backup = is_running_backup_on_thomson(data)
    if not (is_auto and is_running_backup and is_not_overwork):
        logger.warning("Job(%s) is not auto --> check your config: is_auto(%s), is_not_overwork(%s), is_running_backup(%s)"%(str(data), str(is_auto), str(is_not_overwork), str(is_running_backup)))
        date_time = DateTime()
        print "%s Job: %d from thomson %s not auto"%(str(date_time.get_now_as_human_creadeble()),jid,target_host)
        return 0
    if not SYSTEM["auto"]["RETURN_MAIN"]:
        logger.warning("System auto return main not active check your config!")
        return 1
    job_status = get_job_status(jd)
    logger.info("Job(%s) status --> |%s|"%(str(data), job_status))
    if job_status.upper() == "OK":
        origin_source_backup, origin_udp_port = get_job_backup_info(jd)
        disable_backup = deactive_backup(jd)
        time.sleep(2)
        enable_backup = active_backup(jd)
        if enable_backup.upper() == "NOTOK":
            stop = stop_job(jd)
            #logger.warning("Job(%s) STOP --> %s"%(str(data), stop))
            time.sleep(1)
            enable_backup = active_backup(jd)
            logger.warning("Job(%s) enable backup --> %s"%(str(data), enable_backup))
            time.sleep(1)
            start = start_job(jd)
            #logger.warning("Job(%s) START --> %s"%(str(data), start))
        logger.critical("Tool just returned the main source by disable and enable Active backup: Job(%s)"%(str(data)))
        source_backup, udp_port = get_job_backup_info(jd)
        if origin_source_backup != source_backup:
            set_backup = set_backup_ip(jd, origin_source_backup)
            logger.warning("Job(%s) thomson tool change value ip backup from %s to %s --> %s"%(str(data), source_backup, origin_source_backup, set_backup))
        if origin_udp_port != udp_port:
            set_backup_port = set_backup_udp_port(jd, origin_udp_port)
            logger.warning("Job(%s) thomson tool change value udp port backup from %s to %s --> %s"%(str(data), str(source_backup), str(origin_source_backup), set_backup_port))
    elif job_status.upper() == "MAJOR":
        stop = stop_job(jd)
        time.sleep(2)
        start = start_job(jd)
        logger.critical("Tool just returned the main source by stop and start job: Job(%s)"%(str(data)))
    return 0

def callback(ch, method, properties, body):
    date_time = DateTime()
    print "------------->\n" + str(date_time.get_now_as_human_creadeble()) + " recieved: " + body + "\n<-------------"
    logger.info("received " + body)
    if not body:
        logger.warning("received " + body + "empty!")
        return 1
    t = threading.Thread(target=return_main, args=(body,))
    t.start()

if __name__ == "__main__":
    rb = Rabbit(SYSTEM["RUNNING_BACKUP_QUEUE"])
    rb.connect()
    rb.channel.basic_consume(callback,
                          queue=rb.routing_key,
                          no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    rb.channel.start_consuming()
    #data = """{"host":"172.17.5.110", "jid": 1100}"""
    #print return_main(data)
