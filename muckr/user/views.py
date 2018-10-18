import flask

from muckr.user.models import User, UserSchema
from muckr.extensions import database
from muckr.errors import error_response


blueprint = flask.Blueprint('user', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)


def _jsonify(data):
    response = flask.jsonify(data)
    response.mimetype = 'application/vnd.api+json'
    return response


@blueprint.route('/users', methods=['GET'])
def get_users():
    page = flask.request.args.get('page', 1, type=int)
    per_page = min(flask.request.args.get('per_page', 10, type=int), 100)
    users = User.query.paginate(page, per_page, False)
    data, errors = users_schema.dump(users.items)
    if errors:
        return error_response(500)
    return _jsonify(data)


@blueprint.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    data, errors = user_schema.dump(user)
    if errors:
        return error_response(500)
    return _jsonify(data)


@blueprint.route('/users', methods=['POST'])
def create_user():
    json = flask.request.get_json() or {}
    data, errors = user_schema.load(json)
    if errors:
        return _jsonify(errors), 422

    password = data.pop('password', None)
    user = User(**data)
    if password is not None:
        user.set_password(password)

    database.session.add(user)
    database.session.commit()

    data, errors = user_schema.dump(user)
    if errors:
        return error_response(500)

    response = _jsonify(data)
    response.status_code = 201
    response.headers['Location'] = flask.url_for('user.get_user', id=user.id)
    return response


@blueprint.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    json = flask.request.get_json() or {}
    data, errors = UserSchema(partial=True).load(json)
    if errors:
        return error_response(500)

    password = data.pop('password', None)
    if password is not None:
        user.set_password(password)

    for key, value in data.items():
        setattr(user, key, value)

    database.session.commit()

    data, errors = UserSchema().dump(user)
    if errors:
        return error_response(500)

    return _jsonify(data)


@blueprint.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    database.session.delete(user)
    database.session.commit()

    return _jsonify({}), 204
