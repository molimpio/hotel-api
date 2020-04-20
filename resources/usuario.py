from flask_restful import Resource, reqparse
from models.usuario import UserModel


class User(Resource):

    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'Usuário não encontrado'}, 404

    def delete(self, user_id):
        user = UserModel.find_hotel(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'Erro interno ao tentar excluir usuario'}, 500

            return {'message': 'Usuário removido com sucesso'}, 200
        return {'message': 'Usuário não existe, verifique ID'}, 404
