from math import floor
import numpy as np
import pprint


def ler_matrizes():
    matrizes = []
    with open("matrizes.txt", "r") as f:
        conteudo = f.read()
        matrizes_txt = conteudo.strip().split("\n\n")

        for matriz_txt in matrizes_txt:
            linhas = matriz_txt.split("\n")
            matriz = []

            for linha in linhas:
                elementos = linha.split()
                linha_inteiros = []

                for elemento in elementos:
                    linha_inteiros.append(int(elemento))

                matriz.append(linha_inteiros)

            matrizes.append(matriz)
    return matrizes


class InterpolacaoBilinear:
    def __init__(self, matriz: list[list]):
        self.matriz = matriz

    @staticmethod
    def __gerar_matriz(linhas: int, colunas: int):
        return [[0 for _ in range(colunas)] for _ in range(linhas)]

    @staticmethod
    def __get_nova_posicao(linha: int, coluna: int):
        if linha == 0 and coluna == 0:
            return 0, 0
        return linha * 2, coluna * 2

    def __salvar_matriz(self, matriz: list[list], tipo: str):
        with open("matrizes_resultados.txt", "+a") as resultado:
            resultado.write(f"Matriz {tipo}:\n")
            for linha in matriz:
                resultado.write(f"{self.__get_linha_como_string(linha)}\n")
            resultado.write("\n\n")

    def __preencher_matriz_ampliada(self, nova_matriz: list[list]):
        linhas = len(nova_matriz)
        colunas = len(nova_matriz[0])
        for i in range(linhas):
            linha_vazia = sum(nova_matriz[i]) == 0
            step = 1 if linha_vazia else 2
            start = 0 if linha_vazia else 1

            for j in range(start, colunas, step):
                nova_celula = nova_matriz[i][j]
                if linha_vazia and j % 2 != 0:
                    nova_celula = round(
                        (
                            nova_matriz[i - 1][j - 1]
                            + nova_matriz[i + 1][j - 1]
                            + nova_matriz[i - 1][j + 1]
                            + nova_matriz[i + 1][j + 1]
                        )
                        / 4
                    )

                if linha_vazia and j % 2 == 0:
                    nova_celula = round(
                        (nova_matriz[i + 1][j] + nova_matriz[i - 1][j]) / 2
                    )

                if not linha_vazia and j % 2 != 0:
                    nova_celula = round(
                        (nova_matriz[i][j + 1] + nova_matriz[i][j - 1]) / 2
                    )

                nova_matriz[i][j] = nova_celula

        return nova_matriz

    def __ampliar_matriz(self):
        linhas = len(self.matriz)
        colunas = len(self.matriz[0])

        nova_matriz = self.__gerar_matriz(
            linhas=(linhas * 2) - 1, colunas=(colunas * 2) - 1
        )

        for i in range(linhas):
            for j in range(colunas):
                nova_linha, nova_coluna = self.__get_nova_posicao(i, j)
                nova_matriz[nova_linha][nova_coluna] = self.matriz[i][j]

        return nova_matriz

    def __reduzir_matriz(self):
        linhas = len(self.matriz)
        colunas = len(self.matriz[0])

        linhas = linhas - floor(linhas / 2)
        colunas = colunas - floor(colunas / 2)
        return self.__gerar_matriz(linhas, colunas)

    def __corrige_indice(self, linha, coluna):
        if linha + 1 > len(self.matriz) - 1:
            linha -= 1

        if coluna + 1 > len(self.matriz[0]) - 1:
            coluna -= 1

        return linha, coluna

    def __get_nova_posicao_reducao(self, linha: int, coluna: int):
        linha, coluna = self.__get_nova_posicao(linha, coluna)
        return self.__corrige_indice(linha, coluna)

    def __preencher_matriz_reduzida(self, nova_matriz):
        linhas = len(nova_matriz)
        colunas = len(nova_matriz[0])
        for i in range(linhas):
            for j in range(colunas):
                linha, coluna = self.__get_nova_posicao_reducao(i, j)
                nova_matriz[i][j] = round(
                    (
                        self.matriz[linha][coluna]
                        + self.matriz[linha + 1][coluna]
                        + self.matriz[linha][coluna + 1]
                        + self.matriz[linha + 1][coluna + 1]
                    )
                    / 4
                )

        return nova_matriz

    def reduzir(self):
        nova_matriz = self.__reduzir_matriz()
        nova_matriz = self.__preencher_matriz_reduzida(nova_matriz)
        self.__salvar_matriz(nova_matriz, "reduzida")

    def __get_linha_como_string(self, linha: list[int]):
        return " ".join([str(celula) for celula in linha])

    def ampliar(self):
        nova_matriz = self.__ampliar_matriz()
        nova_matriz = self.__preencher_matriz_ampliada(nova_matriz)
        self.__salvar_matriz(nova_matriz, "ampliada")


def main():
    matrizes = ler_matrizes()
    for matriz in matrizes:
        ib = InterpolacaoBilinear(matriz)
        ib.ampliar()
        ib.reduzir()


if __name__ == "__main__":
    main()
