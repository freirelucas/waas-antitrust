# Como usar

<p class="deck">Guia operacional para quatro perfis de uso: leitor que quer apenas explorar (simulador in-browser, sem instalar), cético que quer rodar localmente e contestar, calibrador que quer ajustar parâmetros contra dados reais e desenvolvedor que quer escrever testes ou propor extensão. Cada perfil tem caminho próprio abaixo; a instalação local completa fica pronta em menos de um minuto em Python 3.12.</p>

Este guia operacional cobre quatro perfis de uso: **leigo** (simulador in-browser, sem instalar), **cético** (rodar localmente e contestar), **calibrador** (ajustar parâmetros contra dados reais), e **desenvolvedor** (escrever testes e propor PR).

## Caminho rápido — simulador in-browser

Para uma primeira aproximação sem instalação, abra o [simulador interativo](brincar.md): roda no navegador, 13 sliders, atualização em <300 ms por rodada. É uma versão reduzida do modelo Python (P1–P4), suficiente para entender qualitativamente o efeito do canal e da janela de adesão; os achados científicos do projeto vêm do modelo cheio rodado localmente (próxima seção).

## Instalação local

Requer **Python 3.12+** (`mesa >= 3.5` não instala em Python 3.10/3.11).

```bash
git clone https://github.com/freirelucas/waas-antitrust.git
cd waas-antitrust
python3.12 -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
```

Validar que tudo instalou (deve mostrar `331 passed`):

```bash
pytest -x -q -m "not slow" tests/
```

## Rodar o modelo — caso mínimo

```python
from waas_antitrust.model import WaaSModel, WaaSParametros

params = WaaSParametros(regime="B", seed=42, n_tiques=40)
df = WaaSModel(params).executar()

# DataFrame com 40 linhas × 34 colunas
print(df[["n_sinais", "n_violadoras_ativas", "dano_acumulado",
          "capital_social_residual", "valor_dissuasao_difusa_acum"]].tail())
```

Os três regimes institucionais são `"A"` (status quo), `"B"` (Resolução CADE) e `"C"` (Lei). Convenção de nomes:

- métricas de **fluxo** (por tique): terminam em `_tique` (e.g. `vp_tique`)
- métricas de **estoque** (cumulativas): terminam em `_acum` (e.g. `dano_acumulado`)

## Ativar LCMC (modo corrida, R20)

Sob `modo_corrida=True`, o modelo aplica a Leniência Condicionada à Massa Crítica plena: gatilho `q_min` + decaimento Saito intra/inter-firma.

```python
from waas_antitrust.cenarios import aplicar_cenario
from waas_antitrust.model import WaaSModel, WaaSParametros

# Cenário canônico de LCMC + WaaS
p = aplicar_cenario(
    WaaSParametros(n_empresas=20, n_tiques=40, seed=11),
    "cenario_corrida_leniencia",
)
df = WaaSModel(p).executar()
print(f"firmas que atingiram massa crítica interna: "
      f"{df['n_firmas_atingiram_massa_critica_interna'].max()}")
```

27 cenários canônicos disponíveis (incluindo os 6 do reframe v2, os 2 do R28 EUA/UE, os 2 do canal puro + erosão Coleman, os 3 do R29 — cascata arbitrária, calibração Saito 2021 e cruzamento R29 × R26 —, os 4 do R30 — coordenada, descoordenada, assimétrica e com forum shopping — e a recompensa coletiva R29-iv):

```python
from waas_antitrust.cenarios import listar_cenarios
for nome in listar_cenarios():
    print(f"  {nome}")
```

## Customizar parâmetros — vetores de quebra

`WaaSParametros` expõe ~30 parâmetros documentados. Os principais para falsificar o desenho:

```python
WaaSParametros(
    # Vetor A — TCC clássico (Art. 85) já dá desconto
    D_disc=0.30,
    D_disc_base_tcc=0.20,         # ⇒ D_extra=0.10, ICᶠ* difícil

    # Vetor B — Judiciário anula TCC-WaaS (F6)
    p_anulacao_tcc=0.10,

    # Vetor C — custo legal individual do denunciante
    custo_legal_uw=0.30,           # 30% de salário anual

    # Vetor D (R26) — erosão Coleman do capital social
    alpha_erosao=0.2,

    # Vetor E (Cient. Político v2) — gargalo CADE
    taxa_capacidade=0.10,          # 180 servidores área-fim do RIG 2024

    # Reframe v2 — uso adversarial (R24)
    distribuicao_arquetipos={
        "ético": 0.10, "imitativo": 0.30, "racional": 0.30,
        "fairminded": 0.10, "aleatório": 0.00, "oportunista": 0.20,
    },
)
```

## Inspecionar agentes (micro)

Após `model.executar()`, todos os agentes ficam acessíveis como objetos Python comuns:

```python
m = WaaSModel(WaaSParametros(n_empresas=4, n_tiques=10, seed=23, regime="B"))
m.executar()

# Trabalhadores de uma firma específica
for t in m.trabalhadores_por_empresa[0][:5]:
    print(f"  {t.arquetipo:13s} · papel={t.papel:9s} · "
          f"observou={t.observou} · sinalizou={t.sinaliza_agora}")

# Empresas
for e in m.empresas:
    print(f"  firma {e.unique_id}: viola={e.eh_violadora}, "
          f"conduta={e.conduta_potencial}, TCC={e.tcc_assinado}")

# Autoridade
print(f"  CADE: p_perc={m.p_perc:.3f}, kappa={m.autoridade.capacidade}")
```

## Telas de simulação (viz)

Duas telas matplotlib materializam o comportamento micro/macro:

```python
from waas_antitrust.viz import painel_macro, painel_micro

m = WaaSModel(WaaSParametros(
    n_empresas=10, n_tiques=20, seed=37, regime="B",
    modo_corrida=True, alpha_erosao=0.2,
))
m.executar()

# Tela macro 2×2: p_perc, massa crítica, bem-estar, capital social
fig_macro, _ = painel_macro.gerar_figura()
fig_macro.savefig("painel_macro.png", dpi=150)

# Tela micro 2×2 de UMA firma: arquétipos, papéis, estado, fila LCMC
fig_micro, _ = painel_micro.gerar_figura(m, fid=0)
fig_micro.savefig("painel_micro_firma0.png", dpi=150)
```

Outras figuras: `viz.cascata` (formação de massa crítica), `viz.erosao` (Proposição 5 Coleman), `viz.inversao`, `viz.fase`.

## Varredura de Sobol (análise de sensibilidade)

A varredura usa replicação correta sobre seeds (matriz inteira por réplica, preservando pareamento de Saltelli) e os índices são mediados entre réplicas:

```python
from waas_antitrust.sobol import PROBLEMA_SOBOL_8D, executar_varredura
from waas_antitrust.sobol.analise import calcular_indices_replicado

df = executar_varredura(n_base=64, regime="B", n_replicas=5)
indices = calcular_indices_replicado(df, PROBLEMA_SOBOL_8D, metrica="bem_estar")
print(indices)
```

Versão paper-grade (várias horas):

```bash
waas-sobol --n-base 1024 --jobs -1 --out results/sobol_full.parquet
```

## Gates de qualidade

Antes de propor PR, rodar:

```bash
pytest -x -q -m "not slow" tests/   # 331 testes, ~25s
ruff check src/ tests/ scripts/
black --check src/ tests/ scripts/
mkdocs build --strict               # site sem warnings
```

A skill `run-waas-antitrust` traz um driver que exercita modelo + Sobol + figuras num passe só:

```bash
python .claude/skills/run-waas-antitrust/driver.py --out /tmp/waas-driver
```

## Estrutura do código

```
src/waas_antitrust/
├── agents.py              # TrabalhadorAgent, EmpresaAgent, AutoridadeAgent
├── model.py               # WaaSModel + WaaSParametros (~30 params)
├── cenarios.py            # 27 cenários canônicos + aplicar_cenario
├── instrumentos.py        # 5 entradas: canal base (v3) + 4 instrumentos
├── corrida.py             # FilaInternaCooperacao + FilaLeniencia (LCMC)
├── hirschman.py           # custo_exodo_esperado (R07)
├── condutas.py            # 28 condutas digitais × 10 papéis
├── choques.py             # Choques exógenos (Eurace@Unibi, R19)
├── robustez.py            # bootstrap_ci, beta_binomial_smoothing
├── jogo_global.py         # limiar Morris-Shin (+ por posição, R20)
├── calibracao/            # saito, cade, transparencia_cade, brasscom
├── normas/                # urn, articulacao, remissoes, corpus, cite (T07)
├── viz/                   # paleta + 5 figuras (cascata, erosao, painel_*, ...)
└── sobol/                 # problema, execucao, analise
```

Para visão completa de quem decide o quê, ver [Modelagem multiagente](modelagem_multiagente.md).
