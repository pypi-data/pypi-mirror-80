from libpythonpro.spam.db import Conexao
from libpythonpro.spam.modelos import Usuario


def conexao_obj():
    return Conexao()


def test_salvar_usuario(sessao):
    usuario = Usuario(nome='Getulio', email='augustoge71@gmail.com')
    sessao.salvar(usuario)
    assert isinstance(usuario.id, int)


def test_listar_usuarios(sessao):
    usuarios = [
        Usuario(nome='Getulio', email='augustoge71@gmail.com'),
        Usuario(nome='Carol', email='augustoge71@gmail.com')
    ]
    for usuario in usuarios:
        sessao.salvar(usuario)
    assert usuarios == sessao.listar()
