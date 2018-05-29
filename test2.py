from schedule_auto_thomson import ScheduleAuto

log = """[{"sev": "Minor", "nid": 9, "host": "172.29.3.189", "opdate": 1527559107622, "cldate": 1527559110622, "lid": 2640666153587716, "jid": 11822, "res": "FILE /Video_Main//EPL_181017.ts", "cat": "Communication", "jname": "Kenh EPL Ao.Test", "desc": "Stream discontinuity:continuity counter error on PID 2068"}]"""

sa = ScheduleAuto()
base_dir = sa.set_supervisord_schedule(host="1.1.1.1", jid=1111, name="test", ip="1.1.1.1")
print type(base_dir)
