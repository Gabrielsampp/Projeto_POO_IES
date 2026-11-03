
import pytest

from src.papeis.criador import Criador
from src.usuario.professor import Professor
from src.quiz.quiz import Quiz
from src.quiz.pergunta import Pergunta
from src.tema.tema import Tema


def criar_quiz():
    tema = Tema("Programação")
    pergunta = Pergunta(
        tema,
        "O que é Python?",
        ["Linguagem", "Hardware", "Sistema"],
        0,
        "F"
    )
    return Quiz("Quiz de Python", [pergunta])


def criar_professor():
    return Professor("Ana", "ana@email.com", "P001")


def test_professor_herda_de_criador():
    professor = criar_professor()
    assert isinstance(professor, Criador)


def test_criar_quiz():
    professor = criar_professor()
    quiz = criar_quiz()

    professor.adicionar_quiz(quiz)

    assert quiz in professor.quizzes
    assert quiz.professor is professor


def test_impedir_quiz_duplicado():
    professor = criar_professor()
    quiz = criar_quiz()

    professor.adicionar_quiz(quiz)

    with pytest.raises(ValueError):
        professor.adicionar_quiz(quiz)


def test_impedir_quiz_de_outro_criador():
    professor1 = criar_professor()
    professor2 = Professor("Carlos", "carlos@email.com", "P002")
    quiz = criar_quiz()

    professor1.adicionar_quiz(quiz)

    with pytest.raises(ValueError):
        professor2.adicionar_quiz(quiz)


def test_impedir_adicionar_objeto_invalido():
    professor = criar_professor()

    with pytest.raises(TypeError):
        professor.adicionar_quiz("Não é um quiz")


def test_historico_de_quizzes_nao_permite_alteracao_direta():
    professor = criar_professor()

    with pytest.raises(AttributeError):
        professor.quizzes.append(criar_quiz())
