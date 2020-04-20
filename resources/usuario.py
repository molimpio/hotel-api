from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import safe_str_cmp

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="Campo login é obrigatório")
atributos.add_argument('senha', type=str, required=True, help="Campo senha é obrigatório")


class User(Resource):
    # /usuarios/user_id
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'Usuário não encontrado'}, 404

    @jwt_required
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
        dados = atributos.parse_args()
        login = dados['login']

        if UserModel.find_by_login(login):
            return {'message': 'Usuário com login {} já existe'.format(login)}, 200

        user = UserModel(**dados)
        user.save_user()
        return {'message': 'Usuário cadastrado com sucesso'}, 201


class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            token = create_access_token(identity=user.user_id)
            return {'access_token': token}, 200
        return {'message': 'Dados incorretos'}, 401
