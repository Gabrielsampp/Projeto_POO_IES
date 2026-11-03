
import pytest

from src.tema.tema import Tema
from src.quiz.pergunta import Pergunta


@pytest.fixture
def pergunta():
    tema = Tema("Python")

    return Pergunta(
        tema,
        "Qual é a extensão dos arquivos Python?",
        [".py", ".java", ".cpp"],
        0,
        "F"
    )


def test_criar_pergunta(pergunta):
    assert pergunta.enunciado == "Qual é a extensão dos arquivos Python?"
    assert pergunta.indice_correto == 0


def test_pergunta_sem_enunciado():
    with pytest.raises(ValueError):
        Pergunta(Tema("Python"), "", ["A", "B", "C"], 0, "F")


def test_quantidade_invalida():
    with pytest.raises(ValueError):
        Pergunta(Tema("Python"), "Pergunta?", ["A", "B"], 0, "F")


def test_alternativas_duplicadas():
    with pytest.raises(ValueError):
        Pergunta(Tema("Python"), "Pergunta?", ["A", "a", "B"], 0, "F")


def test_indice_correto_invalido():
    with pytest.raises(ValueError):
        Pergunta(Tema("Python"), "Pergunta?", ["A", "B", "C"], 3, "F")


def test_dificuldade_invalida():
    with pytest.raises(ValueError):
        Pergunta(Tema("Python"), "Pergunta?", ["A", "B", "C"], 0, "X")


def test_calcular_pontuacao(pergunta):
    assert pergunta.calcular_pontuacao() == 1


def test_verificar_resposta(pergunta):
    assert pergunta.verificar_resposta(0) is True
    assert pergunta.verificar_resposta(1) is False


def test_adicionar_alternativa(pergunta):
    pergunta.adicionar_alternativa(".html")
    assert len(pergunta.alternativas) == 4


def test_remover_alternativa(pergunta):
    pergunta.adicionar_alternativa(".html")
    pergunta.remover_alternativa(1)

    assert len(pergunta.alternativas) == 3


def test_alterar_alternativa(pergunta):
    pergunta.alterar_alternativa(1, ".html")

    assert pergunta.alternativas[1] == ".html"


def test_alterar_para_alternativa_duplicada(pergunta):
    with pytest.raises(ValueError):
        pergunta.alterar_alternativa(1, ".PY")


def test_remover_alternativa_correta(pergunta):
    with pytest.raises(ValueError):
        pergunta.remover_alternativa(0)


def test_indice_correto_apos_remocao():
    pergunta = Pergunta(
        Tema("Python"),
        "Pergunta?",
        ["A", "B", "C", "D"],
        2,
        "M"
    )

    pergunta.remover_alternativa(0)

    assert pergunta.indice_correto == 1


def test_alternativas_nao_podem_ser_alteradas_diretamente(pergunta):
    with pytest.raises(TypeError):
        pergunta.alternativas[0] = "Nova alternativa"


def test_igualdade_entre_perguntas():
    tema1 = Tema("Python")
    tema2 = Tema("PYTHON")

    pergunta1 = Pergunta(
        tema1, "O que é Python?", ["A", "B", "C"], 0, "F"
    )

    pergunta2 = Pergunta(
        tema2, "O que é Python?", ["X", "Y", "Z"], 1, "D"
    )

    assert pergunta1 == pergunta2


def test_perguntas_com_enunciados_diferentes():
    tema = Tema("Python")

    pergunta1 = Pergunta(
        tema, "O que é Python?", ["A", "B", "C"], 0, "F"
    )

    pergunta2 = Pergunta(
        tema, "O que é Java?", ["A", "B", "C"], 0, "F"
    )

    assert pergunta1 != pergunta2


def test_pontuacao_por_dificuldade():
    tema = Tema("Python")

    facil = Pergunta(tema, "P1", ["A", "B", "C"], 0, "F")
    media = Pergunta(tema, "P2", ["A", "B", "C"], 0, "M")
    dificil = Pergunta(tema, "P3", ["A", "B", "C"], 0, "D")

    assert facil.calcular_pontuacao() == 1
    assert media.calcular_pontuacao() == 2
    assert dificil.calcular_pontuacao() == 3

def test_alterar_alternativas_sem_invalidar_indice(pergunta):
    pergunta.alternativas = [".py", ".java", ".cpp", ".html"]

    assert len(pergunta.alternativas) == 4


def test_impedir_alteracao_que_invalida_indice():
    pergunta = Pergunta(
        Tema("Python"),
        "Pergunta?",
        ["A", "B", "C", "D", "E"],
        4,
        "F"
    )

    with pytest.raises(ValueError):
        pergunta.alternativas = ["A", "B", "C"]


def test_verificar_resposta_com_indice_inexistente(pergunta):
    with pytest.raises(IndexError):
        pergunta.verificar_resposta(10)


def test_verificar_resposta_com_tipo_invalido(pergunta):
    with pytest.raises(TypeError):
        pergunta.verificar_resposta("0")