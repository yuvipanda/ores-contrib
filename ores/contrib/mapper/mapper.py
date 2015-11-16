import json
import flask
import mwapi

from ores.contrib.mapper import MappingError

host_mapper = {
    'enwiki': 'https://en.wikipedia.org',
}

ORES_URL = 'https://ores.wmflabs.org'


class Mapper:
    """
    A simple interface to map anything into a list of revids

    It takes as input an arbitrary dictionary (args) and sends out
    as output a MapperResponse, which contains:

        - a model name
        - a list of revids
        - a 'mapping' of some input key to the revids

    """
    def run(self, api, args):
        raise NotImplementedError()

    def view_func(self, dbname):
        api = mwapi.Session(host_mapper[dbname])
        try:
            data = self.run(api, flask.request.args).realize(dbname)
        except MappingError as e:
            data = {
                'error': {
                    'code': e.code,
                    'message': e.message,
                    }
                }

        return flask.Response(
            response=json.dumps(data),
            mimetype='application/json'
        )
