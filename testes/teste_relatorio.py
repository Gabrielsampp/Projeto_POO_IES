import pytest

from src.relatorio.relatorio import Relatorio
from src.tema.tema import Tema
from src.quiz.pergunta import Pergunta
from src.quiz.quiz import Quiz
from src.usuario.aluno import Aluno
from src.usuario.professor import Professor
from src.tentativa.tentativa import Tentativa


def criar_quiz():
    tema = Tema("Programação")

    perguntas = [
        Pergunta(
            tema,
            f"Pergunta {i}",
            ["Alternativa A", "Alternativa B", "Alternativa C"],
            0,
            "F"
        )
        for i in range(10)
    ]

    return Quiz("Quiz de teste", perguntas)


def criar_participante(nome="Ana", identificador="A001"):
    return Aluno(nome, f"{identificador}@email.com", identificador)


def criar_tentativa(participante, quiz, quantidade_acertos):
    tentativa = Tentativa(participante, quiz)

    for i in range(len(quiz)):
        indice = 0 if i < quantidade_acertos else 1
        tentativa.registrar_resposta(i, indice)

    tentativa.finalizar()
    return tentativa


def test_relatorio_rejeita_dados_invalidos():
    with pytest.raises(TypeError):
        Relatorio(10)


def test_taxa_aprovacao():
    quiz = criar_quiz()
    aluno1 = criar_participante("Ana", "A001")
    aluno2 = criar_participante("Carlos", "A002")

    t1 = criar_tentativa(aluno1, quiz, 8)
    t2 = criar_tentativa(aluno2, quiz, 6)

    relatorio = Relatorio([t1, t2])

    assert relatorio.taxa_aprovacao() == 50.0


def test_taxa_aprovacao_sem_tentativas():
    relatorio = Relatorio([])

    assert relatorio.taxa_aprovacao() == 0.0


def test_distribuicao_notas():
    quiz = criar_quiz()
    aluno1 = criar_participante("Ana", "A001")
    aluno2 = criar_participante("Carlos", "A002")

    t1 = criar_tentativa(aluno1, quiz, 0)
    t2 = criar_tentativa(aluno2, quiz, 8)

    distribuicao = Relatorio([t1, t2]).distribuicao_notas()

    assert distribuicao["0"] == 1
    assert distribuicao["71-80"] == 1
    assert sum(distribuicao.values()) == 2


def test_top_n_por_media_desempenho():
    quiz = criar_quiz()
    aluno1 = criar_participante("Ana", "A001")
    aluno2 = criar_participante("Carlos", "A002")

    t1 = criar_tentativa(aluno1, quiz, 6)
    t2 = criar_tentativa(aluno2, quiz, 9)

    ranking = Relatorio([t1, t2]).top_n_por_media_desempenho(1)

    assert len(ranking) == 1
    assert ranking[0]["participante"] is aluno2
    assert ranking[0]["media_desempenho"] == 90.0


def test_ranking_nao_inclui_professor():
    quiz = criar_quiz()
    professor = Professor("Paulo", "paulo@email.com", "P001")

    tentativa = criar_tentativa(professor, quiz, 10)

    ranking = Relatorio([tentativa]).top_n_por_media_desempenho()

    assert ranking == []


def test_desempenho_por_tema():
    quiz = criar_quiz()
    aluno = criar_participante()

    tentativa = criar_tentativa(aluno, quiz, 7)

    resultado = Relatorio([tentativa]).desempenho_por_tema()

    assert len(resultado) == 1
    assert resultado[0]["tema"] == "Programação"
    assert resultado[0]["acertos"] == 7
    assert resultado[0]["respostas"] == 10
    assert resultado[0]["taxa_acerto"] == 70.0


def test_questoes_mais_erradas():
    quiz = criar_quiz()
    aluno = criar_participante()

    tentativa = criar_tentativa(aluno, quiz, 5)

    resultado = Relatorio([tentativa]).questoes_mais_erradas(3)

    assert len(resultado) == 3
    assert resultado[0]["erros"] == 1
    assert resultado[0]["taxa_erro"] == 100.0


def test_evolucao_usuario():
    quiz = criar_quiz()
    aluno = criar_participante()

    t1 = criar_tentativa(aluno, quiz, 5)
    t2 = criar_tentativa(aluno, quiz, 8)

    resultado = Relatorio([t1, t2]).evolucao_usuario(aluno)

    assert len(resultado) == 2
    assert resultado[0]["desempenho"] == 50.0
    assert resultado[1]["desempenho"] == 80.0


def test_top_n_rejeita_valor_invalido():
    relatorio = Relatorio([])

    with pytest.raises(ValueError):
        relatorio.top_n_por_media_desempenho(0)

    with pytest.raises(TypeError):
        relatorio.top_n_por_media_desempenho("5")