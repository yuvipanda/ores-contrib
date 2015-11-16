import requests


ORES_URL = 'https://ores.wmflabs.org'


class MappingResponse:
    def __init__(self, model, revids, mapping):
        self.model = model
        self.revids = revids
        self.mapping = mapping

    def realize(self, dbname):
        url = '{base}/scores/{dbname}/?models={model}&revids={revids}'.format(
            base=ORES_URL,
            dbname=dbname,
            model=self.model,
            revids='|'.join([str(r) for r in self.revids])
        )
        response = requests.get(url).json()
        return {
            'mapping': self.mapping,
            'ores': response
        }
