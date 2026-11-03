
from datetime import datetime, timedelta

import pytest

from src.usuario.aluno import Aluno
from src.usuario.professor import Professor
from src.quiz.quiz import Quiz
from src.tema.tema import Tema
from src.quiz.pergunta import Pergunta
from src.tentativa.resposta import Resposta
from src.tentativa.tentativa import Tentativa


@pytest.fixture
def perguntas():
    tema = Tema("Python")

    return [
        Pergunta(tema, "P1", ["A", "B", "C"], 0, "F"),
        Pergunta(tema, "P2", ["A", "B", "C"], 1, "M"),
        Pergunta(tema, "P3", ["A", "B", "C"], 2, "D")
    ]


@pytest.fixture
def quiz(perguntas):
    return Quiz("Quiz Python", perguntas)


@pytest.fixture
def aluno():
    return Aluno("Ana", "ana@email.com", "001")


@pytest.fixture
def tentativa(aluno, quiz):
    return Tentativa(aluno, quiz)


def test_criar_resposta(perguntas):
    resposta = Resposta(perguntas[0], 0)

    assert resposta.indice_alternativa == 0


def test_resposta_correta(perguntas):
    resposta = Resposta(perguntas[0], 0)

    assert resposta.correta is True


def test_resposta_incorreta(perguntas):
    resposta = Resposta(perguntas[0], 1)

    assert resposta.correta is False


def test_pontuacao_resposta_correta(perguntas):
    resposta = Resposta(perguntas[1], 1)

    assert resposta.pontuacao == 2


def test_pontuacao_resposta_incorreta(perguntas):
    resposta = Resposta(perguntas[1], 0)

    assert resposta.pontuacao == 0


def test_resposta_com_pergunta_invalida():
    with pytest.raises(TypeError):
        Resposta("Pergunta", 0)


def test_resposta_com_indice_invalido(perguntas):
    with pytest.raises(IndexError):
        Resposta(perguntas[0], 5)


def test_resposta_com_indice_nao_inteiro(perguntas):
    with pytest.raises(TypeError):
        Resposta(perguntas[0], "0")


def test_criar_tentativa(tentativa, aluno):
    assert tentativa.participante is aluno
    assert tentativa.status == "em andamento"


def test_registrar_resposta(tentativa):
    resposta = tentativa.registrar_resposta(0, 0)

    assert resposta.correta is True
    assert 0 in tentativa.respostas


def test_impedir_resposta_duplicada(tentativa):
    tentativa.registrar_resposta(0, 0)

    with pytest.raises(ValueError):
        tentativa.registrar_resposta(0, 1)


def test_impedir_pergunta_inexistente(tentativa):
    with pytest.raises(IndexError):
        tentativa.registrar_resposta(10, 0)


def test_calcular_pontuacao_total(tentativa):
    tentativa.registrar_resposta(0, 0)
    tentativa.registrar_resposta(1, 1)
    tentativa.registrar_resposta(2, 0)

    assert tentativa.pontuacao == 3


def test_calcular_acertos(tentativa):
    tentativa.registrar_resposta(0, 0)
    tentativa.registrar_resposta(1, 1)
    tentativa.registrar_resposta(2, 0)

    assert tentativa.acertos == 2


def test_calcular_taxa_de_acerto(tentativa):
    tentativa.registrar_resposta(0, 0)
    tentativa.registrar_resposta(1, 1)

    assert tentativa.taxa_acerto == 100


def test_taxa_de_acerto_sem_respostas(tentativa):
    assert tentativa.taxa_acerto == 0


def test_finalizar_tentativa_completa(tentativa):
    tentativa.registrar_resposta(0, 0)
    tentativa.registrar_resposta(1, 1)
    tentativa.registrar_resposta(2, 2)

    tentativa.finalizar()

    assert tentativa.status == "concluida"
    assert tentativa.completa is True
    assert tentativa.data_fim is not None


def test_finalizar_tentativa_incompleta(tentativa):
    tentativa.registrar_resposta(0, 0)

    tentativa.finalizar()

    assert tentativa.status == "incompleta"
    assert tentativa.completa is False


def test_impedir_responder_apos_finalizar(tentativa):
    tentativa.finalizar()

    with pytest.raises(ValueError):
        tentativa.registrar_resposta(0, 0)


def test_impedir_finalizar_duas_vezes(tentativa):
    tentativa.finalizar()

    with pytest.raises(ValueError):
        tentativa.finalizar()


def test_tentativa_tem_duracao(tentativa):
    assert tentativa.duracao >= 0


def test_encerrar_por_tempo_excedido(aluno, perguntas):
    quiz = Quiz("Quiz com tempo", perguntas, limite_tempo=1)
    tentativa = Tentativa(aluno, quiz)

    tentativa._data_inicio = datetime.now() - timedelta(minutes=2)

    with pytest.raises(ValueError):
        tentativa.registrar_resposta(0, 0)

    assert tentativa.status == "incompleta"
    assert tentativa.data_fim is not None


def test_primeira_tentativa_de_aluno_congela_quiz(aluno, quiz):
    assert quiz.congelado is False

    Tentativa(aluno, quiz)

    assert quiz.congelado is True


def test_professor_nao_congela_quiz(perguntas):
    professor = Professor("João", "joao@email.com", "P001")
    quiz = Quiz("Quiz", perguntas)

    Tentativa(professor, quiz)

    assert quiz.congelado is False
