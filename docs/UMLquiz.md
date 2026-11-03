# Diagrama UML — Sistema de Quiz Educacional

Para retornar ao README, [clique aqui](../README.md).

```mermaid
classDiagram

    class Usuario {
        <<abstract>>
        -str _nome
        -str _email
        -str _identificador
        +tipo*
        +__str__()
        +__eq__(outro)
    }

    class Aluno {
        +tipo
        +__str__()
    }

    class Professor {
        +tipo
        +__str__()
    }

    class Participante {
        -list _tentativas
        +tentativas
        +adicionar_tentativa(tentativa)
    }

    class Criador {
        -list _quizzes
        +quizzes
        +adicionar_quiz(quiz)
    }

    class Tema {
        -str _nome
        +nome
        +__str__()
        +__eq__(outro)
    }

    class Pergunta {
        -Tema _tema
        -str _enunciado
        -list _alternativas
        -int _indice_correto
        -str _dificuldade
        -Quiz _quiz
        +tema
        +enunciado
        +alternativas
        +indice_correto
        +dificuldade
        +quiz
        +adicionar_alternativa(valor)
        +remover_alternativa(indice)
        +alterar_alternativa(indice, valor)
        +verificar_resposta(indice)
        +calcular_pontuacao()
        +__str__()
        +__eq__(outro)
    }

    class Quiz {
        -str _titulo
        -list _perguntas
        -float _limite_tempo
        -int _limite_tentativas
        -int _valor_bonus
        -Professor _professor
        -bool _congelado
        +titulo
        +perguntas
        +limite_tempo
        +limite_tentativas
        +valor_bonus
        +professor
        +congelado
        +adicionar_pergunta(pergunta)
        +remover_pergunta(pergunta)
        +alterar_ordem_perguntas(perguntas)
        +calcular_pontuacao_maxima()
        +__len__()
        +__iter__()
        +__str__()
    }

    class Tentativa {
        -Participante _participante
        -Quiz _quiz
        -dict _respostas
        -datetime _data_inicio
        -datetime _data_fim
        -str _status
        +participante
        +quiz
        +respostas
        +data_inicio
        +data_fim
        +status
        +pontuacao
        +acertos
        +quantidade_respondida
        +taxa_acerto
        +duracao
        +completa
        +registrar_resposta(indice_pergunta, indice_alternativa)
        +finalizar()
    }

    class Resposta {
        -Pergunta _pergunta
        -int _indice_alternativa
        +pergunta
        +indice_alternativa
        +correta
        +pontuacao
    }

    class Relatorio {
        +taxa_aprovacao()
        +distribuicao_notas()
        +top_n_por_media_desempenho(n)
        +desempenho_por_tema(participante)
        +questoes_mais_erradas(n)
        +evolucao_usuario(participante)
    }

    Usuario <|-- Aluno
    Usuario <|-- Professor

    Participante <|-- Aluno
    Participante <|-- Professor

    Criador <|-- Professor

    Professor "1" --> "0..*" Quiz : cria
    Quiz "1" o-- "1..*" Pergunta : mantém
    Pergunta "*" --> "1" Tema : pertence
    Pergunta "0..1" --> "0..1" Quiz : vinculada
    Participante "1" --> "0..*" Tentativa : realiza
    Quiz "1" --> "0..*" Tentativa : recebe
    Tentativa "1" *-- "0..*" Resposta : registra
    Resposta "*" --> "1" Pergunta : responde
    Relatorio ..> Tentativa : analisa
```

## Observações sobre o modelo

- `Usuario` é uma classe abstrata.
- `Aluno` e `Professor` herdam de `Usuario`.
- `Participante` e `Criador` são classes independentes, reutilizadas por múltipla herança.
- `Professor` pode atuar como criador e participante.
- `Quiz` mantém uma coleção de perguntas.
- `Tentativa` registra as respostas de um participante em um quiz.
- `Relatorio` analisa os dados das tentativas.

