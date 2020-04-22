from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="Campo login é obrigatório")
atributos.add_argument('senha', type=str, required=True, help="Campo senha é obrigatório")
atributos.add_argument('ativado', type=bool)


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
        user.ativado = False
        user.save_user()
        return {'message': 'Usuário cadastrado com sucesso'}, 201


class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            if user.ativado:
                token = create_access_token(identity=user.user_id)
                return {'access_token': token}, 200
            return {'message': 'Usuário não está ativado no sistema'}, 200
        return {'message': 'Dados incorretos'}, 401


class UserLogout(Resource):

    @jwt_required
    def post(self):
        # JWT Token Identifier
        jwt_id = get_raw_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Usuário deslogado com sucesso'}, 200


class UserConfirm(Resource):
    # raiz_do_site/confirmacao/{user_id}
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_user(user_id)

        if not user:
            return {'message': 'User ID {} not found'.format(user_id)}, 200

        user.ativado = True
        user.save_user()
        return {'message': 'Usuário confirmado com sucesso'}, 200
