#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from github_webhook import Webhook
from flask import Flask
import json
import github
import os

app = Flask(__name__)
webhook = Webhook(app)
TOKEN = os.environ["GITHUB_TOKEN"]
NEW_ISSUE_LABELS = os.environ["NEW_ISSUE_LABELS"]


@app.route("/")
def hello_world():
    return "Hello, World!"

@webhook.hook("issues")
def on_issues(data):
    allowed_ations = ["opened"]
    (owner_dict, repo_dict, issue_dict, action) = parse_issue_info(data)
    print("Sender: {} Repo: {} Issue: {} Action: {}\n".format(
        owner_dict["login"], repo_dict["name"], 
        issue_dict["number"], action
    ) )
    if not (action in allowed_ations):
        return "Action not allowed"
    issue = get_issue(repo_dict, issue_dict)
    issue.add_to_labels(NEW_ISSUE_LABELS)
    
    

# @webhook.hook("issue_comment")
# def on_issue_comment(data):
#     print("Got push with: {0}".format(data))
#     with open("/tmp/issues_comment.data", "w") as fi:
#         fi.write(json.dumps(data, indent=2))


def parse_issue_info(data):
    return (data["sender"], data["repository"], data["issue"], data["action"])

def get_issue(repo_dict, issue_dict):
    g = github.Github(TOKEN)
    repo = g.get_repo(repo_dict["id"])
    issue = repo.get_issue(issue_dict["number"])
    return issue


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=20886)
