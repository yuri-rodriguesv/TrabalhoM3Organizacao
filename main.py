# main.py
# Autor: Yuri Rodrigues
# Disciplina: Organizacao de Computadores
#
# Programa principal do simulador de memoria cache.

import argparse
from cache import CacheSimulator
from utils import validar_parametros, ler_enderecos


def criar_parser():
    parser = argparse.ArgumentParser(
        description="Simulador de memoria cache com mapeamento direto e associativo por conjunto"
    )

    parser.add_argument("--cache-size", type=int, required=True,
                        help="Tamanho total da cache em bytes. Ex: 1024")
    parser.add_argument("--block-size", type=int, required=True,
                        help="Tamanho do bloco em bytes. Ex: 16")
    parser.add_argument("--assoc", type=int, required=True,
                        help="Associatividade. 1 = direta, 2 = 2-way, 4 = 4-way etc.")
    parser.add_argument("--addr-bits", type=int, required=True,
                        help="Quantidade de bits do endereco fisico. Ex: 16")
    parser.add_argument("--input", type=str, required=True,
                        help="Arquivo .txt com os enderecos de memoria")
    parser.add_argument("--policy", type=str, default="LRU", choices=["LRU", "FIFO", "lru", "fifo"],
                        help="Politica de substituicao para associatividade maior que 1")
    parser.add_argument("--verbose", action="store_true",
                        help="Mostra os detalhes de cada acesso e o estado da cache")

    return parser


def main():
    parser = criar_parser()
    args = parser.parse_args()

    try:
        # Primeiro valida a configuracao da cache
        info = validar_parametros(
            cache_size=args.cache_size,
            block_size=args.block_size,
            assoc=args.assoc,
            addr_bits=args.addr_bits
        )

        # Depois carrega os enderecos do arquivo
        enderecos = ler_enderecos(args.input, args.addr_bits)

        simulador = CacheSimulator(
            cache_size=args.cache_size,
            block_size=args.block_size,
            assoc=args.assoc,
            addr_bits=args.addr_bits,
            policy=args.policy.upper()
        )

        simulador.imprimir_configuracao()
        simulador.simular(enderecos, verbose=args.verbose)
        simulador.imprimir_relatorio()

    except Exception as erro:
        print("\nERRO:", erro)


if __name__ == "__main__":
    main()
