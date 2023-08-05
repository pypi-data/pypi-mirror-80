from fittrackee import appLog, db
from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from ..users.models import User
from ..users.utils import authenticate, authenticate_as_admin
from .models import Sport

sports_blueprint = Blueprint('sports', __name__)


@sports_blueprint.route('/sports', methods=['GET'])
@authenticate
def get_sports(auth_user_id):
    """
    Get all sports

    **Example request**:

    .. sourcecode:: http

      GET /api/sports HTTP/1.1
      Content-Type: application/json

    **Example response**:

    - for non admin user :

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "data": {
          "sports": [
            {
              "id": 1,
              "img": "/img/sports/cycling-sport.png",
              "is_active": true,
              "label": "Cycling (Sport)"
            },
            {
              "id": 2,
              "img": "/img/sports/cycling-transport.png",
              "is_active": true,
              "label": "Cycling (Transport)"
            },
            {
              "id": 3,
              "img": "/img/sports/hiking.png",
              "is_active": true,
              "label": "Hiking"
            },
            {
              "id": 4,
              "img": "/img/sports/mountain-biking.png",
              "is_active": true,
              "label": "Mountain Biking"
            },
            {
              "id": 5,
              "img": "/img/sports/running.png",
              "is_active": true,
              "label": "Running"
            },
            {
              "id": 6,
              "img": "/img/sports/walking.png",
              "is_active": true,
              "label": "Walking"
            }
          ]
        },
        "status": "success"
      }

    - for admin user :

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "data": {
          "sports": [
            {
              "has_activities": true,
              "id": 1,
              "img": "/img/sports/cycling-sport.png",
              "is_active": true,
              "label": "Cycling (Sport)"
            },
            {
              "has_activities": false,
              "id": 2,
              "img": "/img/sports/cycling-transport.png",
              "is_active": true,
              "label": "Cycling (Transport)"
            },
            {
              "has_activities": false,
              "id": 3,
              "img": "/img/sports/hiking.png",
              "is_active": true,
              "label": "Hiking"
            },
            {
              "has_activities": false,
              "id": 4,
              "img": "/img/sports/mountain-biking.png",
              "is_active": true,
              "label": "Mountain Biking"
            },
            {
              "has_activities": false,
              "id": 5,
              "img": "/img/sports/running.png",
              "is_active": true,
              "label": "Running"
            },
            {
              "has_activities": false,
              "id": 6,
              "img": "/img/sports/walking.png",
              "is_active": true,
              "label": "Walking"
            }
          ]
        },
        "status": "success"
      }

    :param integer auth_user_id: authenticate user id (from JSON Web Token)

    :reqheader Authorization: OAuth 2.0 Bearer Token

    :statuscode 200: success
    :statuscode 401:
        - Provide a valid auth token.
        - Signature expired. Please log in again.
        - Invalid token. Please log in again.

    """

    user = User.query.filter_by(id=int(auth_user_id)).first()
    sports = Sport.query.order_by(Sport.id).all()
    response_object = {
        'status': 'success',
        'data': {'sports': [sport.serialize(user.admin) for sport in sports]},
    }
    return jsonify(response_object), 200


@sports_blueprint.route('/sports/<int:sport_id>', methods=['GET'])
@authenticate
def get_sport(auth_user_id, sport_id):
    """
    Get a sport

    **Example request**:

    .. sourcecode:: http

      GET /api/sports/1 HTTP/1.1
      Content-Type: application/json

    **Example response**:

    - success for non admin user :

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "data": {
          "sports": [
            {
              "id": 1,
              "img": "/img/sports/cycling-sport.png",
              "is_active": true,
              "label": "Cycling (Sport)"
            }
          ]
        },
        "status": "success"
      }

    - success for admin user :

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "data": {
          "sports": [
            {
              "has_activities": false,
              "id": 1,
              "img": "/img/sports/cycling-sport.png",
              "is_active": true,
              "label": "Cycling (Sport)"
            }
          ]
        },
        "status": "success"
      }

    - sport not found

    .. sourcecode:: http

      HTTP/1.1 404 NOT FOUND
      Content-Type: application/json

      {
        "data": {
          "sports": []
        },
        "status": "not found"
      }

    :param integer auth_user_id: authenticate user id (from JSON Web Token)
    :param integer sport_id: sport id

    :reqheader Authorization: OAuth 2.0 Bearer Token

    :statuscode 200: success
    :statuscode 401:
        - Provide a valid auth token.
        - Signature expired. Please log in again.
        - Invalid token. Please log in again.
    :statuscode 404: sport not found

    """

    user = User.query.filter_by(id=int(auth_user_id)).first()
    sport = Sport.query.filter_by(id=sport_id).first()
    if sport:
        response_object = {
            'status': 'success',
            'data': {'sports': [sport.serialize(user.admin)]},
        }
        code = 200
    else:
        response_object = {'status': 'not found', 'data': {'sports': []}}
        code = 404
    return jsonify(response_object), code


@sports_blueprint.route('/sports/<int:sport_id>', methods=['PATCH'])
@authenticate_as_admin
def update_sport(auth_user_id, sport_id):
    """
    Update a sport
    Authenticated user must be an admin

    **Example request**:

    .. sourcecode:: http

      PATCH /api/sports/1 HTTP/1.1
      Content-Type: application/json

    **Example response**:

    - success

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "data": {
          "sports": [
            {
              "has_activities": false,
              "id": 1,
              "img": "/img/sports/cycling-sport.png",
              "is_active": false,
              "label": "Cycling (Sport)"
            }
          ]
        },
        "status": "success"
      }

    - sport not found

    .. sourcecode:: http

      HTTP/1.1 404 NOT FOUND
      Content-Type: application/json

      {
        "data": {
          "sports": []
        },
        "status": "not found"
      }

    :param integer auth_user_id: authenticate user id (from JSON Web Token)
    :param integer sport_id: sport id

    :<json string is_active: sport active status

    :reqheader Authorization: OAuth 2.0 Bearer Token

    :statuscode 200: sport updated
    :statuscode 400: invalid payload
    :statuscode 401:
        - Provide a valid auth token.
        - Signature expired. Please log in again.
        - Invalid token. Please log in again.
    :statuscode 403: You do not have permissions.
    :statuscode 404: sport not found
    :statuscode 500:

    """
    sport_data = request.get_json()
    if not sport_data or sport_data.get('is_active') is None:
        response_object = {'status': 'error', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400

    try:
        sport = Sport.query.filter_by(id=sport_id).first()
        if sport:
            sport.is_active = sport_data.get('is_active')
            db.session.commit()
            response_object = {
                'status': 'success',
                'data': {'sports': [sport.serialize(True)]},
            }
            code = 200
        else:
            response_object = {'status': 'not found', 'data': {'sports': []}}
            code = 404
    except (exc.IntegrityError, exc.OperationalError, ValueError) as e:
        db.session.rollback()
        appLog.error(e)
        response_object = {
            'status': 'error',
            'message': 'Error. Please try again or contact the administrator.',
        }
        code = 500
    return jsonify(response_object), code
