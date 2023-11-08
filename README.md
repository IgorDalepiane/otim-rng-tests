# Otimização de Algoritmos - PPGES 2023/02

#### Capítulo 16.7 (Random number generation) do livro "The Algorithm Design Manual", de Skiena

Alunos: [Igor Costa](https://github.com/IgorDalepiane) e [Lucas Fell](https://github.com/fell-lucas)

### Dependências:

- memory-profiler==0.61.0
- matplotlib==3.8.1
- scipy==1.11.3
- numpy==1.26.1
- argparse==1.4.0

Para instalar, basta executar o comando:

```bash
pip install -r requirements.txt
```
#### Códigos fontes

 - Algoritmo LCG: https://github.com/rossilor95/lcg-python/blob/main/lcg.py
 - Algoritmo Mersenne Twister: https://github.com/python/cpython/blob/3.12/Lib/random.py

### Execução:

Para executar o programa, basta executar o comando:

```bash
python3 main.py
```

Opcionalmente, você pode passar os seguntes argumentos:

- `--lcg_modulus`: Módulo 'm' do LCG, padrão: 4_294_967_296
- `--lcg_multiplier`: Multiplicador 'a' do LCG, padrão: 594_156_893
- `--lcg_increment`: Incremento 'c' do LCG, padrão: 0
- `--seed`: Semente inicial dos algoritmos LCG e MT, padrão: gerada aleatoriamente
- `--count`: Quantidade de números aleatórios a serem gerados, padrão: testes de 1000, 100000 e 1000000 números
- `--max_range`: Valor máximo dos números aleatórios gerados, padrão: 1000000

Exemplo:

```bash
python3 main.py --lcg_modulus 4294967296 --lcg_multiplier 594156893 --lcg_increment 0 --seed 123456789 --count 1000 --max_range 1000000
```

### Resultados:

Os resultados serão salvos no diretório `plots/` com o nome `<seed>_<count>.png`.
