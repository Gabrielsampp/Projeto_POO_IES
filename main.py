
import argparse
import json
from pathlib import Path

from src.dados import carregar_dados, salvar_dados
from src.tema.tema import Tema
from src.quiz.pergunta import Pergunta
from src.quiz.quiz import Quiz
from src.usuario.aluno import Aluno
from src.usuario.professor import Professor
from src.tentativa.tentativa import Tentativa
from src.relatorio.relatorio import Relatorio


ARQUIVO_CONFIG = Path(__file__).parent / "settings.json"

dados = carregar_dados()

temas = dados["temas"]
perguntas = dados["perguntas"]
quizzes = dados["quizzes"]
usuarios = dados["usuarios"]
tentativas = dados["tentativas"]


def salvar():
    salvar_dados(temas, perguntas, quizzes, usuarios, tentativas)


def buscar_usuario(identificador):
    for usuario in usuarios:
        if usuario.identificador == identificador:
            return usuario
    raise ValueError("Usuário não encontrado.")


def buscar_professor(identificador):
    usuario = buscar_usuario(identificador)

    if not isinstance(usuario, Professor):
        raise ValueError("O identificador não pertence a um professor.")

    return usuario


def buscar_quiz(indice):
    if not 1 <= indice <= len(quizzes):
        raise ValueError("Quiz inexistente.")

    return quizzes[indice - 1]


def carregar_configuracoes():
    padrao = {
        "limite_tempo_padrao": None,
        "limite_tentativas_padrao": None,
        "nota_minima_aprovacao": 70
    }

    if not ARQUIVO_CONFIG.exists():
        return padrao

    with ARQUIVO_CONFIG.open("r", encoding="utf-8") as arquivo:
        configuracoes = json.load(arquivo)

    padrao.update(configuracoes)
    return padrao


config = carregar_configuracoes()


def cadastrar_usuario(args):
    if args.tipo == "aluno":
        usuario = Aluno(args.nome, args.email, args.identificador)
    else:
        usuario = Professor(args.nome, args.email, args.identificador)

    if any(u.identificador == usuario.identificador for u in usuarios):
        raise ValueError("Já existe um usuário com esse identificador.")

    usuarios.append(usuario)
    salvar()
    print(f"{usuario.tipo} cadastrado com sucesso.")


def listar_usuarios(args):
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    for usuario in usuarios:
        print(f"\n{usuario}")


def cadastrar_pergunta(args):
    nome_tema = input("Tema: ").strip()

    if not nome_tema:
        raise ValueError("O tema não pode estar vazio.")

    tema = next(
        (t for t in temas if t.nome.casefold() == nome_tema.casefold()),
        None
    )

    if tema is None:
        tema = Tema(nome_tema)
        temas.append(tema)

    enunciado = input("Enunciado: ").strip()

    quantidade = int(input("Quantidade de alternativas (3 a 5): "))

    if not 3 <= quantidade <= 5:
        raise ValueError("A quantidade deve estar entre 3 e 5.")

    alternativas = []

    for i in range(quantidade):
        alternativas.append(input(f"Alternativa {i + 1}: "))

    indice_correto = int(input("Número da alternativa correta: ")) - 1
    dificuldade = input("Dificuldade (F/M/D): ").strip().upper()

    pergunta = Pergunta(
        tema,
        enunciado,
        alternativas,
        indice_correto,
        dificuldade
    )

    if any(p == pergunta for p in perguntas):
        raise ValueError("Já existe uma pergunta com esse tema e enunciado.")

    perguntas.append(pergunta)
    salvar()

    print("Pergunta cadastrada com sucesso.")


def listar_perguntas(args):
    if not perguntas:
        print("Nenhuma pergunta cadastrada.")
        return

    for i, pergunta in enumerate(perguntas, start=1):
        print(f"\n[{i}]")
        print(pergunta)


def criar_quiz(args):
    professor = buscar_professor(args.professor)

    if not perguntas:
        raise ValueError("Cadastre perguntas antes de criar um quiz.")

    listar_perguntas(argparse.Namespace())

    entrada = input(
        "\nDigite os números das perguntas separados por vírgula: "
    )

    indices = [int(x.strip()) for x in entrada.split(",")]

    if not indices or len(indices) != len(set(indices)):
        raise ValueError("Seleção vazia ou com números repetidos.")

    if any(i < 1 or i > len(perguntas) for i in indices):
        raise ValueError("Uma das perguntas selecionadas não existe.")

    quiz = Quiz(
        args.titulo,
        limite_tempo=(
            args.tempo
            if args.tempo is not None
            else config["limite_tempo_padrao"]
        ),
        limite_tentativas=(
            args.limite_tentativas
            if args.limite_tentativas is not None
            else config["limite_tentativas_padrao"]
        )
    )

    for indice in indices:
        quiz.adicionar_pergunta(perguntas[indice - 1])

    professor.adicionar_quiz(quiz)
    quizzes.append(quiz)

    salvar()
    print("\nQuiz criado com sucesso.")
    print(quiz)


def listar_quizzes(args):
    if not quizzes:
        print("Nenhum quiz cadastrado.")
        return

    for i, quiz in enumerate(quizzes, start=1):
        print(f"\n[{i}]")
        print(quiz)
        print("Professor:", (
            quiz.professor.nome if quiz.professor else "Não definido"
        ))


def executar_quiz(args):
    quiz = buscar_quiz(args.quiz)
    participante = buscar_usuario(args.participante)

    if not hasattr(participante, "adicionar_tentativa"):
        raise ValueError("Esse usuário não pode participar de quizzes.")

    tentativa = Tentativa(participante, quiz)
    tentativas.append(tentativa)

    print(f"\nIniciando: {quiz.titulo}")
    
    for i, pergunta in enumerate(quiz.perguntas):
        print(f"\nPergunta {i + 1}: {pergunta.enunciado}")

        for j, alternativa in enumerate(pergunta.alternativas, start=1):
            print(f"{j}. {alternativa}")

        resposta = int(input("Sua resposta: ")) - 1

        tentativa.registrar_resposta(i, resposta)

    tentativa.finalizar()
    salvar()

    print("\nResultado:")
    print(tentativa)
    print("\nGabarito:")

    for i, pergunta in enumerate(quiz.perguntas):
        resposta = tentativa.respostas[i]

        print(
            f"{i + 1}. Correta: "
            f"{pergunta.alternativas[pergunta.indice_correto]}"
            f" | Sua resposta: "
            f"{pergunta.alternativas[resposta.indice_alternativa]}"
        )


def relatorio_aprovacao(args):
    relatorio = Relatorio(tentativas)
    print(f"Taxa de aprovação: {relatorio.taxa_aprovacao():.2f}%")


def relatorio_distribuicao(args):
    distribuicao = Relatorio(tentativas).distribuicao_notas()

    print("Distribuição das notas:")
    for faixa, quantidade in distribuicao.items():
        print(f"{faixa}%: {quantidade}")


def relatorio_ranking(args):
    ranking = Relatorio(tentativas).top_n_por_media_desempenho(args.quantidade)

    if not ranking:
        print("Não existem resultados para o ranking.")
        return

    print("Ranking por Média de Desempenho:")
    for posicao, item in enumerate(ranking, start=1):
        print(
            f"{posicao}º - {item['participante'].nome}: "
            f"{item['media_desempenho']:.2f}% "
            f"({item['total_tentativas']} tentativas)"
        )


def relatorio_temas(args):
    resultado = Relatorio(tentativas).desempenho_por_tema()

    for item in resultado:
        print(
            f"{item['tema']}: {item['acertos']}/{item['respostas']} "
            f"({item['taxa_acerto']:.2f}%)"
        )


def relatorio_questoes(args):
    resultado = Relatorio(tentativas).questoes_mais_erradas(args.quantidade)

    for item in resultado:
        print(
            f"{item['pergunta'].enunciado}: "
            f"{item['erros']} erros em {item['respostas']} respostas "
            f"({item['taxa_erro']:.2f}%)"
        )


def relatorio_evolucao(args):
    participante = buscar_usuario(args.participante)
    resultado = Relatorio(tentativas).evolucao_usuario(participante)

    if not resultado:
        print("Não existem tentativas completas para esse usuário.")
        return

    for item in resultado:
        print(
            f"{item['data']:%d/%m/%Y %H:%M} - {item['quiz']}: "
            f"{item['desempenho']:.2f}%"
        )


def executar_comando(funcao, args):
    try:
        funcao(args)
    except (ValueError, TypeError, IndexError, KeyError, OSError) as erro:
        print(f"Erro: {erro}")


def criar_parser():
    parser = argparse.ArgumentParser(
        description="Sistema de Quiz Educacional"
    )

    comandos = parser.add_subparsers(dest="grupo", required=True)

    # Usuários
    usuario = comandos.add_parser("usuario")
    usuario_comandos = usuario.add_subparsers(
        dest="acao", required=True
    )

    cadastrar = usuario_comandos.add_parser("cadastrar")
    cadastrar.add_argument("--tipo", choices=["aluno", "professor"], required=True)
    cadastrar.add_argument("--nome", required=True)
    cadastrar.add_argument("--email", required=True)
    cadastrar.add_argument("--identificador", required=True)
    cadastrar.set_defaults(func=cadastrar_usuario)

    listar = usuario_comandos.add_parser("listar")
    listar.set_defaults(func=listar_usuarios)

    # Perguntas
    pergunta = comandos.add_parser("pergunta")
    pergunta_comandos = pergunta.add_subparsers(
        dest="acao", required=True
    )

    adicionar = pergunta_comandos.add_parser("adicionar")
    adicionar.set_defaults(func=cadastrar_pergunta)

    listar = pergunta_comandos.add_parser("listar")
    listar.set_defaults(func=listar_perguntas)

    # Quizzes
    quiz = comandos.add_parser("quiz")
    quiz_comandos = quiz.add_subparsers(
        dest="acao", required=True
    )

    criar = quiz_comandos.add_parser("criar")
    criar.add_argument("--titulo", required=True)
    criar.add_argument("--professor", required=True)
    criar.add_argument("--tempo", type=float)
    criar.add_argument("--limite-tentativas", type=int)
    criar.set_defaults(func=criar_quiz)

    listar = quiz_comandos.add_parser("listar")
    listar.set_defaults(func=listar_quizzes)

    executar = quiz_comandos.add_parser("executar")
    executar.add_argument("--quiz", type=int, required=True)
    executar.add_argument("--participante", required=True)
    executar.set_defaults(func=executar_quiz)

    # Relatórios
    relatorio = comandos.add_parser("relatorio")
    relatorio_comandos = relatorio.add_subparsers(
        dest="acao", required=True
    )

    opcoes = {
        "aprovacao": relatorio_aprovacao,
        "distribuicao": relatorio_distribuicao,
        "ranking": relatorio_ranking,
        "temas": relatorio_temas,
        "questoes": relatorio_questoes,
        "evolucao": relatorio_evolucao
    }

    for nome, funcao in opcoes.items():
        comando = relatorio_comandos.add_parser(nome)

        if nome in ("ranking", "questoes"):
            comando.add_argument("--quantidade", type=int, default=10)

        if nome == "evolucao":
            comando.add_argument("--participante", required=True)

        comando.set_defaults(func=funcao)

    return parser


if __name__ == "__main__":
    parser = criar_parser()
    argumentos = parser.parse_args()
    executar_comando(argumentos.func, argumentos)
