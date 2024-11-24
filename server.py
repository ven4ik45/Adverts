import json

import flask
from flask import Flask
from flask import jsonify, request
from flask.views import MethodView
from models import Adverts, Session
from sqlalchemy.exc import IntegrityError

app = Flask("adverts")


class HttpError(Exception):
    def __init__(self, status_code: int, error_msg: str|dict|list):
        self.status_code = status_code
        self.error_msg = error_msg


@app.errorhandler(HttpError)
def http_error_handler(error: HttpError):
    http_response = jsonify({"status": "error", "msg": error.error_msg})
    http_response.status = error.status_code
    return http_response


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(http_response: flask.Response):
    request.session.close()
    return http_response


def create_advert(advert: Adverts):
    try:
        request.session.add(advert)
        request.session.commit()
    except IntegrityError:
        raise HttpError(
            status_code=409,
            error_msg="Advert with this name has already been created"
        )
    return advert


def get_advert(advert_id: int):
    advert = request.session.get(Adverts, advert_id)
    if advert is None:
        raise HttpError(status_code=404, error_msg="advert not found")
    return advert


class AdvertsView(MethodView):
    def get(self, advert_id: int = None):
        if advert_id:
            advert = get_advert(advert_id)
            return jsonify(advert.json)
        else:
            all_advert = request.session.query(Adverts).all()
            adverts = []
            if not all_advert:
                raise HttpError(404, "No adverts created yet")
            for value in all_advert:
                advert = {"title": value.json["title"], "id": value.json["id"]}
                adverts.append(advert)
            return jsonify(adverts)

    def post(self):
        json_data = request.json
        advert = Adverts(**json_data)
        advert = create_advert(advert)
        return jsonify({"status": "created", "id": advert.id, "date": advert.title})

    def delete(self, advert_id: int):
        advert = get_advert(advert_id)
        request.session.delete(advert)
        request.session.commit()
        return jsonify({"status": "deleted"})


advert_view = AdvertsView.as_view("adverts")

app.add_url_rule("/create_advert", view_func=advert_view, methods=["POST"])
app.add_url_rule("/list_adverts", view_func=advert_view, methods=["GET"])
app.add_url_rule("/advert/<int:advert_id>", view_func=advert_view, methods=["GET", "DELETE"])


app.run()
