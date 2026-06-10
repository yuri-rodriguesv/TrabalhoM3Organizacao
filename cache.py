# cache.py
# Logica principal da simulacao da memoria cache.

import math


class CacheLine:
    def __init__(self):
        self.valid = False
        self.tag = None

        # Usado para LRU e FIFO
        self.last_used = 0
        self.inserted_at = 0


class CacheSimulator:
    def __init__(self, cache_size, block_size, assoc, addr_bits, policy="LRU"):
        self.cache_size = cache_size
        self.block_size = block_size
        self.assoc = assoc
        self.addr_bits = addr_bits
        self.policy = policy

        self.total_lines = cache_size // block_size
        self.num_sets = self.total_lines // assoc

        self.offset_bits = int(math.log2(block_size))
        self.index_bits = int(math.log2(self.num_sets))
        self.tag_bits = addr_bits - self.index_bits - self.offset_bits

        # Criacao da cache:
        # Uma lista de conjuntos, onde cada conjunto possui "assoc" linhas.
        self.cache = []
        for _ in range(self.num_sets):
            conjunto = []
            for _ in range(assoc):
                conjunto.append(CacheLine())
            self.cache.append(conjunto)

        self.acessos = 0
        self.hits = 0
        self.misses = 0

        # Contador simples para controlar LRU/FIFO
        self.tempo = 0

    def decompor_endereco(self, endereco):
        # Offset: parte final do endereco
        offset_mask = (1 << self.offset_bits) - 1
        offset = endereco & offset_mask

        # Numero do bloco na memoria principal
        bloco = endereco // self.block_size

        # Index: conjunto onde esse bloco deve ir
        index = bloco % self.num_sets

        # Tag: identifica o bloco dentro do conjunto
        tag = bloco // self.num_sets

        return tag, index, offset

    def acessar(self, endereco):
        self.acessos += 1
        self.tempo += 1

        tag, index, offset = self.decompor_endereco(endereco)
        conjunto = self.cache[index]

        # Procura se a tag ja esta no conjunto
        for linha in conjunto:
            if linha.valid and linha.tag == tag:
                self.hits += 1
                linha.last_used = self.tempo
                return "HIT", tag, index, offset

        # Se chegou aqui, deu miss
        self.misses += 1

        # Tenta achar uma linha vazia primeiro
        linha_escolhida = None
        for linha in conjunto:
            if not linha.valid:
                linha_escolhida = linha
                break

        # Se nao tiver linha vazia, aplica politica de substituicao
        if linha_escolhida is None:
            if self.policy == "FIFO":
                linha_escolhida = min(conjunto, key=lambda linha: linha.inserted_at)
            else:
                # Padrao: LRU
                linha_escolhida = min(conjunto, key=lambda linha: linha.last_used)

        linha_escolhida.valid = True
        linha_escolhida.tag = tag
        linha_escolhida.last_used = self.tempo
        linha_escolhida.inserted_at = self.tempo

        return "MISS", tag, index, offset

    def simular(self, enderecos, verbose=False):
        for endereco in enderecos:
            resultado, tag, index, offset = self.acessar(endereco)

            if verbose:
                print("\nAcesso:", endereco, "(hex:", hex(endereco), ")")
                print("Tag:", tag, "| Index:", index, "| Offset:", offset, "| Resultado:", resultado)
                self.imprimir_estado_cache()

    def imprimir_configuracao(self):
        print("\n========== CONFIGURACAO DA CACHE ==========")
        print("Tamanho da cache:", self.cache_size, "bytes")
        print("Tamanho do bloco:", self.block_size, "bytes")
        print("Associatividade:", self.assoc)
        print("Politica:", self.policy if self.assoc > 1 else "Direta")
        print("Bits de endereco:", self.addr_bits)
        print("Total de linhas:", self.total_lines)
        print("Numero de conjuntos:", self.num_sets)
        print("Bits de offset:", self.offset_bits)
        print("Bits de index:", self.index_bits)
        print("Bits de tag:", self.tag_bits)
        print("===========================================")

    def imprimir_estado_cache(self):
        print("\nEstado atual da cache:")

        for i, conjunto in enumerate(self.cache):
            print("Conjunto", i, end=": ")

            partes = []
            for j, linha in enumerate(conjunto):
                if linha.valid:
                    partes.append("Linha " + str(j) + " [tag=" + str(linha.tag) + "]")
                else:
                    partes.append("Linha " + str(j) + " [vazia]")

            print(" | ".join(partes))

    def imprimir_relatorio(self):
        percentual_hits = 0
        percentual_misses = 0

        if self.acessos > 0:
            percentual_hits = (self.hits / self.acessos) * 100
            percentual_misses = (self.misses / self.acessos) * 100

        print("\n============== RELATORIO FINAL ==============")
        print("Total de acessos:", self.acessos)
        print("Cache hits:", self.hits, "(", format(percentual_hits, ".2f"), "% )")
        print("Cache misses:", self.misses, "(", format(percentual_misses, ".2f"), "% )")
        print("=============================================")
