
from twilio.rest import Client

account_sid = "AC0dc1a21da68954d29bb7610cd57db786"
auth_token = "e424f3294b6b5d89df36b62c8ca7fd6f"

twilio_num = "+18444313888"
target_num = "+15043579029"


client = Client(account_sid, auth_token)

message = client.messages.create(
    body= "This is what you want the message to be",
    from_= twilio_num,
    to= target_num
)
