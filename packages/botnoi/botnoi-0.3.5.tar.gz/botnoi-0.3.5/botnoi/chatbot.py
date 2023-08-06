class lineevent():
  def __init__(self,event):
    self.event = event
    self.eventtype = event['events'][0]['type']
    self.msgid  = event['events'][0]['message']['id']
    self.time = event['events'][0]['timestamp']
    self.token = event['events'][0]['replyToken']
    self.idpage = event['destination']
    self.userid = event['events'][0]['source']['userId']
  def extractmessage(self):
    self.message = event['events'][0]['message']['text']





