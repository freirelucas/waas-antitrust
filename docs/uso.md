# Uso

## Instalação

Requer **Python 3.12+** (`mesa>=3.5` não instala em 3.10/3.11).

```bash
python3.12 -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
```

## Rodar o modelo

```python
from waas_antitrust.model import WaaSModel, WaaSParametros

params = WaaSParametros(regime="B", seed=42, n_tiques=40)
df = WaaSModel(params).executar()
print(df[["n_sinais", "verdadeiros_positivos_acum", "falsos_negativos_acum"]].tail())
```

Os três regimes institucionais são `"A"`, `"B"` e `"C"` (ver [Início](index.md)).
As métricas de **fluxo** (por tique) terminam em `_tique`; as de **estoque**
(acumuladas) terminam em `_acum`.

## Varredura de Sobol

A varredura usa replicação correta sobre seeds (a matriz inteira é avaliada por
réplica, preservando o pareamento de Saltelli) e os índices são mediados entre
réplicas:

```python
from waas_antitrust.sobol import PROBLEMA_SOBOL_8D, executar_varredura
from waas_antitrust.sobol.analise import calcular_indices_replicado

df = executar_varredura(n_base=64, regime="B", n_replicas=5)
indices = calcular_indices_replicado(df, PROBLEMA_SOBOL_8D, metrica="bem_estar")
print(indices)
```

Pela linha de comando:

```bash
waas-sobol --n-base 1024 --jobs -1 --out results/sobol_full.parquet
```

## Gerar figuras

```bash
waas-figuras --out figuras/ --formato ambos
```

Gera as figuras implementadas como módulo (inversão e fase). As demais
permanecem no caderno (backlog T01).

## Testes e lint

```bash
pytest -q tests/                  # suíte completa
pytest -q -m "not slow" tests/    # rápido, sem varreduras
ruff check src/ tests/ scripts/
black --check src/ tests/ scripts/
```

## Driver de fumaça

A skill `run-waas-antitrust` traz um driver que exercita modelo, Sobol e figuras
num passe só:

```bash
python .claude/skills/run-waas-antitrust/driver.py --out /tmp/waas-driver
```
