# Simulador de Memória Cache

Trabalho da disciplina de Organização de Computadores.

## Autor

Yuri Rodrigues

## Descrição

Este programa simula o funcionamento de uma memória cache.

Ele permite testar:

* mapeamento direto;
* mapeamento associativo por conjunto;
* política de substituição LRU;
* política de substituição FIFO.

O programa lê endereços de memória de um arquivo `.txt`, executa os acessos na cache e mostra um relatório final com total de acessos, cache hits e cache misses.

## Arquivos do projeto

* `main.py`: arquivo principal do programa. Nele ficam as configurações da simulação.
* `cache.py`: contém a lógica da cache e da simulação.
* `utils.py`: contém funções auxiliares de validação e leitura do arquivo de entrada.
* `acessos_teste1.txt`: arquivo de teste com endereços simples.
* `acessos_teste2.txt`: arquivo de teste com mais repetições e conflitos.
* `README.md`: instruções do projeto.

## Como executar

É necessário ter Python instalado no computador.

Como as configurações principais da cache estão definidas diretamente no arquivo `main.py`, basta executar:

```bash
python main.py
```

## Como alterar a configuração da cache

Para testar outras configurações, abra o arquivo `main.py` e altere os valores das variáveis no início do código.

Exemplo:

```python
CACHE_SIZE = 256
BLOCK_SIZE = 16
ASSOC = 1
ADDR_BITS = 16
INPUT_FILE = "acessos_teste1.txt"
POLICY = "LRU"
VERBOSE = False
```

Descrição de cada variável:

| Variável     | Descrição                                            |
| ------------ | ---------------------------------------------------- |
| `CACHE_SIZE` | Tamanho total da cache em bytes                      |
| `BLOCK_SIZE` | Tamanho de cada bloco em bytes                       |
| `ASSOC`      | Grau de associatividade da cache                     |
| `ADDR_BITS`  | Quantidade de bits do endereço físico                |
| `INPUT_FILE` | Nome do arquivo `.txt` com os endereços              |
| `POLICY`     | Política de substituição: `LRU` ou `FIFO`            |
| `VERBOSE`    | Se for `True`, mostra o passo a passo de cada acesso |

## Exemplo de configuração com mapeamento direto

```python
CACHE_SIZE = 256
BLOCK_SIZE = 16
ASSOC = 1
ADDR_BITS = 16
INPUT_FILE = "acessos_teste1.txt"
POLICY = "LRU"
VERBOSE = False
```

Nesse caso, a associatividade é `1`, então a cache funciona com mapeamento direto. Cada bloco da memória principal pode ocupar apenas uma linha específica da cache.

## Exemplo de configuração com mapeamento associativo por conjunto

```python
CACHE_SIZE = 1024
BLOCK_SIZE = 32
ASSOC = 2
ADDR_BITS = 16
INPUT_FILE = "acessos_teste2.txt"
POLICY = "LRU"
VERBOSE = False
```

Nesse caso, a associatividade é `2`, então a cache funciona como 2-way set-associative. Cada conjunto possui duas linhas, e o programa procura a tag nas duas linhas do conjunto.

## Exemplo usando FIFO

```python
CACHE_SIZE = 1024
BLOCK_SIZE = 32
ASSOC = 2
ADDR_BITS = 16
INPUT_FILE = "acessos_teste2.txt"
POLICY = "FIFO"
VERBOSE = False
```

A política `FIFO` remove primeiro a linha que entrou primeiro no conjunto.

## Exemplo usando LRU

```python
CACHE_SIZE = 1024
BLOCK_SIZE = 32
ASSOC = 2
ADDR_BITS = 16
INPUT_FILE = "acessos_teste2.txt"
POLICY = "LRU"
VERBOSE = False
```

A política `LRU` remove a linha que foi usada há mais tempo.

## Modo detalhado

Para visualizar cada acesso passo a passo, altere a variável `VERBOSE` para `True` no arquivo `main.py`.

```python
VERBOSE = True
```

Com isso, o programa mostra:

* endereço acessado;
* tag;
* index;
* offset;
* se ocorreu hit ou miss;
* estado atual da cache após cada acesso.

## Formato do arquivo de entrada

O arquivo deve possuir um endereço por linha.

Os endereços podem estar em decimal:

```txt
16
32
48
```

Ou em hexadecimal:

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
Cache hits: 5 ( 50.00 % )
Cache misses: 5 ( 50.00 % )
=============================================
```

## Como o endereço é tratado

Para cada endereço lido do arquivo, o programa divide o valor em três partes:

* `tag`: identifica qual bloco da memória está armazenado naquela linha ou conjunto;
* `index`: indica em qual linha ou conjunto da cache o programa deve procurar;
* `offset`: indica a posição dentro do bloco.

Exemplo com o endereço `0x0010`, cache de 256 bytes, bloco de 16 bytes, associatividade 1 e endereço de 16 bits:

```txt
0x0010 em hexadecimal = 16 em decimal

bloco = endereço // tamanho do bloco
bloco = 16 // 16
bloco = 1

index = bloco % número de conjuntos
index = 1 % 16
index = 1

tag = bloco // número de conjuntos
tag = 1 // 16
tag = 0

offset = 0
```

Resultado:

```txt
TAG = 0
INDEX = 1
OFFSET = 0
```

Assim, o programa procura o endereço no conjunto ou linha `1` da cache e compara a tag armazenada com a tag `0`.

## Observações

O programa valida algumas entradas inválidas, como:

* cache que não é potência de 2;
* bloco que não é potência de 2;
* arquivo inexistente;
* endereço fora do limite definido por `ADDR_BITS`;
* configuração incompatível entre cache, bloco e associatividade;
* arquivo de entrada vazio ou sem endereços válidos.

## Estrutura geral do funcionamento

O funcionamento do programa pode ser resumido assim:

```txt
1. Define as configurações no main.py
2. Valida os parâmetros
3. Lê os endereços do arquivo .txt
4. Para cada endereço:
   - calcula tag, index e offset
   - procura o endereço na cache
   - verifica se foi hit ou miss
   - atualiza a cache, se necessário
5. Mostra o relatório final
```