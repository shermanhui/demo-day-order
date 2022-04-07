import ast
import os
import random
import hashlib
import hmac
import pytz

from datetime import date
from datetime import datetime
from datetime import timedelta
from pytz import timezone

slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]
team_list_var = os.environ["TEAM_LIST"]


def create_markdown_list(elements):
    if not elements:
        return ""

    # Slack doesn't support actual markdown lists so I'm mocking a list
    # with a "-" char before each element and a new line after
    # https://api.slack.com/reference/surfaces/formatting#block-formatting
    markdown_list = ""

    for element in elements:
        markdown_list += f"- {element}\n "

    return markdown_list


def generate_demo_order_blocks(header_text="Here's a list of teams in random order:"):
    team_list = generate_randomized_list(team_list_var)
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": header_text,
            },
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": create_markdown_list(team_list)},
        },
    ]


def generate_randomized_list(team_list):
    # Add check for team list after its stored in db
    teams = ast.literal_eval(team_list)
    return random.sample(teams, len(teams))


def generate_valid_dates():
    valid_dates = []
    start_date = date(2021, 1, 7)
    end_date = date(2021, 12, 31)

    delta = end_date - start_date

    for i in range(0, delta.days + 1, 14):
        day = start_date + timedelta(days=i)
        valid_dates.append(day)

    return valid_dates


def verify(request, secret=slack_signing_secret):
    body = request.get_data()

    decoded_body = body.decode("utf-8")

    timestamp = request.headers["X-Slack-Request-Timestamp"]

    base_string = f"v0:{timestamp}:{decoded_body}"

    computed_sha = hmac.new(
        secret.encode("utf-8"),
        base_string.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()

    generated_signature = f"v0={computed_sha}"

    slack_signature = request.headers["X-Slack-Signature"]

    if not hmac.compare_digest(generated_signature, slack_signature):
        err_str = (
            f"generated_signature: {generated_signature} "
            f"does not equal slack_signature {slack_signature}"
        )
        raise Exception(err_str)
    else:
        return True


def verify_is_valid_demo_day():
    valid_dates = [
        "2022-01-13",
        "2022-01-27",
        "2022-02-10",
        "2022-02-24",
        "2022-03-10",
        "2022-03-24",
        "2022-04-07",
        "2022-04-21",
        "2022-05-05",
        "2022-05-19",
        "2022-06-02",
        "2022-06-16",
    ]

    current_date = (
        datetime.now(tz=pytz.utc)
        .astimezone(tz=timezone("America/Los_Angeles"))
        .strftime("%Y-%m-%d")
    )

    if current_date in valid_dates:
        return True

    return
