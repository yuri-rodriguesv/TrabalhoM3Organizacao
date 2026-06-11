# main.py
# Autor: Yuri Rodrigues
# Disciplina: Organizacao de Computadores
#
# Programa principal do simulador de memoria cache.

from cache import CacheSimulator
from utils import validar_parametros, ler_enderecos


# ============================================================
# CONFIGURACOES DA SIMULACAO
# Altere os valores abaixo para testar outras configuracoes
# ============================================================

CACHE_SIZE = 1024          # tamanho total da cache em bytes
BLOCK_SIZE = 32           # tamanho de cada bloco em bytes
ASSOC = 2                 # 1 = mapeamento direto, 2 = 2-way, 4 = 4-way etc.
ADDR_BITS = 16            # quantidade de bits do endereco fisico
INPUT_FILE = "acessos_teste2.txt"   # arquivo com os enderecos de memoria

# Politica de substituicao usada quando ASSOC > 1
# Pode ser "LRU" ou "FIFO"
POLICY = "LRU"

# Se for True, mostra cada acesso passo a passo
# Se for False, mostra apenas o relatorio final
VERBOSE = True


def main():
    try:
        # Primeiro valida se a configuracao da cache faz sentido
        validar_parametros(
            cache_size=CACHE_SIZE,
            block_size=BLOCK_SIZE,
            assoc=ASSOC,
            addr_bits=ADDR_BITS
        )

        # Depois le os enderecos do arquivo de entrada
        enderecos = ler_enderecos(INPUT_FILE, ADDR_BITS)

        # Cria o simulador da cache usando as configuracoes acima
        simulador = CacheSimulator(
            cache_size=CACHE_SIZE,
            block_size=BLOCK_SIZE,
            assoc=ASSOC,
            addr_bits=ADDR_BITS,
            policy=POLICY.upper()
        )

        # Mostra a configuracao calculada: tag, index e offset
        simulador.imprimir_configuracao()

        # Executa a simulacao dos acessos
        simulador.simular(enderecos, verbose=VERBOSE)

        # Mostra o resultado final: hits e misses
        simulador.imprimir_relatorio()

    except Exception as erro:
        print("\nERRO:", erro)


if __name__ == "__main__":
    main()