from datetime import datetime
from flask import Blueprint, request, jsonify
from pymongo.errors import PyMongoError

from app.extensions import mongo

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')


@webhook.route('/receiver', methods=['POST'])
def receiver():
    event_type = request.headers.get('X-GitHub-Event', '')
    payload = request.json
    
    if not payload:
        return {'error': 'No payload received'}, 400
    
    event_data = None
    
    if event_type == 'push':
        event_data = handle_push_event(payload)
    elif event_type == 'pull_request':
        event_data = handle_pull_request_event(payload)
    
    if event_data:
        try:
            mongo.db.events.insert_one(event_data)
            return {'status': 'success', 'action': event_data['action']}, 200
        except PyMongoError as e:
            return {'error': 'Failed to store event', 'details': str(e)}, 500
    
    return {'status': 'ignored', 'event': event_type}, 200


def handle_push_event(payload):
    ref = payload.get('ref', '')
    branch = ref.replace('refs/heads/', '') if ref.startswith('refs/heads/') else ref
    
    commits = payload.get('commits', [])
    head_commit = payload.get('head_commit', {})
    
    commit = head_commit if head_commit else (commits[0] if commits else {})
    
    author = commit.get('author', {}).get('name', 'Unknown')
    commit_hash = commit.get('id', payload.get('after', ''))
    timestamp = commit.get('timestamp', datetime.utcnow().isoformat())
    
    return {
        'request_id': commit_hash,
        'author': author,
        'action': 'PUSH',
        'from_branch': branch,
        'to_branch': branch,
        'timestamp': timestamp
    }


def handle_pull_request_event(payload):
    action = payload.get('action', '')
    pr = payload.get('pull_request', {})
    
    if action not in ['opened', 'reopened', 'closed']:
        return None
    
    author = pr.get('user', {}).get('login', 'Unknown')
    pr_id = str(pr.get('number', ''))
    from_branch = pr.get('head', {}).get('ref', '')
    to_branch = pr.get('base', {}).get('ref', '')
    
    is_merged = pr.get('merged', False)
    merged_at = pr.get('merged_at')
    
    if action == 'closed' and is_merged:
        timestamp = merged_at if merged_at else datetime.utcnow().isoformat()
        return {
            'request_id': pr_id,
            'author': author,
            'action': 'MERGE',
            'from_branch': from_branch,
            'to_branch': to_branch,
            'timestamp': timestamp
        }
    elif action in ['opened', 'reopened']:
        created_at = pr.get('created_at', datetime.utcnow().isoformat())
        return {
            'request_id': pr_id,
            'author': author,
            'action': 'PULL_REQUEST',
            'from_branch': from_branch,
            'to_branch': to_branch,
            'timestamp': created_at
        }
    
    return None


api = Blueprint('API', __name__, url_prefix='/api')


@api.route('/events', methods=['GET'])
def get_events():
    try:
        events = list(mongo.db.events.find({}, {'_id': 0}).sort('_id', -1).limit(50))
    except PyMongoError as e:
        return jsonify({'error': 'Failed to fetch events', 'details': str(e)}), 500
    
    formatted_events = []
    for event in events:
        message = format_event_message(event)
        formatted_events.append({
            **event,
            'message': message
        })
    
    return jsonify(formatted_events)


def format_event_message(event):
    action = event.get('action', '')
    author = event.get('author', 'Unknown')
    from_branch = event.get('from_branch', '')
    to_branch = event.get('to_branch', '')
    timestamp = event.get('timestamp', '')
    
    if action == 'PUSH':
        return f'"{author}" pushed to "{to_branch}" on {timestamp}'
    elif action == 'PULL_REQUEST':
        return f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp}'
    elif action == 'MERGE':
        return f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {timestamp}'
    
    return f'{author} performed {action} on {timestamp}'
