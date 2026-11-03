
import json
from pathlib import Path
from datetime import datetime

from src.tema.tema import Tema
from src.quiz.pergunta import Pergunta
from src.quiz.quiz import Quiz
from src.usuario.aluno import Aluno
from src.usuario.professor import Professor
from src.tentativa.tentativa import Tentativa
from src.tentativa.resposta import Resposta


DIRETORIO_DATA = Path(__file__).resolve().parent.parent / "data"


def _ler_json(nome):
    caminho = DIRETORIO_DATA / nome

    if not caminho.exists() or caminho.stat().st_size == 0:
        return []

    try:
        with caminho.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except json.JSONDecodeError as erro:
        raise ValueError(
            f"O arquivo {nome} contém JSON inválido."
        ) from erro

    if not isinstance(dados, list):
        raise ValueError(
            f"O conteúdo de {nome} deve ser uma lista."
        )

    return dados


def _salvar_json(nome, dados):
    DIRETORIO_DATA.mkdir(parents=True, exist_ok=True)

    caminho = DIRETORIO_DATA / nome
    temporario = caminho.with_suffix(".tmp")

    with temporario.open("w", encoding="utf-8") as arquivo:
        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

    temporario.replace(caminho)


def salvar_dados(
    temas,
    perguntas,
    quizzes,
    usuarios,
    tentativas
):
    """Salva todos os dados do sistema em arquivos JSON."""

    temas_json = [
        {"nome": tema.nome}
        for tema in temas
    ]

    temas_por_nome = {
        tema.nome.casefold(): tema
        for tema in temas
    }

    perguntas_json = []

    ids_perguntas = {}

    for indice, pergunta in enumerate(perguntas, start=1):
        identificador = f"P{indice:04d}"
        ids_perguntas[id(pergunta)] = identificador

        perguntas_json.append({
            "id": identificador,
            "tema": pergunta.tema.nome,
            "enunciado": pergunta.enunciado,
            "alternativas": list(pergunta.alternativas),
            "indice_correto": pergunta.indice_correto,
            "dificuldade": pergunta.dificuldade,
            "quiz_id": next(
                (
                    f"Q{i:04d}"
                    for i, quiz in enumerate(quizzes, start=1)
                    if pergunta.quiz is quiz
                ),
                None
            )
        })

    quizzes_json = []

    ids_quizzes = {
        id(quiz): f"Q{i:04d}"
        for i, quiz in enumerate(quizzes, start=1)
    }

    for quiz in quizzes:
        quizzes_json.append({
            "id": ids_quizzes[id(quiz)],
            "titulo": quiz.titulo,
            "perguntas": [
                ids_perguntas[id(pergunta)]
                for pergunta in quiz.perguntas
            ],
            "limite_tempo": quiz.limite_tempo,
            "limite_tentativas": quiz.limite_tentativas,
            "valor_bonus": quiz.valor_bonus,
            "professor": (
                quiz.professor.identificador
                if quiz.professor is not None
                else None
            ),
            "congelado": quiz.congelado
        })

    usuarios_json = []

    for usuario in usuarios:
        usuarios_json.append({
            "tipo": usuario.tipo,
            "nome": usuario.nome,
            "email": usuario.email,
            "identificador": usuario.identificador
        })

    tentativas_json = []

    for indice, tentativa in enumerate(tentativas, start=1):
        respostas_json = []

        for indice_pergunta, resposta in tentativa.respostas.items():
            respostas_json.append({
                "pergunta": ids_perguntas[id(resposta.pergunta)],
                "indice_alternativa": resposta.indice_alternativa
            })

        tentativas_json.append({
            "id": f"T{indice:04d}",
            "participante": tentativa.participante.identificador,
            "quiz": ids_quizzes[id(tentativa.quiz)],
            "data_inicio": tentativa.data_inicio.isoformat(),
            "data_fim": (
                tentativa.data_fim.isoformat()
                if tentativa.data_fim is not None
                else None
            ),
            "status": tentativa.status,
            "respostas": respostas_json
        })

    _salvar_json("temas.json", temas_json)

    _salvar_json(
        "quizzes.json",
        {
            "perguntas": perguntas_json,
            "quizzes": quizzes_json
        }
    )

    _salvar_json("usuario.json", usuarios_json)
    _salvar_json("tentativas.json", tentativas_json)


def carregar_dados():
    """Reconstrói os objetos do sistema a partir dos arquivos JSON."""

    temas_json = _ler_json("temas.json")
    usuarios_json = _ler_json("usuario.json")
    tentativas_json = _ler_json("tentativas.json")

    caminho_quizzes = DIRETORIO_DATA / "quizzes.json"

    if not caminho_quizzes.exists() or caminho_quizzes.stat().st_size == 0:
        quizzes_json = {"perguntas": [], "quizzes": []}
    else:
        with caminho_quizzes.open("r", encoding="utf-8") as arquivo:
            quizzes_json = json.load(arquivo)

    if not isinstance(quizzes_json, dict):
        raise ValueError("O arquivo quizzes.json possui formato inválido.")

    # 1. Reconstruir temas.
    temas = [
        Tema(item["nome"])
        for item in temas_json
    ]

    temas_por_nome = {
        tema.nome.casefold(): tema
        for tema in temas
    }

    # 2. Reconstruir usuários.
    usuarios = []

    usuarios_por_id = {}

    for item in usuarios_json:
        if item["tipo"] == "Aluno":
            usuario = Aluno(
                item["nome"],
                item["email"],
                item["identificador"]
            )
        elif item["tipo"] == "Professor":
            usuario = Professor(
                item["nome"],
                item["email"],
                item["identificador"]
            )
        else:
            raise ValueError("Tipo de usuário desconhecido.")

        usuarios.append(usuario)
        usuarios_por_id[usuario.identificador] = usuario

    # 3. Reconstruir perguntas.
    perguntas = []
    perguntas_por_id = {}

    for item in quizzes_json.get("perguntas", []):
        tema = temas_por_nome.get(item["tema"].casefold())

        if tema is None:
            raise ValueError(
                f"Tema não encontrado: {item['tema']}"
            )

        pergunta = Pergunta(
            tema,
            item["enunciado"],
            item["alternativas"],
            item["indice_correto"],
            item["dificuldade"]
        )

        perguntas.append(pergunta)
        perguntas_por_id[item["id"]] = pergunta

    # 4. Reconstruir quizzes e associações.
    quizzes = []
    quizzes_por_id = {}

    for item in quizzes_json.get("quizzes", []):
        quiz = Quiz(
            item["titulo"],
            limite_tempo=item["limite_tempo"],
            limite_tentativas=item["limite_tentativas"],
            valor_bonus=item["valor_bonus"]
        )

        for id_pergunta in item["perguntas"]:
            pergunta = perguntas_por_id[id_pergunta]
            quiz.adicionar_pergunta(pergunta)

        professor_id = item["professor"]

        if professor_id is not None:
            professor = usuarios_por_id.get(professor_id)

            if not isinstance(professor, Professor):
                raise ValueError(
                    f"Professor não encontrado: {professor_id}"
                )

            professor.adicionar_quiz(quiz)

        quizzes.append(quiz)
        quizzes_por_id[item["id"]] = quiz

    # Restaurar vínculos de perguntas removidas dos quizzes.
    for item in quizzes_json.get("perguntas", []):
        quiz_id = item.get("quiz_id")

        if quiz_id is not None:
            pergunta = perguntas_por_id[item["id"]]
            quiz = quizzes_por_id[quiz_id]

            if pergunta.quiz is None:
                pergunta._vincular_quiz(quiz)

    # 5. Reconstruir tentativas e respostas.
    tentativas = []

    for item in tentativas_json:
        participante = usuarios_por_id[item["participante"]]
        quiz = quizzes_por_id[item["quiz"]]

        tentativa = Tentativa(participante, quiz)

        tentativa._data_inicio = datetime.fromisoformat(
            item["data_inicio"]
        )

        tentativa._data_fim = (
            datetime.fromisoformat(item["data_fim"])
            if item["data_fim"] is not None
            else None
        )

        tentativa._status = item["status"]

        for resposta_item in item["respostas"]:
            pergunta = perguntas_por_id[resposta_item["pergunta"]]

            indice_pergunta = next(
                i for i, p in enumerate(quiz.perguntas)
                if p is pergunta
            )

            tentativa._respostas[indice_pergunta] = Resposta(
                pergunta,
                resposta_item["indice_alternativa"]
            )

        tentativas.append(tentativa)

    # Restaurar congelamento mesmo quando não existem tentativas.
    for item in quizzes_json.get("quizzes", []):
        if item.get("congelado", False):
            quiz = quizzes_por_id[item["id"]]

            if not quiz.congelado:
                quiz._congelar()

    return {
        "temas": temas,
        "perguntas": perguntas,
        "quizzes": quizzes,
        "usuarios": usuarios,
        "tentativas": tentativas
    }
