import flask

from ores.contrib.mapper import Mapper, MappingResponse, MappingError

app = flask.Flask(__name__)


# FIXME: Move this out to a seperate file somewhere else
# FIXME: Set this up to be able to autogenerate docs somehow
class WP10PageMapper(Mapper):
    TYPE = 'page'
    NAME = 'wp10'

    def run(self, api, args):
        if 'titles' in args:
            # FIXME: Throw up if we have too many titles or pageids
            page_args = {'titles': args.get('titles')}
            response_key = 'title'
        elif 'pageids' in args:
            page_args = {'pageids': args.get('pageids')}
            response_key = 'pageid'
        else:
            pass  # FIXME: Raise an appropriate error here

        resp = api.get(
            action='query', prop='revisions',
            rvprop='ids', formatversion='2', **page_args
        )
        meta = {}
        for page in resp['query']['pages']:
            if 'missing' in page:
                meta[page[response_key]] = None
            else:
                meta[page[response_key]] = page['revisions'][0]['revid']

        if not any(meta.values()):
            # There were no legit revids
            raise MappingError('noexist', 'No revision ids found for the given request')

        return MappingResponse(
            'wp10',
            [rev for rev in meta.values() if rev is not None],
            meta
        )


def register_mapping(mapping_class):
    route = '/{type}/{name}/<string:dbname>'.format(
        type=mapping_class.TYPE,
        name=mapping_class.NAME
    )
    app.add_url_rule(route, view_func=mapping_class().view_func)


register_mapping(WP10PageMapper)

if __name__ == '__main__':
    app.run(debug=True)
