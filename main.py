
from dotenv import load_dotenv

load_dotenv()


import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest

client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
log_channel = "#norplink-logs"
try:
    response = client.chat_postMessage(channel='#norplink-logs', text="Hello world!")
    assert response["message"]["text"] == "Hello world!"
except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
    assert e.response["ok"] is False
    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    print(f"Got an error: {e.response['error']}")
    # Also receive a corresponding status_code
    assert isinstance(e.response.status_code, int)
    print(f"Received a response status_code: {e.response.status_code}")

def send_log(client:WebClient, user, channel, timestamp, link):
    text = f"<@{user}> in <#{channel}> at {timestamp} posted {link}"
    client.chat_postMessage(channel=log_channel, text=text)

send_log(client, "U05QJ4CF5QT", "C0ADTEB9GA0", "12345", "https://asd.com")



# # Initialize SocketModeClient with an app-level token + WebClient
# client = SocketModeClient(
#     # This app-level token will be used only for establishing a connection
#     app_token=os.environ.get("SLACK_APP_TOKEN"),  # xapp-A111-222-xyz
#     # You will be using this WebClient for performing Web API calls in listeners
#     web_client=WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))  # xoxb-111-222-xyz
# )


# def process(client: SocketModeClient, req: SocketModeRequest):
#     if req.type == "events_api":
#         # Acknowledge the request anyway
#         response = SocketModeResponse(envelope_id=req.envelope_id)
#         client.send_socket_mode_response(response)

#         # Add a reaction to the message if it's a new message
#         if req.payload["event"]["type"] == "message" \
#             and req.payload["event"].get("subtype") is None:
#             client.web_client.reactions_add(
#                 name="eyes",
#                 channel=req.payload["event"]["channel"],
#                 timestamp=req.payload["event"]["ts"],
#             )
#     if req.type == "interactive" \
#         and req.payload.get("type") == "shortcut":
#         if req.payload["callback_id"] == "hello-shortcut":
#             # Acknowledge the request
#             response = SocketModeResponse(envelope_id=req.envelope_id)
#             client.send_socket_mode_response(response)
#             # Open a welcome modal
#             client.web_client.views_open(
#                 trigger_id=req.payload["trigger_id"],
#                 view={
#                     "type": "modal",
#                     "callback_id": "hello-modal",
#                     "title": {
#                         "type": "plain_text",
#                         "text": "Greetings!"
#                     },
#                     "submit": {
#                         "type": "plain_text",
#                         "text": "Good Bye"
#                     },
#                     "blocks": [
#                         {
#                             "type": "section",
#                             "text": {
#                                 "type": "mrkdwn",
#                                 "text": "Hello!"
#                             }
#                         }
#                     ]
#                 }
#             )

#     if req.type == "interactive" \
#         and req.payload.get("type") == "view_submission":
#         if req.payload["view"]["callback_id"] == "hello-modal":
#             # Acknowledge the request and close the modal
#             response = SocketModeResponse(envelope_id=req.envelope_id)
#             client.send_socket_mode_response(response)

# # Add a new listener to receive messages from Slack
# # You can add more listeners like this
# client.socket_mode_request_listeners.append(process)
# # Establish a WebSocket connection to the Socket Mode servers
# client.connect()
# # Just not to stop this process
# from threading import Event
# Event().wait()