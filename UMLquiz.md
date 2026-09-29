# Diagrama UML - Sistema de Quiz Educacional
Para ir ao README, [clique aqui](README.md).
```mermaid
classDiagram

    %% =========================
    %% Classes
    %% =========================

    class Usuario {
        -str nome
        -str identificador
        +validar_nome() void
        +validar_identificador() void
        +__str__() str
        +__eq__(other) bool
    }

    class Participante {
        <<mixin>>
        +responder() void
    }

    class Criador {
        <<mixin>>
        +criar_quiz() void
        +editar_quiz() void
    }

    class Aluno {
    }

    class Professor {
    }

    class Tema {
        -str nome
        +validar_nome() void
    }

    class Pergunta {
        -str enunciado
        -list alternativas
        -int indice_correta
        -str dificuldade
        -Tema tema
        +adicionar_alternativa(alternativa) void
        +remover_alternativa(indice) void
        +alterar_alternativa(indice, alternativa) void
        +verificar_resposta(indice) bool
        +calcular_pontuacao() int
        +validar() void
        +__str__() str
    }

    class PerguntaBonus {
    }

    class Quiz {
        -str titulo
        -list perguntas
        -int limite_tempo
        -int limite_tentativas
        -int valor_bonus
        -Professor professor
        +adicionar_pergunta(pergunta) void
        +remover_pergunta(pergunta) void
        +alterar_ordem_perguntas() void
        +calcular_pontuacao_maxima() int
        +iniciar() Tentativa
        +pode_realizar_tentativa(usuario) bool
        +__len__() int
    }

    class Resposta {
        -Pergunta pergunta
        -int alternativa_escolhida
        -float tempo_gasto
        -int pontuacao_obtida
        +corrigir() bool
        +calcular_pontuacao() int
    }

    class Tentativa {
        -Usuario usuario
        -Quiz quiz
        -list respostas
        -int pontuacao
        -float tempo_total
        -datetime data_hora
        -str status
        +registrar_resposta(resposta) void
        +calcular_pontuacao() int
        +finalizar() void
        +encerrar_por_tempo() void
        +__iter__() iterator
    }

    class Relatorio {
        +gerar_ranking() list
        +desempenho_por_tema() dict
        +questoes_mais_erradas() list
        +evolucao_desempenho() dict
    }

    %% =========================
    %% Herança e Mixins
    %% =========================

    Usuario <|-- Aluno
    Usuario <|-- Professor

    Participante <|-- Aluno
    Participante <|-- Professor

    Criador <|-- Professor

    Pergunta <|-- PerguntaBonus

    %% =========================
    %% Relacionamentos
    %% =========================

    Professor "1" --> "0..*" Quiz : Cria / Gerencia
    Quiz "1" *-- "1..*" Pergunta : Composicao
    Pergunta "*" --> "1" Tema : Pertence a
    Usuario "1" --> "0..*" Tentativa : Realiza
    Quiz "1" --> "0..*" Tentativa : Possui
    Tentativa "1" *-- "0..*" Resposta : Composicao
    Resposta "*" --> "1" Pergunta : Responde
    Professor --> Relatorio : Consulta
