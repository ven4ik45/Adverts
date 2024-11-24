
import flask
from flask import Flask
from flask import jsonify, request
from flask.views import MethodView
from models import Adverts, Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

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
        raise HttpError(404, "advert not found")
    return advert



class AdvertsView(MethodView):
    def get(self, advert_id: int = None):
        if advert_id:
            advert = get_advert(advert_id)
            return jsonify(advert.json)
        else:
            qs = dict(request.args)
            for key, value in qs.items():
                if key == "all" and value == ("true" or True):
                    all_advert = Session().query(Adverts, Adverts.id, Adverts.title).all()
                    adverts = {}
                    for i in all_advert:
                        adverts[i[1]] = (i[2])
                    if len(adverts) == 0:
                        raise HttpError(404, "No adverts created yet")
                    return adverts

    def post(self):
        json_data = request.json
        advert = Adverts(**json_data)
        advert = create_advert(advert)
        return jsonify({"id": advert.id, "date": advert.data_create})

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
