# Comandos — todos os scripts e CLIs

<p class="deck">Inventário das ferramentas executáveis do projeto: dois <em>entry points</em> instalados via <code>pip install -e .</code> (<code>waas-sobol</code>, <code>waas-figuras</code>); dez scripts em <code>scripts/</code> para análises específicas; vinte e dois módulos de visualização invocáveis via <code>python -m waas_antitrust.viz.&lt;nome&gt;</code>. Esta página é a referência rápida; para o tutorial guiado por perfil de uso, ver <a href="uso.md">Como usar</a>.</p>

## Entry points instalados (CLI)

Após `pip install -e ".[dev]"`, dois comandos ficam no PATH:

### `waas-sobol` — varredura paramétrica global

```bash
# Validação rápida (5-10 min)
waas-sobol --n-base 128 --n-replicas 3 --regime B --out results/sobol_quick.parquet

# Paper-grade (várias horas)
waas-sobol --n-base 1024 --jobs -1 --regime B --out results/sobol_full.parquet
```

Implementação em `src/waas_antitrust/cli.py:sobol`. Carrega o problema 8D de
`sobol/problema.py` (`PROBLEMA_SOBOL_8D` com bounds em W_mult, k_rel, D_disc, rho,
r_represalia, F_falso, densidade, taxa_observacao); chama
`sobol/execucao.executar_varredura` que usa joblib para paralelizar; grava `.parquet`
com `N·(2d+2)·n_replicas` linhas. A análise dos índices ($S_1$, $S_T$) faz-se
depois com `sobol.analise.calcular_indices_replicado(df, PROBLEMA_SOBOL_8D, metrica="bem_estar")`.

| Argumento | Default | Descrição |
|---|---|---|
| `--n-base N` | 128 | Total = $N \cdot (2d+2) \cdot$ réplicas; 128 valida, 1024 paper-grade |
| `--n-replicas K` | 5 | Réplicas da matriz inteira; mediadas nos índices |
| `--regime` | B | A / B / C |
| `--jobs J` | -1 | Núcleos (-1 = todos) |
| `--n-empresas` | 15 | Empresas por execução |
| `--n-tiques` | 24 | Horizonte em trimestres |
| `--out` | `results/sobol.parquet` | Arquivo de saída |

### `waas-figuras` — gera as figuras tipo conceitual

```bash
waas-figuras --out figuras/ --formato ambos     # png + svg
waas-figuras --out figuras/ --formato todos     # png + svg + pdf
```

Gera as figuras conceituais (`inversao`, `fase`) — para todas as 21 publicadas no
site, use `scripts/regerar_todas_as_figuras.py`.

## Scripts em `scripts/` (10)

| Script | O que faz | Saída |
|---|---|---|
| `calibrar.py` | Calibração ingênua R03 em grid sobre 3 alvos (primeira ponta) | Stdout: top-5 pontos |
| `calibrar_formal.py` | **Calibração formal R03** sobre problema reduzido com Nelder-Mead | `results/calibracao_formal_r03.json` |
| `identificabilidade_r03.py` | 175 rodadas 1D que decompõem o "conflito de 3 alvos" | `results/identificabilidade_r03.parquet` |
| `varredura_alpha_erosao.py` | Varredura grade 10 seeds × 8 alphas que falsifica Prop. 5 forte | `results/alpha_erosao_grade.parquet` |
| `mapa_lambda_hirschman.py` | Mapa de regime (λ × peso_hirschman) — resposta ao Mat A | `results/mapa_lambda_hirschman.parquet` + `docs/img/19_…` |
| `gerar_figura_dissuasao.py` | Figura central da home (dissuasão e bem-estar A/B/C) | `docs/img/03_dissuasao_bem_estar.png` |
| `gerar_figs_paper.py` | Regenera as 4 PDFs do paper a partir dos módulos viz | `paper/figs/0[1-4]_*.pdf` |
| `regerar_todas_as_figuras.py` | **Orquestrador**: regera todas as 23 figuras do site em sequência | `docs/img/*.png` |
| `gerar_figuras.py` | Gera as figuras conceituais simples (inversão, fase) | `figuras/*.{png,svg,pdf}` |
| `run_sobol_full.py` | Varredura Sobol full paper-grade — wrapper do `waas-sobol` | `results/sobol_full.parquet` |

Cada um aceita `--help` para a lista de flags.

## Módulos viz invocáveis

Todos os 18 módulos de figura aceitam invocação direta como módulo:

```bash
# Modo único — gera 1 figura em docs/img/<NN>_*.png
python -m waas_antitrust.viz.choques        # figura 20 — 5 catálogos de choque
python -m waas_antitrust.viz.identificabilidade  # figura 21 — sensibilidade R03
python -m waas_antitrust.viz.painel         # figura 18 — síntese 2×3
python -m waas_antitrust.viz.alpha_erosao_limiar  # figura 10 — falsificação Prop. 5
python -m waas_antitrust.viz.internacional  # figura 13 — 3 jurisdições
```

A lista canônica está em [`roadmap_figuras.md`](roadmap_figuras.md).

## Fluxos sugeridos

### Quero reproduzir TUDO

```bash
git clone https://github.com/freirelucas/waas-antitrust.git
cd waas-antitrust && pip install -e ".[dev]"

# 1. Os 4 artefatos científicos da rodada
python scripts/varredura_alpha_erosao.py          # falsifica Prop. 5 forte
python scripts/identificabilidade_r03.py          # decompõe os 3 alvos
python scripts/calibrar_formal.py                 # calibração formal
python scripts/mapa_lambda_hirschman.py           # mapa Mat A

# 2. Todas as 23 figuras do site (5-10 min)
python scripts/regerar_todas_as_figuras.py

# 3. Os 4 PDFs do paper
python scripts/gerar_figs_paper.py

# 4. Sobol paper-grade (várias horas)
waas-sobol --n-base 1024 --jobs -1 --out results/sobol_full.parquet
```

### Quero brincar interativamente

Abra o [simulador in-browser](brincar.md): roda no navegador, 13 sliders, atualização em <300 ms. Para a versão Python plena (sem aproximações), abra `notebooks/WaaS_brincar.ipynb` localmente com `jupyter notebook`.

### Quero rodar testes

```bash
# Suite completa (~25s, 343 testes)
pytest -x -q -m "not slow"

# Apenas os testes de regressão dos achados científicos
pytest -x -q tests/test_achados_rodada.py

# Apenas viz (com nbval do demo)
pytest -x -q tests/test_viz.py
pytest --nbval-lax notebooks/WaaS_demo.ipynb
```
