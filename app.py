import os
import requests
from flask import Flask
from flask import jsonify
from flask import request
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from utils import create_markdown_list
from utils import generate_randomized_list
from utils import generate_demo_order_blocks
from utils import verify
from utils import verify_is_valid_demo_day

channel_id = os.environ["SLACK_CHANNEL_ID"]
slack_token = os.environ["SLACK_OAUTH_TOKEN"]
sc = WebClient(token=slack_token)

app = Flask(__name__)


@app.route("/")
def home():
    return "Homepage"


@app.route("/set-start-date", methods=["POST"])
def set_start_time():
    # if no start time found
    # prompt for start date
    # calculate all valid demo days starting from 14 days from start date
    # store list of valid demo days in db
    # else if there is a start time
    # confirm overwrite
    pass


@app.route("/get-scheduled-dates", methods=["GET", "POST"])
def get_scheduled_dates():
    # if there is a stored list of dates
    # get current date
    # return list of valid demo days after the current date
    # else if no dates stored
    # return no scheduled dates msg
    pass


@app.route("/delete-schedule", methods=["POST"])
def delete_schedule():
    # if there are valid demo days
    # delete stored valid demo days
    # else if no dates stored then no action is taken
    # alert nothing was done
    pass


@app.route("/slash-get-list", methods=["POST"])
def slash_get_list():
    if verify(request):
        return {
            "response_type": "in_channel",
            "blocks": generate_demo_order_blocks(),
        }
    else:
        return {
            "response_type": "in_channel",
            "text": "An error occured with this request"
        }


def post_scheduled_demo_order_msg(event, context):
    if verify_is_valid_demo_day():
        sc.chat_postMessage(
            channel=channel_id,
            blocks=generate_demo_order_blocks(
                    "It's Demo Day! Here are the order of presentations:"
                ),
        )

    # silently fail and do nothing if it is not a demo day
    return
