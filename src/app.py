"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")
Jonh = {
    "id": jackson_family._generateId(),
    "first_name": "Jonh",
    "last_name": "Jackson",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
}
jackson_family.add_member(Jonh)

jane = {
    "id": jackson_family._generateId(),
    "first_name": "Jane",
    "last_name": "Jackson",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
}
jackson_family.add_member(jane)

Jimmy = {
    "id": jackson_family._generateId(),
    "first_name": "Jimmy",
    "last_name": "Jackson",
    "age": 5,
    "lucky_numbers": 1
}
jackson_family.add_member(Jimmy)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = members



    return jsonify(response_body), 200

@app.route('/member', methods=['POST'])
def add_member():
    new_member = request.json
    print(new_member, "AQUI ESTOYYYYYYYYYYYYY")
    jackson_family.add_member(new_member)
    return jsonify({"done": "endpoint"}), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_family(member_id):
    eliminar_familiar = jackson_family.delete_member(member_id)
    return jsonify({"done": True}), 200

@app.route('/member/<int:member_id>', methods=['PUT'])
def update_family_member(member_id):
    new_family_member = request.json
    new_member = jackson_family.update_member(member_id, new_family_member)
    if not new_member:
        return jsonify({"msg": "no se encontro al miembro"}), 400
    return jsonify({"done": "miembro Actualizado"})

@app.route('/member/<int:member_id>', methods=['GET'])
def get_one_member(member_id):
    un_miembro_encontrado = jackson_family.get_member(member_id)
    response_body = un_miembro_encontrado
    return jsonify(response_body), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

# {
#     "id": "Int",
#     "first_name": "String",
#     "last_name": "Jackson",
#     "age": 23,
#     "lucky_numbers": [30,12,25]

# }
