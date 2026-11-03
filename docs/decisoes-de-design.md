# Decisões de Design — Sistema de Quiz Educacional

## 1. Organização dos usuários

A classe `Usuario` representa a entidade base dos usuários, concentrando atributos e comportamentos comuns, como nome, e-mail e identificador.

As classes `Aluno` e `Professor` especializam `Usuario`, diferenciando os tipos de usuários do sistema.

### 1.1 Separação entre usuários e papéis

`Participante` e `Criador` foram definidos como classes independentes de `Usuario`.

Essa decisão permite reutilizar comportamentos sem transformar os papéis em tipos de usuário.

- `Aluno` herda de `Usuario` e `Participante`.
- `Professor` herda de `Usuario`, `Participante` e `Criador`.

Dessa forma, um professor pode criar quizzes e também participar de avaliações.

## 2. Perguntas e temas

Cada `Pergunta` possui um tema, um enunciado, alternativas, índice da alternativa correta e nível de dificuldade.

A dificuldade é representada por três valores:

- `F`: Fácil.
- `M`: Média.
- `D`: Difícil.

A pontuação é calculada conforme o nível de dificuldade:

| Dificuldade | Pontuação |
|---|---:|
| Fácil | 1 |
| Média | 2 |
| Difícil | 3 |

As perguntas possuem validações para impedir alternativas inválidas, índices incorretos e duplicidade de enunciados dentro do mesmo tema.

O tema é associado à pergunta, permitindo organizar e analisar os resultados por assunto.

## 3. Composição e associação

### 3.1 Quiz e Pergunta

Um `Quiz` mantém uma coleção de perguntas e calcula sua pontuação máxima a partir delas.

Uma pergunta não pode ser reutilizada em outro quiz.

Quando uma pergunta é removida de um quiz, seu vínculo com o quiz original é preservado, impedindo que ela seja associada posteriormente a outro quiz.

### 3.2 Tentativa e Resposta

Uma `Tentativa` está associada a um participante e a um quiz.

Durante sua execução, as respostas são registradas e relacionadas às perguntas correspondentes.

A pontuação da tentativa é calculada a partir das respostas corretas.

## 4. Regras de execução

- Uma tentativa pertence a um participante e a um quiz.
- O limite de tentativas é individual por participante e quiz.
- O quiz é congelado após o início da primeira tentativa de um aluno.
- Um quiz vazio não pode ser iniciado.
- Uma pergunta não pode ser respondida mais de uma vez na mesma tentativa.
- A dificuldade não é exibida ao participante durante a execução.
- Tentativas incompletas não são consideradas nos relatórios de desempenho.
- A taxa de acerto considera a quantidade de respostas corretas em relação à quantidade de perguntas respondidas.
- O tempo limite é verificado durante as operações da tentativa; não há interrupção assíncrona da entrada da CLI.

## 5. Pontuação e relatórios

A pontuação é calculada de acordo com o peso da dificuldade de cada pergunta.

A taxa de acerto é calculada pela relação entre respostas corretas e respostas registradas.

Os relatórios consideram apenas tentativas concluídas.

O ranking considera alunos e utiliza a média do desempenho percentual das tentativas concluídas. Professores não são incluídos no ranking de alunos.

A taxa de aprovação considera o percentual de participantes com desempenho igual ou superior a 70%.

## 6. Persistência

A persistência é realizada utilizando arquivos JSON, sem ORM ou banco de dados externo.

O módulo `src/dados.py` centraliza as operações de leitura e gravação.

Os dados são separados em arquivos:

- `temas.json`: temas cadastrados.
- `quizzes.json`: perguntas e quizzes.
- `usuario.json`: usuários cadastrados.
- `tentativas.json`: tentativas e respostas registradas.

Os relacionamentos são reconstruídos durante o carregamento dos dados, utilizando identificadores para relacionar usuários, perguntas, quizzes e tentativas.

A gravação utiliza um arquivo temporário antes de substituir o arquivo de destino, reduzindo o risco de corrupção durante a escrita.

## 7. Testes automatizados

O projeto utiliza Pytest para verificar as regras de negócio e os comportamentos das classes.

Os testes abrangem:

- Validação e comportamento de usuários.
- Comportamentos dos papéis `Participante` e `Criador`.
- Validação e manipulação de perguntas.
- Regras de gerenciamento de quizzes.
- Registro e finalização de tentativas.
- Cálculos e relatórios.
- Persistência e reconstrução dos dados.

