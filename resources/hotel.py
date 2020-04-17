from flask_restful import Resource, reqparse

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


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('cidade')
    argumentos.add_argument('diaria')

    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None

    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message': 'Hotel não encontrado'}, 404

    def post(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        novo_hotel = {'hotel_id': hotel_id, **dados}

        hoteis.append(novo_hotel)
        return novo_hotel, 201

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        novo_hotel = {'hotel_id': hotel_id, **dados}

        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200

        hoteis.append(novo_hotel)
        return novo_hotel, 201

    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': 'Hotel removido com sucesso'}
