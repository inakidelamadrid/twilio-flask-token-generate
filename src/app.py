from json import load
import os
from dotenv import load_dotenv
from flask import Flask, request, abort
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant, ConversationsGrant

load_dotenv()
twilio_account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
twilio_api_key_sid = os.environ.get("TWILIO_API_KEY_SID")
twilio_api_key_secret = os.environ.get("TWILIO_API_KEY_SECRET")

app = Flask(__name__)


@app.route("/token", methods=["POST"])
def token():
    """Generate an access token."""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # validate username and password
    # (this is application-specific and should be implemented according to
    # your application requirements)
    if not username or not password:
        abort(401)

    token = AccessToken(
        twilio_account_sid,
        twilio_api_key_sid,
        twilio_api_key_secret,
        identity=username,
        ttl=3600,
    )

    # add grants to token
    token.add_grant(VideoGrant(room="My Room"))
    token.add_grant(ConversationsGrant(configuration_profile_sid="configuration_profile_sid"))

    return {'token': token.to_jwt()}
