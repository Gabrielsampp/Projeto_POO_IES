# 🧠 Sistema de Quiz Educacional

**Projeto individual — Programação Orientada a Objetos (2026.2)**

Sistema de quiz educacional executado por linha de comando (CLI), desenvolvido em Python. Permite cadastrar usuários, criar perguntas e quizzes, executar avaliações, registrar tentativas e consultar relatórios de desempenho.

O projeto aplica conceitos de Programação Orientada a Objetos, incluindo herança, múltipla herança, encapsulamento, composição, associação e validação de dados. A persistência é realizada por arquivos JSON.

## 📌 Sumário

- [Descrição](#-descrição)
- [Objetivo](#-objetivo)
- [Tecnologias](#-tecnologias)
- [Como executar](#-como-executar)
- [Comandos disponíveis](#-comandos-disponíveis)
- [Estrutura do projeto](#-estrutura-do-projeto)
- [Modelagem e decisões de design](#-modelagem-e-decisões-de-design)
- [Funcionalidades implementadas](#-funcionalidades-implementadas)
- [Testes](#-testes)

## ℹ️ Descrição

O sistema simula um ambiente de avaliações educacionais. Professores podem cadastrar perguntas e criar quizzes, enquanto alunos podem realizar tentativas e acompanhar seus resultados.

As perguntas são organizadas por temas e possuem níveis de dificuldade. Também podem ser classificadas como bônus, concedendo pontuação adicional quando respondidas corretamente.

Cada tentativa registra as respostas, a pontuação obtida, o tempo e o estado de conclusão.

Os resultados podem ser consultados por meio de relatórios que apresentam indicadores gerais e individuais.

## 🎯 Objetivo

Aplicar os conhecimentos de Programação Orientada a Objetos em um sistema funcional, com classes de responsabilidades distintas, validações, relacionamentos entre objetos, persistência de dados e testes automatizados.

## 🛠️ Tecnologias

- Python
- JSON
- Pytest
- CLI
- Mermaid

## 💻 Como executar

### Requisitos

- Python instalado.
- Pytest para executar os testes automatizados.

### Instalação

Clone o repositório e acesse a pasta do projeto:

```bash
git clone <https://github.com/Gabrielsampp/Projeto_POO_IES.git>
cd Projeto_POO_IES
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o sistema:

```bash
py main.py --help
```

O comando `--help` apresenta os grupos de operações disponíveis.

Os dados são armazenados em arquivos JSON na pasta `data/`. O sistema carrega esses dados ao iniciar e os atualiza após operações que modificam os cadastros ou os resultados.

## ⌨️ Comandos disponíveis

### Usuários

Cadastrar professor:

```bash
py main.py usuario cadastrar --tipo professor --nome "Paulo" --email "paulo@email.com" --identificador "P001"
```

Cadastrar aluno:

```bash
py main.py usuario cadastrar --tipo aluno --nome "Ana" --email "ana@email.com" --identificador "A001"
```

Listar usuários:

```bash
py main.py usuario listar
```

### Perguntas

Cadastrar uma pergunta:

```bash
py main.py pergunta adicionar
```

O sistema solicitará:

- Tema.
- Enunciado.
- Quantidade de alternativas.
- Alternativas.
- Número da alternativa correta.
- Dificuldade (Fácil, Média ou Difícil).
- Classificação como pergunta bônus ou normal.

Listar perguntas:

```bash
py main.py pergunta listar
```

### Quizzes

Criar um quiz:

```bash
py main.py quiz criar --titulo "Programação básica" --professor P001
```

Durante a criação, o sistema solicitará os números das perguntas que farão parte do quiz.

Também é possível configurar limites:

```bash
py main.py quiz criar --titulo "Programação básica" --professor P001 --tempo 30 --limite-tentativas 2
```

Listar quizzes:

```bash
py main.py quiz listar
```

Executar um quiz:

```bash
py main.py quiz executar --quiz 1 --participante A001
```

### Relatórios

Consultar taxa de aprovação:

```bash
py main.py relatorio aprovacao
```

Consultar distribuição das notas:

```bash
py main.py relatorio distribuicao
```

Consultar ranking:

```bash
py main.py relatorio ranking
```

Consultar desempenho por tema:

```bash
py main.py relatorio temas
```

Consultar questões mais erradas:

```bash
py main.py relatorio questoes
```

Consultar evolução de um participante:

```bash
py main.py relatorio evolucao --participante A001
```

## 🏗️ Estrutura do projeto

```text
Projeto_POO_IES/
│
├── data/
│   ├── quizzes.json
│   ├── temas.json
│   ├── tentativas.json
│   └── usuario.json
│
├── docs/
│   ├── decisoes-de-design.md
│   └── UMLquiz.md
│
├── src/
│   ├── papeis/
│   │   ├── criador.py
│   │   └── participante.py
│   │
│   ├── quiz/
│   │   ├── pergunta.py
│   │   ├── pergunta_bonus.py
│   │   └── quiz.py
│   │
│   ├── relatorio/
│   │   └── relatorio.py
│   │
│   ├── tema/
│   │   └── tema.py
│   │
│   ├── tentativa/
│   │   ├── resposta.py
│   │   └── tentativa.py
│   │
│   ├── usuario/
│   │   ├── usuario.py
│   │   ├── aluno.py
│   │   └── professor.py
│   │
│   └── dados.py
│
├── testes/
│   ├── teste_criador.py
│   ├── teste_participante.py
│   ├── teste_pergunta.py
│   ├── teste_quiz.py
│   ├── teste_relatorio.py
│   ├── teste_tentativa.py
│   ├── teste_usuario.py
│   └── teste_dados.py
│
├── .gitignore
├── main.py
├── pytest.ini
├── requirements.txt
├── settings.json
└── README.md
```

### Organização das responsabilidades

- `usuario/`: identidade e especializações dos usuários.
- `papeis/`: comportamentos de participação e criação.
- `quiz/`: perguntas, perguntas bônus e gerenciamento dos quizzes.
- `tema/`: representação dos temas.
- `tentativa/`: execução, respostas e resultados.
- `relatorio/`: análise dos resultados registrados.
- `dados.py`: leitura e gravação dos dados em JSON.
- `data/`: armazenamento persistente.
- `testes/`: testes automatizados.
- `docs/`: documentação de decisões e modelagem.

## 🧱 Modelagem e decisões de design

O sistema utiliza herança para especializar usuários e múltipla herança para reutilizar comportamentos.

`Participante` e `Criador` são papéis independentes. Um aluno é um usuário participante, enquanto um professor é um usuário que pode atuar tanto como participante quanto como criador de quizzes.

O quiz mantém suas perguntas e cada tentativa registra as respostas associadas à avaliação realizada.

As perguntas bônus são especializações de `Pergunta`, utilizando herança e polimorfismo para calcular a pontuação adicional.

As decisões de modelagem estão documentadas em [`docs/decisoes-de-design.md`](docs/decisoes-de-design.md).

O diagrama UML está disponível em [`docs/UMLquiz.md`](docs/UMLquiz.md).

## 🎮 Funcionalidades implementadas

- Cadastro e listagem de alunos e professores.
- Cadastro de perguntas com tema, alternativas, resposta correta e dificuldade.
- Classificação de perguntas como normais ou bônus.
- Pontuação adicional de 2 pontos para perguntas bônus respondidas corretamente.
- Cálculo de pontuação conforme a dificuldade e a classificação da pergunta.
- Validação de perguntas e alternativas.
- Criação e listagem de quizzes.
- Associação de perguntas aos quizzes.
- Bloqueio de reutilização de perguntas em outros quizzes.
- Limite de tempo e de tentativas configurável por quiz.
- Execução de tentativas e registro de respostas.
- Cálculo de pontuação e taxa de acerto.
- Exibição do gabarito após a execução.
- Persistência de dados em JSON.
- Relatórios de aprovação, distribuição de notas, ranking, desempenho por tema, questões mais erradas e evolução individual.

## 🧪 Testes

O projeto utiliza Pytest para verificar as regras de negócio, validações, relacionamentos, execução das tentativas, cálculo de pontuação, perguntas bônus, relatórios e persistência.

Para executar a suíte de testes:

```bash
py -m pytest -v
```

**Última validação: 96 testes aprovados.**