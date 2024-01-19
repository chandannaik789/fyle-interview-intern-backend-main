@app.route('/principal/teachers', methods=['GET'])
def get_principal_teachers():
    principal_id = get_principal_id_from_headers(request.headers)
    teachers = get_teachers_for_principal(principal_id)
    return jsonify({"data": teachers})