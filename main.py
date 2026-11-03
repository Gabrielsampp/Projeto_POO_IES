
from src.tema.tema import Tema
from src.quiz.pergunta import Pergunta
from src.quiz.quiz import Quiz


temas = {}
perguntas = []
quizzes = []


def ler_inteiro(mensagem, minimo=None, maximo=None):
    while True:
        try:
            valor = int(input(mensagem))

            if minimo is not None and valor < minimo:
                print(f"Digite um valor a partir de {minimo}.")
                continue

            if maximo is not None and valor > maximo:
                print(f"Digite um valor até {maximo}.")
                continue

            return valor

        except ValueError:
            print("Digite um número inteiro válido.")


def obter_tema():
    nome = input("Nome do tema: ").strip()

    if not nome:
        raise ValueError("O tema não pode estar vazio.")

    chave = nome.casefold()

    if chave not in temas:
        temas[chave] = Tema(nome)

    return temas[chave]


def cadastrar_pergunta():
    tema = obter_tema()
    enunciado = input("Enunciado: ").strip()

    quantidade = ler_inteiro(
        "Quantidade de alternativas (3 a 5): ", 3, 5
    )

    alternativas = []

    for i in range(quantidade):
        alternativa = input(f"Alternativa {i + 1}: ").strip()

        if not alternativa:
            raise ValueError("A alternativa não pode estar vazia.")

        alternativas.append(alternativa)

    indice_correto = ler_inteiro(
        f"Qual é a alternativa correta (1 a {quantidade})? ",
        1,
        quantidade
    ) - 1

    dificuldade = input("Dificuldade (F=fácil, M=média, D=difícil): ")
    dificuldade = dificuldade.strip().upper()

    pergunta = Pergunta(
        tema,
        enunciado,
        alternativas,
        indice_correto,
        dificuldade
    )

    # Evita duplicatas na biblioteca de perguntas.
    if any(pergunta == existente for existente in perguntas):
        raise ValueError("Já existe uma pergunta com esse tema e enunciado.")

    perguntas.append(pergunta)
    print("Pergunta cadastrada com sucesso.")


def listar_perguntas():
    if not perguntas:
        print("Nenhuma pergunta cadastrada.")
        return

    for i, pergunta in enumerate(perguntas, start=1):
        print(f"\n--- Pergunta {i} ---")
        print(pergunta)


def criar_quiz():
    titulo = input("Título do Quiz: ").strip()

    if not perguntas:
        print("Cadastre pelo menos uma pergunta antes.")
        return

    print("\nPerguntas disponíveis:")
    listar_perguntas()

    escolhidas = ler_lista_indices()

    quiz = Quiz(titulo)

    for indice in escolhidas:
        quiz.adicionar_pergunta(perguntas[indice])

    quizzes.append(quiz)
    print("\nQuiz criado com sucesso!")
    print(quiz)


def ler_lista_indices():
    entrada = input(
        "\nDigite os números das perguntas separados por vírgula: "
    )

    try:
        numeros = [int(item.strip()) for item in entrada.split(",")]
    except ValueError:
        raise ValueError("Digite apenas números separados por vírgulas.")

    if not numeros:
        raise ValueError("Selecione pelo menos uma pergunta.")

    if len(numeros) != len(set(numeros)):
        raise ValueError("Não repita números na seleção.")

    if any(numero < 1 or numero > len(perguntas) for numero in numeros):
        raise ValueError("Uma das perguntas selecionadas não existe.")

    return [numero - 1 for numero in numeros]


def listar_quizzes():
    if not quizzes:
        print("Nenhum Quiz cadastrado.")
        return

    for i, quiz in enumerate(quizzes, start=1):
        print(f"\n--- Quiz {i} ---")
        print(quiz)

        for pergunta in quiz.perguntas:
            print(f"- {pergunta.enunciado}")


def menu():
    while True:
        print("\n===== SISTEMA DE QUIZ =====")
        print("1. Cadastrar pergunta")
        print("2. Listar perguntas")
        print("3. Criar Quiz")
        print("4. Listar Quizzes")
        print("0. Sair")

        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                cadastrar_pergunta()
            elif opcao == "2":
                listar_perguntas()
            elif opcao == "3":
                criar_quiz()
            elif opcao == "4":
                listar_quizzes()
            elif opcao == "0":
                print("Encerrando o sistema.")
                break
            else:
                print("Opção inválida.")

        except (ValueError, TypeError, IndexError) as erro:
            print(f"Não foi possível concluir a operação: {erro}")


if __name__ == "__main__":
    menu()
