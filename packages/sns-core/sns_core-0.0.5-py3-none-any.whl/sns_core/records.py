from os.path import expanduser, isdir, isfile
from os import mkdir, mknod

from .exceptions import SNSrecordIntegrityException

SNS_RECORD_PATH = "~/.sns_records"

SNSuserRecord = None

class SNSuserRecordInstance():
    def __init__(self, identifier, provider):
        self.identifier = identifier
        self.provider = provider

def register_sns_records():
    global SNSuserRecord
    
    check_record_integrity(restore=True)

    with open(expanduser(SNS_RECORD_PATH) + "/user_record.dat") as user_record:
        record_items = dict(item.split(":", 1) for item in user_record.read().split(";") if ':' in item)

        SNSuserRecord = SNSuserRecordInstance(record_items['identifier'], record_items['provider'])
    
def check_record_integrity(restore=False):
    if not isdir(expanduser(SNS_RECORD_PATH)):
        if restore:
            mkdir(expanduser(SNS_RECORD_PATH))
        else:
            raise SNSrecordIntegrityException("User Record", "Missing the SNS records folder. Set the restore flag to True to restore the folder")

    if not isfile(expanduser(SNS_RECORD_PATH) + "/user_record.dat"):
        if restore:
            user_record = open(expanduser(SNS_RECORD_PATH) + "/user_record.dat", "w+")
            user_record.write("identifier:you;")
            user_record.write("provider:soter.social")
            user_record.close()
        else:
            raise SNSrecordIntegrityException("User Record", "Missing the UserRecord file. Set the restore flag to True to restore the file.\n[WARNING] This will create new key pairs")

register_sns_records()