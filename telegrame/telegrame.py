import telegram
from config import THOMSON_NAME
class telegrambot(object):
    def __init__(self, token=None, chat_id=None):
        """ crate chat bot """
        self.token = token
        self.chat_id = chat_id
        self.bot = telegram.Bot(token = self.token)
 
    def send_message(self, data=""):
        text = self.conver_content(data=data)
        try:
            self.bot.send_message(chat_id=self.chat_id, text=text, parse_mode="HTML")
        except Exception as e:
            print ("Error {0}!".format(e))

    def conver_content(self, data=""):
        """conver message json to text/html"""
        from utils.DateTime import DateTime
        data = data
        now = DateTime().get_now_as_human_creadeble()
        try:
            hostname = THOMSON_NAME[data["host"]]
            sev = data["sev"]
            jid = data["jid"]
            jname = data["jname"]
            desc = data["desc"]
            return "[{5}]<b>{0}</b>  Severity: <code>{1}</code>, JobName: <code>{2}</code>, JobID: <code>{3}</code>, Description: <code>{4}</code>".format(hostname, sev, jname, jid, desc, now)
        except Exception as ex:
            print("Error {0}!".format(ex))
            return None
