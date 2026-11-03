
import pytest

import src.dados as dados

from src.tema.tema import Tema
from src.quiz.pergunta import Pergunta
from src.quiz.quiz import Quiz
from src.usuario.aluno import Aluno
from src.usuario.professor import Professor
from src.tentativa.tentativa import Tentativa


def criar_cenario():
    tema = Tema("Programação")

    perguntas = [
        Pergunta(
            tema,
            f"Pergunta {i}",
            ["A", "B", "C"],
            0,
            "F"
        )
        for i in range(2)
    ]

    professor = Professor(
        "Paulo", "paulo@email.com", "P001"
    )

    aluno = Aluno(
        "Ana", "ana@email.com", "A001"
    )

    quiz = Quiz("Quiz de teste", perguntas)
    professor.adicionar_quiz(quiz)

    tentativa = Tentativa(aluno, quiz)
    tentativa.registrar_resposta(0, 0)
    tentativa.registrar_resposta(1, 1)
    tentativa.finalizar()

    return (
        [tema],
        perguntas,
        [quiz],
        [professor, aluno],
        [tentativa]
    )


def test_salvar_e_carregar_dados(monkeypatch, tmp_path):
    monkeypatch.setattr(dados, "DIRETORIO_DATA", tmp_path)

    dados_originais = criar_cenario()

    dados.salvar_dados(*dados_originais)

    carregados = dados.carregar_dados()

    assert len(carregados["temas"]) == 1
    assert len(carregados["perguntas"]) == 2
    assert len(carregados["quizzes"]) == 1
    assert len(carregados["usuarios"]) == 2
    assert len(carregados["tentativas"]) == 1

    quiz = carregados["quizzes"][0]
    tentativa = carregados["tentativas"][0]

    aluno = next(
        u for u in carregados["usuarios"]
        if isinstance(u, Aluno)
    )

    professor = next(
        u for u in carregados["usuarios"]
        if isinstance(u, Professor)
    )

    assert quiz.congelado is True
    assert quiz.professor is professor
    assert len(professor.quizzes) == 1

    assert tentativa.participante is aluno
    assert tentativa.quiz is quiz
    assert tentativa.completa is True
    assert tentativa.pontuacao == 1
    assert len(aluno.tentativas) == 1

    assert quiz.perguntas[0].quiz is quiz


def test_carregar_dados_vazios(monkeypatch, tmp_path):
    monkeypatch.setattr(dados, "DIRETORIO_DATA", tmp_path)

    resultado = dados.carregar_dados()

    assert resultado == {
        "temas": [],
        "perguntas": [],
        "quizzes": [],
        "usuarios": [],
        "tentativas": []
    }
