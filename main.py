from dotenv import load_dotenv

load_dotenv()


import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest


# Initialize SocketModeClient with an app-level token + WebClient
client = SocketModeClient(
    # This app-level token will be used only for establishing a connection
    app_token=os.environ.get("SLACK_APP_TOKEN"),  # xapp-A111-222-xyz
    # You will be using this WebClient for performing Web API calls in listeners
    web_client=WebClient(token=os.environ.get("SLACK_BOT_TOKEN")),  # xoxb-111-222-xyz
)


log_channel = "#norplink-logs"


def send_log(client: WebClient, user, channel, timestamp, links):
    domain_count = {}
    for link in links:
        # domain_count[link["domain"]] += 1
        domain_count[link["domain"]] = domain_count.get(link["domain"], 0) + 1
    # (Replace . with [dot] in urls to make them unclickable)

    text = f"<@{user}>({user}) in <#{channel}>({channel}) at {timestamp} posted {", ".join(f"{count}x {domain}" for domain, count in domain_count.items())}"

    client.chat_postMessage(channel=log_channel, text=text)


# send_log(client, "U05QJ4CF5QT", "C0ADTEB9GA0", "12345", "https://asd.com")


def process(client: SocketModeClient, req: SocketModeRequest):

    print(req.type)
    if req.type == "events_api":
        # Acknowledge the request anyway
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)
        print(req.payload["event"]["type"])
        # print(req.payload["event"])
        # print(req.payload)
        # Add a reaction to the message if it's a new message
        if (
            req.payload["event"]["type"]
            == "link_shared"
            # and req.payload["event"].get("subtype") is None
        ):

            user = req.payload["event"]["user"]
            channel = req.payload["event"]["channel"]
            ts = req.payload["event"]["message_ts"]
            links = req.payload["event"]["links"]
            print(f"Link Shared! f{user} in {channel} at {ts} shared links to {links}")
            if channel != "COMPOSER":
                send_log(
                    client=client.web_client,
                    user=user,
                    channel=channel,
                    timestamp=ts,
                    links=links,
                )


# Add a new listener to receive messages from Slack
# You can add more listeners like this
client.socket_mode_request_listeners.append(process)
# Establish a WebSocket connection to the Socket Mode servers
client.connect()
# Just not to stop this process
from threading import Event

Event().wait()


# client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

# try:
#     response = client.chat_postMessage(channel="#norplink-logs", text="Hello world!")
#     assert response["message"]["text"] == "Hello world!"
# except SlackApiError as e:
#     # You will get a SlackApiError if "ok" is False
#     assert e.response["ok"] is False
#     assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
#     print(f"Got an error: {e.response['error']}")
#     # Also receive a corresponding status_code
#     assert isinstance(e.response.status_code, int)
#     print(f"Received a response status_code: {e.response.status_code}")
