from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
from resources.site import SiteModel
from resources.filtros import normalize_path_params, consulta_com_cidade, consulta_sem_cidade
import sqlite3


# Params via query string, ex: /hoteis?cidade=Sao Paulo&estrelas_min=4&diaria_max=400
path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        # Filtra somente os dados que tem valores válidos, diferente de None
        dados_validos = {chave: dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)

        if not parametros.get('cidade'):
            query = consulta_sem_cidade
        else:
            query = consulta_com_cidade

        tupla = tuple([parametros[chave] for chave in parametros])
        resultado = cursor.execute(query, tupla)

        hoteis = []
        for linha in resultado:
            hoteis.append({
                'hotel_id': linha[0],
                'nome': linha[1],
                'estrelas': linha[2],
                'diaria': linha[3],
                'cidade': linha[4],
                'site_id': linha[5]
            })

        return {
                'hoteis': hoteis,
                'total_itens': len(hoteis)
            }


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="Campo nome é obrigatório")
    argumentos.add_argument('estrelas', type=float, required=True, help="Campo estrelas é obrigatório")
    argumentos.add_argument('cidade', type=str, required=True, help="Campo cidade é obrigatório")
    argumentos.add_argument('diaria')
    argumentos.add_argument('site_id', type=int, required=True, help="Campo site id é obrigatório")

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel não encontrado'}, 404

    @jwt_required
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'message': 'Hotel com id {} já existe'.format(hotel_id)}, 400

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)

        if not SiteModel.find_by_id(dados.get('site_id')):
            return {'message': 'Site ID inválido'}, 200
        try:
            hotel.save_hotel()
        except:
            return {'message': 'Erro interno ao tentar salvar hotel'}, 500

        return hotel.json()

    @jwt_required
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()

        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200

        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'Erro interno ao tentar salvar hotel'}, 500
        return hotel.json(), 201

    @jwt_required
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'Erro interno ao tentar excluir hotel'}, 500

            return {'message': 'Hotel removido com sucesso'}, 200
        return {'message': 'Hotel não existe, verifique ID'}, 404
