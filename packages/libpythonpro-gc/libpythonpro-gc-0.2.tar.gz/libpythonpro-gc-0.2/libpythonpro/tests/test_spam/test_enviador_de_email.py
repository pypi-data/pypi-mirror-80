import pytest

from libpythonpro.spam.enviador_de_email import Enviador, EmailInvalido


def test_criar_enviador_de_email():
    enviador = Enviador()
    assert enviador is not None


@pytest.mark.parametrize(
    'destinatario',
    ['foo@bar.com.br', 'augustoge71@gmail.com'],
)
def test_remetente(destinatario):
    enviador = Enviador()
    resultado = enviador.enviar(
        destinatario,
        'cgetulioaugusto@yahoo.com.br',
        'Curso Python Pro',
        'Turma Luiz Vital aberta e em andamento.'
    )
    assert destinatario in resultado


@pytest.mark.parametrize(
    'remetente',
    ['', 'augustoge71'],
)
def test_remetente_invalido(remetente):
    enviador = Enviador()
    with pytest.raises(EmailInvalido):
        enviador.enviar(
            remetente,
            'cgetulioaugusto@yahoo.com.br',
            'Curso Python Pro',
            'Turma Luiz Vital aberta e em andamento.'
        )
