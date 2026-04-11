from flask import Blueprint, request, jsonify
from app.controller.ip_service import create_ip, get_ips
from app.utils.auth import token_required

ip_bp = Blueprint('ip_bp', __name__)

@ip_bp.route('/ips', methods=['POST'])
@token_required
def post_ip():
    data = request.get_json()
    
    if not data or 'ip' not in data:
        return jsonify({'error': 'Campo "ip" é obrigatório no corpo da requisição.'}), 400
        
    ip_address = data.get('ip')
    
    try:
        result = create_ip(ip_address)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@ip_bp.route('/ips', methods=['GET'])
@token_required
def list_ips():
    try:
        page = int(request.args.get('page', 1))
        limit = min(int(request.args.get('limit', 15)), 15) 
    except ValueError:
        return jsonify({'error': 'Parâmetros page e limit devem ser números inteiros.'}), 400
        
    filter_ip = request.args.get('filter_ip', "")
    
    try:
        results = get_ips(page=page, limit=limit, filter_ip=filter_ip)
        return jsonify({
            'page': page,
            'limit': limit,
            'results': results
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
