import re
import json

def is_double_node(dscr= None):
    if not dscr:
        return None
    double_node_pattern = re.compile("Job is running on node(s): \d{1,2} and \d{1,2}")
    double_node = re.findall(cron_pattern, self.task)
    if double_node:
        return True
    return False

def is_lost_source(dscr= None):
    if not dscr:
        return None
    if dscr == "Loss of TS synchro":
        return True
    return False

def is_no_video(dscr= None):
    if not dscr:
        return None
    if "No component:on video" in dscr:
        return True
    return False

def is_no_audio(dscr= None):
    if not dscr:
        return None
    if "No component:on audio":
        return True
    return False

def is_cceror(dscr= None):
    if not dscr:
        return None
    if "continuity counter" in dscr:
        return True
    return False

def overflow(dscr= None):
    if not dscr:
        return None
    if "overflow" in dscr:
        return True
    return False

def is_returned_main(dscr= None):
    if not dscr:
        return None
    if "Active input:main" in dscr:
        return True
    return False
