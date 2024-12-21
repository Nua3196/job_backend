from flask import Blueprint, jsonify, request
from app.models.company_model import Company

company_bp = Blueprint('company', __name__, url_prefix='/api/companies')

@company_bp.route('/', methods=['GET'])
def list_companies():
    """
    ---
    tags:
      - Company
    summary: "List all companies"
    description: "Fetch a list of all companies."
    responses:
      200:
        description: "List of companies fetched successfully."
      500:
        description: "Internal server error."
    """
    try:
        companies = Company.get_all()
        return jsonify(companies), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@company_bp.route('/<int:company_id>', methods=['GET'])
def get_company(company_id):
    """
    ---
    tags:
      - Company
    summary: "Get company details"
    description: "Fetch details of a specific company by its ID."
    parameters:
      - in: path
        name: company_id
        required: true
        schema:
          type: integer
        description: "ID of the company to fetch."
    responses:
      200:
        description: "Company details fetched successfully."
      404:
        description: "Company not found."
      500:
        description: "Internal server error."
    """
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
    """
    ---
    tags:
      - Company
    summary: "Add a new company"
    description: "Create a new company record."
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
                description: "Name of the company."
              link:
                type: string
                description: "Link to the company website."
    responses:
      201:
        description: "Company created successfully."
      400:
        description: "Validation error."
      500:
        description: "Internal server error."
    """
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
    """
    ---
    tags:
      - Company
    summary: "Update company details"
    description: "Update details of an existing company."
    parameters:
      - in: path
        name: company_id
        required: true
        schema:
          type: integer
        description: "ID of the company to update."
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
                description: "New name of the company."
              link:
                type: string
                description: "New link to the company website."
    responses:
      200:
        description: "Company updated successfully."
      400:
        description: "Validation error."
      500:
        description: "Internal server error."
    """
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
    """
    ---
    tags:
      - Company
    summary: "Delete a company"
    description: "Delete a company by its ID."
    parameters:
      - in: path
        name: company_id
        required: true
        schema:
          type: integer
        description: "ID of the company to delete."
    responses:
      200:
        description: "Company deleted successfully."
      400:
        description: "Validation error."
      500:
        description: "Internal server error."
    """
    try:
        result = Company.delete(company_id)
        if "error" in result:
            return jsonify(result), 400
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
