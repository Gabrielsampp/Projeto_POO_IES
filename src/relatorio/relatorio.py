from collections import defaultdict
from src.usuario.aluno import Aluno


class Relatorio:
    """Gera relatórios a partir das tentativas registradas no sistema."""

    def __init__(self, tentativas):
        if isinstance(tentativas, (str, bytes)):
            raise TypeError("As tentativas devem ser fornecidas em uma coleção.")

        try:
            self._tentativas = list(tentativas)
        except TypeError:
            raise TypeError("As tentativas devem ser fornecidas em uma coleção.")

        if any(not hasattr(t, "completa") for t in self._tentativas):
            raise TypeError("A coleção contém um objeto que não é uma Tentativa.")

    @property
    def tentativas(self):
        return tuple(self._tentativas)

    def _tentativas_completas(self):
        return [t for t in self._tentativas if t.completa]

    @staticmethod
    def _desempenho(tentativa):
        pontuacao_maxima = tentativa.quiz.calcular_pontuacao_maxima()

        if pontuacao_maxima == 0:
            return 0.0

        return tentativa.pontuacao / pontuacao_maxima * 100

    @staticmethod
    def _arredondar_percentual(valor):
        return int(valor + 0.5)

    def taxa_aprovacao(self):
        """Retorna o percentual de tentativas completas com nota >= 70%."""
        tentativas = self._tentativas_completas()

        if not tentativas:
            return 0.0

        aprovadas = sum(
            self._desempenho(t) >= 70
            for t in tentativas
        )

        return aprovadas / len(tentativas) * 100

    def distribuicao_notas(self):
        """Retorna a quantidade de tentativas em cada faixa percentual."""
        faixas = {"0": 0}

        for inicio in range(1, 100, 10):
            fim = min(inicio + 9, 100)
            faixas[f"{inicio}-{fim}"] = 0

        for tentativa in self._tentativas_completas():
            nota = self._arredondar_percentual(
                self._desempenho(tentativa)
            )

            if nota == 0:
                faixa = "0"
            else:
                inicio = ((nota - 1) // 10) * 10 + 1
                fim = min(inicio + 9, 100)
                faixa = f"{inicio}-{fim}"

            faixas[faixa] += 1

        return faixas

    def top_n_por_media_desempenho(self, n=10):
        """Retorna os alunos ordenados pela média percentual das tentativas."""
        if type(n) is not int:
            raise TypeError("N deve ser um número inteiro.")

        if n <= 0:
            raise ValueError("N deve ser maior que zero.")

        desempenho_por_aluno = {}

        for tentativa in self._tentativas_completas():
            aluno = tentativa.participante

            if not isinstance(aluno, Aluno):
                continue

            chave = id(aluno)

            if chave not in desempenho_por_aluno:
                desempenho_por_aluno[chave] = {
                    "participante": aluno,
                    "desempenhos": []
                }

            desempenho_por_aluno[chave]["desempenhos"].append(
                self._desempenho(tentativa)
            )

        ranking = []

        for dados in desempenho_por_aluno.values():
            media = sum(dados["desempenhos"]) / len(dados["desempenhos"])

            ranking.append({
                "participante": dados["participante"],
                "media_desempenho": media,
                "total_tentativas": len(dados["desempenhos"])
            })

        ranking.sort(
            key=lambda item: item["media_desempenho"],
            reverse=True
        )

        return ranking[:n]

    def desempenho_por_tema(self, participante=None):
        """Calcula a taxa de acerto geral ou de um participante por tema."""
        acertos_por_tema = defaultdict(int)
        respostas_por_tema = defaultdict(int)
        nomes_temas = {}

        for tentativa in self._tentativas_completas():
            if (
                participante is not None
                and tentativa.participante is not participante
            ):
                continue

            for resposta in tentativa.respostas.values():
                tema = resposta.pergunta.tema
                chave = tema.nome.casefold()

                nomes_temas[chave] = tema.nome
                respostas_por_tema[chave] += 1

                if resposta.correta:
                    acertos_por_tema[chave] += 1

        resultado = []

        for chave, total in respostas_por_tema.items():
            acertos = acertos_por_tema[chave]

            resultado.append({
                "tema": nomes_temas[chave],
                "acertos": acertos,
                "respostas": total,
                "taxa_acerto": acertos / total * 100
            })

        return sorted(resultado, key=lambda item: item["tema"].casefold())

    def questoes_mais_erradas(self, n=10):
        """Retorna as perguntas com maior quantidade de respostas incorretas."""
        if type(n) is not int:
            raise TypeError("N deve ser um número inteiro.")

        if n <= 0:
            raise ValueError("N deve ser maior que zero.")

        estatisticas = {}

        for tentativa in self._tentativas_completas():
            for resposta in tentativa.respostas.values():
                pergunta = resposta.pergunta
                chave = id(pergunta)

                if chave not in estatisticas:
                    estatisticas[chave] = {
                        "pergunta": pergunta,
                        "erros": 0,
                        "respostas": 0
                    }

                estatisticas[chave]["respostas"] += 1

                if not resposta.correta:
                    estatisticas[chave]["erros"] += 1

        resultado = []

        for dados in estatisticas.values():
            if dados["erros"] == 0:
                continue

            resultado.append({
                "pergunta": dados["pergunta"],
                "erros": dados["erros"],
                "respostas": dados["respostas"],
                "taxa_erro": dados["erros"] / dados["respostas"] * 100
            })

        resultado.sort(
            key=lambda item: item["erros"],
            reverse=True
        )

        return resultado[:n]

    def evolucao_usuario(self, participante):
        """Retorna o desempenho de um participante ao longo do tempo."""
        tentativas = [
            t for t in self._tentativas_completas()
            if t.participante is participante
        ]

        tentativas.sort(key=lambda t: t.data_inicio)

        return [
            {
                "data": tentativa.data_inicio,
                "quiz": tentativa.quiz.titulo,
                "pontuacao": tentativa.pontuacao,
                "desempenho": self._desempenho(tentativa)
            }
            for tentativa in tentativas
        ]