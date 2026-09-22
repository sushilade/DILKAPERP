import os
import json
import base64
import requests
import threading
from flask import Flask, request, jsonify

app = Flask(__name__)

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
REPO = 'sushilade/DILKAPERP'
BRANCH = 'main'
DATA_FILE = 'data/colleges.json'
GITHUB_API = 'https://api.github.com'

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.after_request
def after_request(response):
    return add_cors_headers(response)

@app.route('/api/colleges', methods=['OPTIONS'])
def options():
    return '', 200

def get_file_data():
    url = f'https://raw.githubusercontent.com/{REPO}/{BRANCH}/{DATA_FILE}'
    resp = requests.get(url)
    if resp.status_code == 200 and resp.text.strip():
        try:
            return resp.json()
        except json.JSONDecodeError:
            pass
    return {"profile": None, "colleges": []}

def get_file_sha():
    url = f'{GITHUB_API}/repos/{REPO}/contents/{DATA_FILE}?ref={BRANCH}'
    resp = requests.get(url, headers={'Authorization': f'token {GITHUB_TOKEN}', 'Accept': 'application/vnd.github+json'})
    if resp.status_code == 200:
        return resp.json().get('sha')
    return None

def save_file_data(data):
    sha = get_file_sha()
    content = json.dumps(data, indent=2)
    content_b64 = base64.b64encode(content.encode()).decode()
    url = f'{GITHUB_API}/repos/{REPO}/contents/{DATA_FILE}'
    resp = requests.put(url,
        headers={'Authorization': f'token {GITHUB_TOKEN}', 'Accept': 'application/vnd.github+json'},
        json={'message': 'Update college data', 'content': content_b64, 'sha': sha, 'branch': BRANCH})
    return resp.status_code == 200

@app.route('/api/colleges', methods=['GET'])
def list_colleges():
    data = get_file_data()
    return jsonify(data['colleges'])

@app.route('/api/colleges', methods=['POST'])
def add_college():
    req = request.get_json()
    data = get_file_data()
    if not data.get('colleges'):
        data['colleges'] = []
    new_id = max([c.get('id', 0) for c in data['colleges']], default=0) + 1
    college = {**req, 'id': new_id}
    data['colleges'].append(college)
    if save_file_data(data):
        return jsonify(college), 201
    return jsonify({'error': 'Failed to save'}), 500

@app.route('/api/colleges/<int:college_id>', methods=['GET'])
def get_college(college_id):
    data = get_file_data()
    for c in data.get('colleges', []):
        if c.get('id') == college_id:
            return jsonify(c)
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/colleges/<int:college_id>', methods=['PUT'])
def update_college(college_id):
    req = request.get_json()
    data = get_file_data()
    for c in data.get('colleges', []):
        if c.get('id') == college_id:
            c.update(req)
            if save_file_data(data):
                return jsonify(c)
            return jsonify({'error': 'Failed to save'}), 500
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/colleges/<int:college_id>', methods=['DELETE'])
def delete_college(college_id):
    data = get_file_data()
    colleges = data.get('colleges', [])
    data['colleges'] = [c for c in colleges if c.get('id') != college_id]
    if save_file_data(data):
        return jsonify({'success': True})
    return jsonify({'error': 'Failed to delete'}), 500

@app.route('/api/profile', methods=['GET'])
def get_profile():
    data = get_file_data()
    profile = data.get('profile')
    if not profile:
        profile = {
            'college_name': 'Dilkap College of Engineering',
            'college_address': 'Plot No. 123, Knowledge Park V, Greater Noida, Uttar Pradesh 201306, India',
            'college_contact_number': '+91-120-1234-5678',
            'expiry_date': '2025-12-31'
        }
        data['profile'] = profile
        save_file_data(data)
    return jsonify(profile)

@app.route('/api/profile', methods=['PUT'])
def update_profile():
    req = request.get_json()
    data = get_file_data()
    data['profile'] = req
    if save_file_data(data):
        return jsonify(req)
    return jsonify({'error': 'Failed to save'}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
