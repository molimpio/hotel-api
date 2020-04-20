from flask_restful import Resource, reqparse
from models.usuario import UserModel


class User(Resource):
    # /usuarios/user_id
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'Usuário não encontrado'}, 404

    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'Erro interno ao tentar excluir usuario'}, 500

            return {'message': 'Usuário removido com sucesso'}, 200
        return {'message': 'Usuário não existe, verifique ID'}, 404


class UserRegister(Resource):
    # /cadastro
    def post(self):
        atributos = reqparse.RequestParser()
        atributos.add_argument('login', type=str, required=True, help="Campo login é obrigatório")
        atributos.add_argument('senha', type=str, required=True, help="Campo senha é obrigatório")
        dados = atributos.parse_args()
        login = dados['login']

        if UserModel.find_by_login(login):
            return {'message': 'Usuário com login {} já existe'.format(login)}, 200

        user = UserModel(**dados)
        user.save_user()
        return {'message': 'Usuário cadastrado com sucesso'}, 201
