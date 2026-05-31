---
name: run-waas-antitrust
description: Compila, executa e dirige o modelo baseado em agentes waas-antitrust (Mesa 3.x) numa máquina Linux limpa — cria o venv Python 3.12, roda o modelo e a varredura de Sobol, gera as figuras do artigo (PNG) e roda os testes. Use ao pedir para run/launch/build/test/screenshot ou rodar/executar/simular o waas-antitrust, fazer uma varredura Sobol, ou gerar as figuras.
---

# run-waas-antitrust

`waas-antitrust` é um pacote científico em Python **sem GUI**: modelo baseado em
agentes (Mesa 3.x) + análise de sensibilidade de Sobol (SALib) + figuras em
Matplotlib + um caderno Jupyter. Não há servidor nem janela — dirige-se pela
**API Python** e por dois CLIs (`waas-sobol`, `waas-figuras`). O artefato visual
são as **figuras PNG** — o equivalente ao "screenshot" deste projeto.

O caminho de agente é o driver **`.claude/skills/run-waas-antitrust/driver.py`**:
num passe só ele exercita as quatro camadas que os PRs costumam tocar (modelo —
com dissuasão R01 e bem-estar R05; sobol; jogo_global R02; viz) e gera as figuras.

> Todos os caminhos são relativos à raiz do repositório.

## Pré-requisitos

**Python 3.12 é obrigatório** — `mesa>=3.5` não instala em 3.10/3.11. Nenhum
pacote de SO extra: o Matplotlib roda headless (backend Agg), sem display/xvfb.

```bash
python3.12 -m venv /home/user/.venv-waas
. /home/user/.venv-waas/bin/activate
```

## Build / instalação

```bash
pip install -e ".[dev]"
```

## Run (caminho de agente) — o driver

```bash
/home/user/.venv-waas/bin/python .claude/skills/run-waas-antitrust/driver.py --out /tmp/waas-driver
```

Imprime as métricas do modelo nos 3 regimes (VP/FP/FN/dano/bem-estar), os índices
de Sobol (ST) replicados, o limiar do jogo global e sua convergência (τ→0), e grava
2 PNGs em `/tmp/waas-driver/` (`01_inversao.png`, `02_fase.png`). **Abra os PNGs**
para inspeção visual. Código de saída 0 = tudo rodou.

## Invocação direta (API / CLI)

Camada de modelo (onde a maioria dos PRs mexe) — importar e chamar:

```bash
/home/user/.venv-waas/bin/python -c "
from waas_antitrust.model import WaaSModel, WaaSParametros
df = WaaSModel(WaaSParametros(regime='B', seed=42, n_tiques=20)).executar()
print(df[['n_sinais','verdadeiros_positivos_acum','falsos_negativos_acum']].tail(3).to_string())
"
```

CLIs (instalados como entry points pelo `pip install -e`):

```bash
waas-sobol --n-base 4 --n-replicas 2 --jobs 1 --n-empresas 3 --n-tiques 4 --out /tmp/sobol_smoke.parquet
waas-figuras --out /tmp/figs_smoke --formato png
```

Caderno-demo (porta de entrada, ~20 s; também é o que o badge do Colab abre):

```bash
pytest --nbval-lax notebooks/WaaS_demo.ipynb
```

## Testes

```bash
pytest -q tests/                  # 38 passam (inclui 1 teste lento de Sobol)
pytest -q -m "not slow" tests/    # 37, rápido (~7 s)
ruff check src/ tests/ scripts/   # limpo
black --check src/ tests/ scripts/
```

## Gotchas

- **Só Python 3.12+.** Em 3.10/3.11 o `pip install` falha com
  `No matching distribution found for mesa<4.0,>=3.5` (mesa 3.5 exige 3.12).
  `requires-python` e a matriz de CI já estão fixados em 3.12.
- **Figuras headless, sem xvfb.** O driver força `matplotlib.use("Agg")` antes de
  importar pyplot; `waas-figuras` também roda sem display. Não precisa de xvfb nem
  de libs GL.
- **Só 2 das "11" visualizações existem como módulo** (`inversao`, `fase`). As
  outras 9 (`sankey`, `painel`, …) são *stubs* que levantam `NotImplementedError`
  (estão no caderno; backlog T01). `waas-figuras` e o driver geram apenas as 2.
- **`bem_estar` é baseado em DANO, não em detecção (R05).** É `−(dano + β·FP + γ·custo)`.
  Logo, no horizonte longo, o Regime A pode ter mais VP que B (há mais crime a
  detectar quando ninguém é dissuadido) — isso é o ponto, não um bug. O sinal
  coerente é `dano_acumulado` (menor = melhor).
- **`waas-sobol` multiplica por réplicas.** `executar_varredura` roda a matriz
  inteira `n_replicas` vezes (padrão 5): `n_base=4, n_replicas=2` → 4·(8+2)·2 = 80
  amostras. O joblib imprime progresso no stderr (verbose=10) — é ruído, não erro.
- **Em populações pequenas o Sobol pode emitir `RuntimeWarning: divide by zero`**
  (variância nula com poucas amostras) e a dissuasão (R01) pode super-deter (a
  detecção percebida `vp/violadoras` é ruidosa). Use n_empresas ≥ 20 para o quadro
  representativo; some no smoke test.

## Troubleshooting

- `No matching distribution found for mesa<4.0,>=3.5` → o venv está em Python
  <3.12. Recrie com `python3.12 -m venv`.
- `ModuleNotFoundError: No module named 'waas_antitrust'` → venv não ativo ou
  faltou `pip install -e ".[dev]"`.
- Erro de display/Tkinter ao gerar figura → garanta `matplotlib.use("Agg")` antes
  de importar `pyplot` (o driver já faz isso).
