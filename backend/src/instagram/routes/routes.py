from flask import current_app as application
from core import token_required
from flask import jsonify, make_response

@application.route('/api/instagram/find', methods=['POST'])
@token_required
def upload_data():
    return make_response(jsonify({'success': True}), 200, {'ContentType': 'application/json'})
