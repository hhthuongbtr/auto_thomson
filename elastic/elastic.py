from elasticsearch import Elasticsearch
from utils import DateTime
from config import DATABASE
import json

port = DATABASE["elastic"]["PORT"]
host = DATABASE["elastic"]["HOST"]
def get_the_last_active_backup_log_by_jobid(thomson_host, jobid):
    query = {
      "from": 0,
      "size": 1,
      "_source": ["message"], 
      "sort": [
        {
          "@timestamp": {
            "order": "desc"
          }
        }
      ],
      "query": {
        "bool": {
          "must": [
            {
              "match": {
                "message": "%s"%(thomson_host)
              }
            },
            {
              "match": {
                "message": "%d"%(jobid)
              }
            },
            {
              "match": {
                "message": "input:backup"
              }
            }
          ]
        }
      }
    }
    d_time = DateTime()
    now = d_time.get_now_as_logtash_fortmat()
    yesterday = d_time.get_yesterday_as_logtash_fortmat()
    index = "logstash-%s,logstash-%s"%(now, yesterday)
    elast = Elasticsearch([{'host': host, 'port': port}]).search(index= index,body = query,)
    return elast['hits']['hits']
   
def get_history_auto_return_main(thomson_host, jobid):
    query = {
      "from": 0,
      "size": 1000,
      "sort": [
        {
          "@timestamp": {
            "order": "desc"
          }
        }
      ], 
      "_source": ["message"], 
      "query": {
        "bool": {
          "must": [
            {
              "match": {
                "host.keyword": "thomson"
              }
            },
            {
              "match": {
                "message": "tool just"
              }
            },
            {
              "match": {
                "message": "the main source"
              }
            },
            {
              "match": {
                "message": "%s"%(thomson_host)
              }
            },
            {
              "match": {
                "message": "%d"%(jobid)
              }
            }
          ],
          "filter": {
            "range": {
              "@timestamp": {
                "gte": "now-5m",
                "lte": "now"
              }
            }
          }
        }
      }
    }
    d_time = DateTime()
    now = d_time.get_now_as_logtash_fortmat()
    yesterday = d_time.get_yesterday_as_logtash_fortmat()
    index = "logstash-%s,logstash-%s"%(now, yesterday)
    elast = Elasticsearch([{'host': host, 'port': port}]).search(index= index,body = query,)
    return elast['hits']['hits'] 

