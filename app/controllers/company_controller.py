from flask import Blueprint, jsonify, request
from app.models.company_model import Company

company_bp = Blueprint('company', __name__, url_prefix='/api/companies')

@company_bp.route('/', methods=['GET'])
def list_companies():
    try:
        companies = Company.get_all()
        return jsonify(companies), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@company_bp.route('/<int:company_id>', methods=['GET'])
def get_company(company_id):
    try:
        company = Company.get_by_id(company_id)
        if not company:
            return jsonify({"error": "Company not found"}), 404
        return jsonify(company), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

from app.middlewares.auth import jwt_required

@company_bp.route('/', methods=['POST'])
@jwt_required(required_roles=['admin'])  # 관리자 권한 필요
def add_company():
    try:
        data = request.json
        if not data.get('name') or not data.get('link'):
            return jsonify({"error": "Name and link are required"}), 400
        result = Company.create(data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@company_bp.route('/<int:company_id>', methods=['PUT'])
@jwt_required(required_roles=['admin'])  # 관리자 권한 필요
def update_company(company_id):
    try:
        data = request.json
        result = Company.update(company_id, data)
        if "error" in result:
            return jsonify(result), 400
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@company_bp.route('/<int:company_id>', methods=['DELETE'])
@jwt_required(required_roles=['admin'])  # 관리자 권한 필요
def delete_company(company_id):
    try:
        result = Company.delete(company_id)
        if "error" in result:
            return jsonify(result), 400
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
