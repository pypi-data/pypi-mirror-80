from .server import SNSserver
from .parser import SNSinteraction

SNSserver.start_server()

@SNSserver(type="USER", action="*")
def follow_user(request):
    return SNSinteraction("STATUS", 200, {})

@SNSserver(type="GROUP", action="join")
def join_group(request):
    return SNSinteraction("STATUS", 201, {})