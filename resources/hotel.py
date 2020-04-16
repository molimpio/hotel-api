from flask_restful import Resource

hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'Alpha Hotel',
        'estrelas': 1.3,
        'diaria': 120.34,
        'cidade': 'São Paulo'
    },
    {
        'hotel_id': 'bravo',
        'nome': 'Bravo Hotel',
        'estrelas': 4.7,
        'diaria': 490.34,
        'cidade': 'Belo Horizonte'
    },
    {
        'hotel_id': 'charlie',
        'nome': 'Charlie Hotel',
        'estrelas': 2.3,
        'diaria': 220.34,
        'cidade': 'Rio de Janeiro'
    }
]


class Hoteis(Resource):
    def get(self):
        return {'hoteis': hoteis}