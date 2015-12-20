import Skype4Py
import time
import datetime
from sets import Set

def format_time_stamp(stamp):
    return datetime.datetime.fromtimestamp(stamp).strftime('%Y-%m-%d %H:%M:%S')

def list_attr(obj):
    print 'listing attributes'
    public_props = (name for name in dir(obj) if not name.startswith('_'))
    for name in public_props:
        print name

class Bot:
    def __init__(self):
        self.skype = Skype4Py.Skype(Events=self)
        self.skype.FriendlyName = 'James Bot'
        self.skype.Attach()
        self.seen_msgs = Set() 

    def AttachmentStatus(self, status):
        if status == Skype4Py.apiAttachSuccess:
            print 'Successfully Attached'
            self._user_stats()
        elif status == Skype4Py.apiAttachPendingAuthorization:
            print 'Pending Authorization'
        else:
            print 'Unsucessfully Attached'

    def sending(self, msg):
        print format_time_stamp(msg.Timestamp), msg.Sender.FullName, ':', msg.Body

    def received(self, msg):
        print format_time_stamp(msg.Timestamp), msg.Sender.FullName, ':', msg.Body

    def MessageStatus(self, msg, status):
        if status == Skype4Py.cmsSending:
            self.sending(msg)
        elif status == Skype4Py.cmsReceived:
            if not msg.Id in self.seen_msgs:
                self.seen_msgs.add(msg.Id)
                self.received(msg)
        elif status == Skype4Py.cmsRead:
            if msg.Id in self.seen_msgs:
                self.seen_msgs.remove(msg.Id)
            else:
                self.received(msg)
        #print 'status', status, 'msg', msg.Body,'id', msg.Id

    def _user_stats(self):
        print 'Logged in as', self.skype.CurrentUser.FullName

def handle_user_input(user_input):
    print user_input

def main():
    bot = Bot()
    raw_input()

if __name__ == "__main__":
    main()
