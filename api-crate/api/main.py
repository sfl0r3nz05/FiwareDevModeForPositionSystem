import os
import uuid
import base64
import hashlib

from datetime import datetime
from tempfile import TemporaryFile

from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

from crate.client import connect

from flask import (
    Flask,
    g as app_globals,
    make_response,
    jsonify
)

from flask_restful import Api, Resource
from flask_restful import reqparse as reqparser
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

# app configuration
CRATE_HOST = os.environ['CRATE_HOST_PORT']
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5mb because GIFs are big ;)

# create Flask app
app = Flask(__name__)
app.config.from_object(__name__)
# apply CORS headers to all responses
CORS(app)

class CrateResource(Resource):

    __name__ = ''
    __table__ = ''

    def __init__(self):
        super(CrateResource, self).__init__()
        self.cursor = self.connection.cursor()

    @property
    def connection(self):
        if not 'conn' in app_globals:
            app_globals.conn = connect(app.config['CRATE_HOST'],
                                       error_trace=True)
        return app_globals.conn

    def error(self, message, status=404):
        return (dict(
            error=message,
            status=status,
        ), status)

    def refresh_table(self):
        self.cursor.execute("REFRESH TABLE {}".format(self.__table__))

    def convert(self, description, results):
        cols = [c[0] for c in description]
        return [dict(zip(cols, r)) for r in results]

    def not_found(self, **kw):
        keys = ', '.join(('{}="{}"'.format(k,v) for k,v in kw.items()))
        return self.error('{} with {} not found'.format(self.__name__, keys), 404)

    def argument_required(self, argument):
        return self.error('Argument "{}" is required'.format(argument), 400)


class GetAgvResource(CrateResource):

    __name__ = 'GetAgvList'
    __table__ = 'mtopeniot.etagv'


class GetRobotArmResource(CrateResource):

    __name__ = 'GetRobotArmList'
    __table__ = 'mtopeniot.etrobotarm'


class GetPlcResource(CrateResource):

    __name__ = 'GetPlcList'
    __table__ = 'mtopeniot.etplc'


class GetAgvList(GetAgvResource):
    """
    Resource for mtopeniot.etagv
    Supported methods: GET
    """

    def get(self):
        id = str(uuid.uuid1())

        self.cursor.execute("SELECT * FROM mtopeniot.etagv")
        response = self.convert(self.cursor.description,
                                self.cursor.fetchall())
        if self.cursor.rowcount > 0:
            return response, 200
        else:
            return self.not_found(id=id)


class GetRobotArmList(GetRobotArmResource):
    """
    Resource for mtopeniot.etrobotarm
    Supported methods: GET
    """

    def get(self):
        id = str(uuid.uuid1())

        self.cursor.execute("SELECT * FROM mtopeniot.etrobotarm")
        response = self.convert(self.cursor.description,
                                self.cursor.fetchall())
        if self.cursor.rowcount > 0:
            return response, 200
        else:
            return self.not_found(id=id)


class GetPlcList(GetPlcResource):
    """
    Resource for mtopeniot.etplc
    Supported methods: GET
    """

    def get(self):
        id = str(uuid.uuid1())

        self.cursor.execute("SELECT * FROM mtopeniot.etplc")
        response = self.convert(self.cursor.description,
                                self.cursor.fetchall())
        if self.cursor.rowcount > 0:
            return response, 200
        else:
            return self.not_found(id=id)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

def run():
    api = Api(app)
    api.add_resource(GetAgvList, '/getAgvs')
    api.add_resource(GetRobotArmList, '/getRobotArms')
    api.add_resource(GetPlcList, '/getPlcs')
    app.run(host='0.0.0.0', port=8080, debug=True, ssl_context='adhoc')

if __name__ == '__main__':
    run()
