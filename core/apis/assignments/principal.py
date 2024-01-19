@app.route('/principal/assignments', methods=['GET'])
def get_principal_assignments():
    principal_id = get_principal_id_from_headers(request.headers)
    assignments = get_assignments_for_principal(principal_id)
    return jsonify({"data": assignments})