# utils.py
# Funcoes auxiliares para validacao e leitura dos enderecos.

import math
import os


def eh_potencia_de_2(valor):
    return valor > 0 and (valor & (valor - 1)) == 0


def validar_parametros(cache_size, block_size, assoc, addr_bits):
    if not eh_potencia_de_2(cache_size):
        raise ValueError("O tamanho da cache deve ser potencia de 2.")

    if not eh_potencia_de_2(block_size):
        raise ValueError("O tamanho do bloco deve ser potencia de 2.")

    if assoc <= 0:
        raise ValueError("A associatividade deve ser maior que zero.")

    if cache_size < block_size:
        raise ValueError("A cache nao pode ser menor que o bloco.")

    if cache_size % block_size != 0:
        raise ValueError("O tamanho da cache deve ser divisivel pelo tamanho do bloco.")

    total_linhas = cache_size // block_size

    if total_linhas % assoc != 0:
        raise ValueError("O numero de linhas da cache deve ser divisivel pela associatividade.")

    num_conjuntos = total_linhas // assoc

    if not eh_potencia_de_2(num_conjuntos):
        raise ValueError("O numero de conjuntos precisa ser potencia de 2.")

    offset_bits = int(math.log2(block_size))
    index_bits = int(math.log2(num_conjuntos))
    tag_bits = addr_bits - offset_bits - index_bits

    if addr_bits <= 0:
        raise ValueError("A quantidade de bits do endereco deve ser maior que zero.")

    if tag_bits < 0:
        raise ValueError("A quantidade de bits do endereco e pequena demais para essa configuracao.")

    return {
        "total_linhas": total_linhas,
        "num_conjuntos": num_conjuntos,
        "offset_bits": offset_bits,
        "index_bits": index_bits,
        "tag_bits": tag_bits
    }


def ler_enderecos(caminho, addr_bits):
    if not os.path.exists(caminho):
        raise FileNotFoundError("Arquivo de entrada nao encontrado: " + caminho)

    enderecos = []
    limite = (1 << addr_bits) - 1

    with open(caminho, "r", encoding="utf-8") as arquivo:
        for numero_linha, linha in enumerate(arquivo, start=1):
            linha = linha.strip()

            # Ignora linhas vazias e comentarios
            if linha == "" or linha.startswith("#"):
                continue

            # Permite comentario no final da linha tambem
            if "#" in linha:
                linha = linha.split("#")[0].strip()

            try:
                if linha.lower().startswith("0x"):
                    endereco = int(linha, 16)
                else:
                    endereco = int(linha)
            except ValueError:
                raise ValueError("Endereco invalido na linha " + str(numero_linha) + ": " + linha)

            if endereco < 0 or endereco > limite:
                raise ValueError(
                    "Endereco fora do espaco de enderecamento na linha "
                    + str(numero_linha)
                    + ": "
                    + str(endereco)
                )

            enderecos.append(endereco)

    if len(enderecos) == 0:
        raise ValueError("O arquivo nao possui enderecos validos.")

    return enderecos
