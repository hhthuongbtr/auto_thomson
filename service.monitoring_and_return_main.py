import re
import json
import threading
import logging
import logging.config
import logging.handlers
from rabbit import Rabbit
from config import SYSTEM, THOMSON_HOST
from thomsonapi import JobDetail
import MySQLdb as mdb

with open("config/python_logging_configuration.json", 'r') as configuration_file:
    config_dict = json.load(configuration_file)
logging.config.dictConfig(config_dict)
# Create the Logger
logger = logging.getLogger("return_main")

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
    session = mdb.connect(host="localhost", port=3306, user="thomson", passwd="thomson@$@", db="thomson", charset='utf8')
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

def is_running_backup_on_thomson(data, job_detail_object):
    is_running_backup = False
    job_info = job_detail_object.get_info()
    if not job_info:
        logger.error("Can not file job: %s on host"%(str(data)))
        return is_running_backup
    job_info = json.loads(job_info)
    status = job_info["status"]
    if status.upper() == "CRITICAL":
        is_running_backup = True
    logger.info("Job(%s) status |%s| --> return %s"%(str(data), status.upper(), str(is_running_backup)))
    return is_running_backup

def is_not_overworked(data):
    is_not_over = True
    return is_not_over

def return_main(body):
    if not is_json(body):
        print "Not json %s"%(str(body))
        return 1
    data = json.loads(body)
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
    is_running_backup = is_running_backup_on_thomson(data, jd)
    if not (is_auto and is_running_backup and is_not_overwork):
        logger.warning("Job(%s) is not auto --> check your config: is_auto(%s), is_not_overwork(%s), is_running_backup(%s)"%(str(data), str(is_auto), str(is_not_overwork), str(is_running_backup)))
        print "Job: %d not auto"%(jid)
        return 0
    disable_backup = jd.is_backup("false")
    logger.warning("Job(%s) disable backup --> %s"%(str(data), disable_backup))
    time.sleep(2)
    enable_backup = jd.is_backup("true")
    logger.warning("Job(%s) enable backup --> %s"%(str(data), enable_backup))
    return 0

def callback(ch, method, properties, body):
    print "------------->\n" + body + "\n<-------------"
    logger.info("received " + body)
    if not body:
        logger.warning("received " + body + "empty!")
        return 1
    t = threading.Thread(target=return_main, args=(body,))
    t.start()

if __name__ == "__main__":
    """
    rb = Rabbit(SYSTEM["RUNNING_BACKUP_QUEUE"])
    rb.connect()
    rb.channel.basic_consume(callback,
                          queue=rb.routing_key,
                          no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    rb.channel.start_consuming()
    """
    data = """{"host":"172.17.5.110", "jid": 1100}"""
    print return_main(data)
