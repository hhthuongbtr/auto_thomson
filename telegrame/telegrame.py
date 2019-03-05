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
            self.bot.send_message(chat_id=self.chat_id, text=text, )
        except Exception as e:
            print ("Error {0}!".format(e))

    def conver_content(self, data=""):
        """conver message json to text/html"""
        data = data
        try:
            hostname = THOMSON_NAME[data["host"]]
            sev = data["sev"]
            jid = data["jid"]
            jname = data["jname"]
            desc = data["desc"]
            return "<b>{0}</b> <br/> Severily: {1} - Job Name: {2} - Job ID: {3} - Description: {4}".format(hostname, sev, jname, jid, desc)
        except Exception as ex:
            print("Error {0}!".format(ex))
            return None