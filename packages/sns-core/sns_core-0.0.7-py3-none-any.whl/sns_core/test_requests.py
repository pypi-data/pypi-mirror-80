import .requests

print("Sending 'USER follow' request")
response = requests.user('follow', From="me", To="you")

print("Received a response:")
print(response)