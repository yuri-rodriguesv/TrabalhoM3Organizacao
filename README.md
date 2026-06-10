# Simulador de Memória Cache

Trabalho da disciplina de Organização de Computadores.

## Autor

Yuri Rodrifues

## Descrição

Este programa simula o funcionamento de uma memória cache.

Ele permite testar:

- mapeamento direto;
- mapeamento associativo por conjunto;
- política de substituição LRU;
- política de substituição FIFO.

O programa lê endereços de memória de um arquivo `.txt`, executa os acessos na cache e mostra um relatório final com total de acessos, hits e misses.

## Arquivos do projeto

- `main.py`: arquivo principal do programa.
- `cache.py`: lógica da cache e da simulação.
- `utils.py`: funções de validação e leitura do arquivo de entrada.
- `acessos_teste1.txt`: arquivo de teste com endereços simples.
- `acessos_teste2.txt`: arquivo de teste com mais conflitos.
- `README.md`: instruções do projeto.

## Como executar

É necessário ter Python instalado.

Exemplo de execução com mapeamento direto:

```bash
python main.py --cache-size 256 --block-size 16 --assoc 1 --addr-bits 16 --input acessos_teste1.txt
```

Exemplo com mapeamento associativo por conjunto 2-way e LRU:

```bash
python main.py --cache-size 1024 --block-size 32 --assoc 2 --addr-bits 16 --input acessos_teste2.txt --policy LRU
```

Exemplo com FIFO:

```bash
python main.py --cache-size 1024 --block-size 32 --assoc 2 --addr-bits 16 --input acessos_teste2.txt --policy FIFO
```

Exemplo com modo detalhado:

```bash
python main.py --cache-size 256 --block-size 16 --assoc 1 --addr-bits 16 --input acessos_teste1.txt --verbose
```

## Formato do arquivo de entrada

O arquivo deve possuir um endereço por linha.

Pode ser decimal:

```txt
16
32
48
```

Ou hexadecimal:

```txt
0x0010
0x0020
0x0030
```

Comentários iniciados com `#` são ignorados.

Exemplo:

```txt
# arquivo de teste
0x0010
0x0024
0x0010
256
0x00FF
```

## Parâmetros

| Parâmetro | Descrição |
|---|---|
| `--cache-size` | Tamanho total da cache em bytes |
| `--block-size` | Tamanho do bloco em bytes |
| `--assoc` | Grau de associatividade |
| `--addr-bits` | Quantidade de bits do endereço físico |
| `--input` | Caminho do arquivo de entrada |
| `--policy` | Política de substituição: LRU ou FIFO |
| `--verbose` | Mostra os detalhes de cada acesso |

## Exemplo de saída

```txt
========== CONFIGURACAO DA CACHE ==========
Tamanho da cache: 256 bytes
Tamanho do bloco: 16 bytes
Associatividade: 1
Politica: Direta
Bits de endereco: 16
Total de linhas: 16
Numero de conjuntos: 16
Bits de offset: 4
Bits de index: 4
Bits de tag: 8
===========================================

============== RELATORIO FINAL ==============
Total de acessos: 10
Cache hits: 3 ( 30.00 % )
Cache misses: 7 ( 70.00 % )
=============================================
```

## Observações

O programa valida algumas entradas inválidas, como:

- cache que não é potência de 2;
- bloco que não é potência de 2;
- arquivo inexistente;
- endereço fora do limite definido por `--addr-bits`;
- configuração incompatível entre cache, bloco e associatividade.
