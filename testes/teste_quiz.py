import pytest

from src.tema.tema import Tema
from src.quiz.pergunta import Pergunta
from src.quiz.quiz import Quiz
from src.quiz.pergunta_bonus import PerguntaBonus


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


def test_criar_quiz(quiz):
    assert quiz.titulo == "Quiz Python"
    assert len(quiz) == 3


def test_titulo_vazio():
    with pytest.raises(ValueError):
        Quiz("   ")


def test_adicionar_pergunta(quiz):
    nova = Pergunta(
        Tema("Java"),
        "P4",
        ["A", "B", "C"],
        0,
        "F"
    )

    quiz.adicionar_pergunta(nova)

    assert len(quiz) == 4


def test_impedir_pergunta_duplicada(quiz, perguntas):
    with pytest.raises(ValueError):
        quiz.adicionar_pergunta(perguntas[0])


def test_impedir_reutilizacao_em_outro_quiz(perguntas):
    quiz1 = Quiz("Quiz 1", [perguntas[0]])
    quiz2 = Quiz("Quiz 2")

    with pytest.raises(ValueError):
        quiz2.adicionar_pergunta(perguntas[0])


def test_remover_pergunta(quiz, perguntas):
    quiz.remover_pergunta(perguntas[0])

    assert len(quiz) == 2


def test_remover_pergunta_inexistente(quiz):
    outra = Pergunta(
        Tema("Java"),
        "Outra pergunta",
        ["A", "B", "C"],
        0,
        "F"
    )

    with pytest.raises(ValueError):
        quiz.remover_pergunta(outra)


def test_pontuacao_maxima(quiz):
    assert quiz.calcular_pontuacao_maxima() == 6


def test_alterar_ordem(quiz, perguntas):
    quiz.alterar_ordem_perguntas(
        [perguntas[2], perguntas[0], perguntas[1]]
    )

    assert quiz.perguntas[0] is perguntas[2]


def test_ordem_invalida(quiz, perguntas):
    with pytest.raises(ValueError):
        quiz.alterar_ordem_perguntas([perguntas[0]])


def test_iterar_quiz(quiz):
    resultado = list(quiz)

    assert len(resultado) == 3


def test_congelar_quiz(quiz):
    quiz._congelar()

    assert quiz.congelado is True


def test_impedir_edicao_apos_congelamento(quiz):
    quiz._congelar()

    nova = Pergunta(
        Tema("Java"),
        "Outra pergunta",
        ["A", "B", "C"],
        0,
        "F"
    )

    with pytest.raises(ValueError):
        quiz.adicionar_pergunta(nova)


def test_impedir_congelar_quiz_vazio():
    quiz = Quiz("Quiz vazio")

    with pytest.raises(ValueError):
        quiz._congelar()


def test_limite_tempo_invalido():
    with pytest.raises(ValueError):
        Quiz("Quiz", limite_tempo=0)


def test_limite_tentativas_invalido():
    with pytest.raises(ValueError):
        Quiz("Quiz", limite_tentativas=-1)


def test_impedir_alterar_titulo_apos_congelamento(quiz):
    quiz._congelar()
    with pytest.raises(ValueError):
        quiz.titulo = "Novo título"


def test_impedir_alterar_tempo_apos_congelamento(quiz):
    quiz._congelar()
    with pytest.raises(ValueError):
        quiz.limite_tempo = 30


def test_impedir_alterar_tentativas_apos_congelamento(quiz):
    quiz._congelar()
    with pytest.raises(ValueError):
        quiz.limite_tentativas = 5


def test_impedir_alterar_bonus_apos_congelamento(quiz):
    quiz._congelar()
    with pytest.raises(ValueError):
        quiz.valor_bonus = 10

def test_pontuacao_maxima_com_pergunta_bonus():
    tema = Tema("Python")

    normal = Pergunta(
        tema, "Normal", ["A", "B", "C"], 0, "F"
    )

    bonus = PerguntaBonus(
        tema, "Bonus", ["A", "B", "C"], 0, "D"
    )

    quiz = Quiz("Quiz bônus", [normal, bonus])

    assert quiz.calcular_pontuacao_maxima() == 6


def test_pergunta_bonus_calcula_pontuacao():
    bonus = PerguntaBonus(
        Tema("Python"), "Bonus", ["A", "B", "C"], 0, "D"
    )

    assert bonus.calcular_pontuacao() == 5