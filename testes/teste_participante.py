
import pytest

from src.usuario.aluno import Aluno
from src.usuario.professor import Professor
from src.papeis.participante import Participante
from src.quiz.quiz import Quiz
from src.tema.tema import Tema
from src.quiz.pergunta import Pergunta
from src.tentativa.tentativa import Tentativa


def criar_quiz():
    tema = Tema("Python")
    pergunta = Pergunta(
        tema, "O que é Python?",
        ["Linguagem", "Hardware", "Sistema"],
        0, "F"
    )
    return Quiz("Quiz Python", [pergunta])


def test_aluno_e_participante():
    aluno = Aluno("Ana", "ana@email.com", "001")
    assert isinstance(aluno, Participante)


def test_professor_e_participante():
    professor = Professor("João", "joao@email.com", "P001")
    assert isinstance(professor, Participante)


def test_historico_inicial_vazio():
    aluno = Aluno("Ana", "ana@email.com", "001")
    assert aluno.tentativas == ()


def test_historico_nao_permite_alteracao_direta():
    aluno = Aluno("Ana", "ana@email.com", "001")

    assert isinstance(aluno.tentativas, tuple)


def test_adicionar_tentativa_automaticamente():
    aluno = Aluno("Ana", "ana@email.com", "001")
    quiz = criar_quiz()

    tentativa = Tentativa(aluno, quiz)

    assert tentativa in aluno.tentativas


def test_tentativa_nao_pode_ser_adicionada_a_outro_participante():
    aluno1 = Aluno("Ana", "ana@email.com", "001")
    aluno2 = Aluno("Maria", "maria@email.com", "002")

    tentativa = Tentativa(aluno1, criar_quiz())

    with pytest.raises(ValueError):
        aluno2.adicionar_tentativa(tentativa)


def test_professor_pode_participar():
    professor = Professor("João", "joao@email.com", "P001")

    tentativa = Tentativa(professor, criar_quiz())

    assert tentativa in professor.tentativas


def test_limite_de_tentativas_por_participante():
    aluno = Aluno("Ana", "ana@email.com", "001")
    quiz = criar_quiz()
    quiz.limite_tentativas = 1

    Tentativa(aluno, quiz)

    with pytest.raises(ValueError):
        Tentativa(aluno, quiz)


def test_limite_independente_por_quiz():
    aluno = Aluno("Ana", "ana@email.com", "001")

    quiz1 = criar_quiz()
    quiz1.limite_tentativas = 1

    quiz2 = criar_quiz()
    quiz2.limite_tentativas = 1

    Tentativa(aluno, quiz1)
    tentativa2 = Tentativa(aluno, quiz2)

    assert tentativa2 in aluno.tentativas
