""" Recovery group pages API: content for the site's page about each program that meets at the center (model/program.py)

GET /api/programs          every group {slug, name, short, image}
GET /api/programs/<slug>   one group's page {slug, name, short, image, intro, sections, source_url}
"""
from flask import Blueprint
from flask_restful import Api, Resource

from model.program import program_list, program


program_api = Blueprint('program_api', __name__, url_prefix='/api')
api = Api(program_api)


class ProgramAPI:
    class _List(Resource):
        def get(self):
            return program_list()

    class _One(Resource):
        def get(self, slug):
            page = program(slug)
            if page is None:
                return {"message": "That recovery group wasn't found"}, 404
            return page

    api.add_resource(_List, '/programs')
    api.add_resource(_One, '/programs/<string:slug>')
