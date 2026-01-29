from flask import Blueprint, request, jsonify
from app.extensions import mongo

webhook = Blueprint("webhook", __name__, url_prefix="/webhook")

# 👇 Health check route (browser friendly)
@webhook.route("/", methods=["GET"])
def health():
    return {"status": "Webhook running"}, 200


# 👇 GitHub webhook receiver
@webhook.route("/receiver", methods=["POST"])
def receiver():
    payload = request.json

    event_type = request.headers.get("X-GitHub-Event")
    author = payload.get("pusher", {}).get("name")
    ref = payload.get("ref", "")
    branch = ref.split("/")[-1]
    timestamp = payload.get("head_commit", {}).get("timestamp")

    mongo.db.events.insert_one({
        "event_type": event_type,
        "author": author,
        "to_branch": branch,
        "timestamp": timestamp
    })

    return {"status": "ok"}, 200
