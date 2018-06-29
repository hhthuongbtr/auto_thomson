from elasticsearch import Elasticsearch
from utils import DateTime
import json

port = 9200
host = "183.80.133.166"
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

def query_by_ident(index='_all' ,host=None, port=9200, ident=None, size=500, ip=0):
    """
    Return array log
    :host: ip elasticsearch
    :port: port of elasticsearch server (default 9200)
    :ident: tu khoa dung de match du lieu
    :size: so luong data lay ra (default 500)
    :index: index of elasticsearch
    :ip: ip address thomson
    """
    query = {
        "sort": [{"@timestamp": "desc"}],
        "from": 0,
        "size": 2,
        "_source": ["message"],
        "query": {
          "bool": {
            "must": [
              {
                "match": {
                  "ident.keyword": "Monitor"
                }
              },
              {
                "match": {
                  "message": "origin"
                }
              },
              {
                "match": {
                  "message": "hni"
                }
              },
              {
                "match": {
                  "message": "down"
                }
              },
              {
                "match": {
                  "message": "239.1.2.17"
                }
              }
            ],
            "filter": {
              "range": {
                "@timestamp": {
                  "gte": "now-24h",
                  "lte": "now"
                }
              }
            }
          }
        },
        "sort": [
          {
            "@timestamp": {
              "order": "DESC"
            }
          }
        ]
      }
    elast = Elasticsearch([{'host':host, 'port': port}]).search(index= index,body = query,)
    return elast['hits']['hits']

#aa = query_by_ident(index='_all' ,host="183.80.133.166", port=9200, ident=None, size=500, ip="172.29.70.189")
#for i in aa:
#    tmp = i["_source"]["message"]
#    log = json.loads(tmp[tmp.find("{"):tmp.find("}")+1])
#    print log["desc"]
