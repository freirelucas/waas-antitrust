# Instruções para o Claude Code

Este arquivo orienta o uso do Claude Code neste repositório. Siga estritamente.

## Linguagem e estilo

- **Idioma**: todos os textos (commits, comentários, docstrings, READMEs, documentação) em **português brasileiro acadêmico**. Sem anglicismos quando houver termo português estabelecido. Manter siglas estabelecidas na literatura científica (ABM, IC, IR, ODD, NATO, VSM).
- **Vocabulário canônico** (não substitua):
  - `denunciante interno` (não *whistleblower*)
  - `recompensa` (não *bounty*)
  - `conformidade` (não *compliance*) — exceto quando referir à literatura jurídica brasileira que adota o anglicismo
  - `cenários adversariais` ou `análise de resistência` (não *stress tests*)
  - `varredura` (não *sweep*)
  - `reamostragem` ou `reamostragem bootstrap` (manter bootstrap entre parênteses na primeira ocorrência)
  - `pequeno-mundo` (não *small-world*)
  - `contágio complexo` (Centola-Macy)
  - `jogo global` (Morris-Shin)
  - `massa crítica`, `conhecimento comum`, `variedade requisitada`
- **Variáveis Python**: em inglês quando seguirem convenção estabelecida (`model`, `step`, `seed`, `rng`); em português para conceitos do domínio (`empresa`, `denunciante`, `recompensa`, `tique`).
- **Strings de saída** (títulos de figura, mensagens de log, docstrings): em português.

## Convenções de código

- **Formatação**: `black` (linha 100) e `ruff` (configurado em `pyproject.toml`).
- **Tipagem**: gradual; use type hints em assinaturas públicas.
- **Testes**: `pytest` + `nbval` para validar o caderno. Cobertura-alvo: 80%.
- **Commits**: estilo *Conventional Commits* em português. Exemplos:
  - `feat: adiciona módulo de calibração Brasscom 2024`
  - `fix(model): corrige sinal residual de auto-detecção no Regime A`
  - `docs: amplia seção sobre Art. 12 da Res. 21/2018`
  - `test: adiciona teste de regressão para a Proposição 1`
- **Estrutura**: cada visualização é um módulo em `src/waas_antitrust/viz/`. Cada calibração externa é um módulo em `calibracao/`.

## Conjunto técnico (não substituir sem motivo)

- Modelagem: **Mesa 3.x** (não Mesa 1.x). Atenção: a API mudou.
- Redes: **NetworkX**. Pequeno-mundo via `watts_strogatz_graph`.
- Sensibilidade: **SALib** (Sobol).
- Análise: **NumPy/Pandas**. Para Sobol assíncrono: **joblib** ou **multiprocessing**.
- Gráficos: **Matplotlib/Seaborn**. Paleta unificada em `viz/paleta.py`; **respeitar**.

## Restrições científicas

- **Não invente referências**. Toda citação deve ser verificável.
- **Toda calibração** contra dados externos deve referenciar a fonte primária no docstring do módulo.
- **Não altere a interpretação teórica** (jogo global, contágio complexo, amplificação de variedade) sem revisão.
- **Proposições 1 a 3** estão no `docs/ODD.md` com esboços de prova. Mudanças no modelo que afetem essas proposições exigem revisão dos esboços.

## Restrições jurídicas

- A análise institucional brasileira parte de **três fontes primárias**: Lei 12.529/2011, Lei 13.608/2018 (com redação da Lei 13.964/2019), Resolução CADE nº 21/2018. **Cite verbatim quando central ao argumento.**
- **Não infira posições do CADE** que não estejam em documentos oficiais. Esta é uma proposição acadêmica, não institucional.
- O autor mantém o repositório independentemente do IPEA. **Não atribua a publicação ao IPEA sem revisão explícita.**

## Como expandir o projeto

- **Nova visualização**: crie módulo em `src/waas_antitrust/viz/`, exponha função `gerar_figura(...)` que retorna `(fig, ax)`. Adicione caso de teste em `tests/test_viz.py`. Registre no `scripts/gerar_figuras.py`.
- **Nova calibração**: módulo em `calibracao/` com docstring contendo fonte primária. Adicione fixture em `tests/conftest.py`.
- **Nova proposição teórica**: documente em `docs/ODD.md` com esboço de prova. Adicione teste de regressão correspondente.

## Operações comuns

```bash
# Testes rápidos (sem nbval)
pytest -x -q tests/

# Testes incluindo o caderno
pytest --nbval-lax notebooks/

# Lint e formatação
ruff check src/ tests/
black --check src/ tests/
pre-commit run --all-files

# Varredura Sobol curta (validação)
python scripts/run_sobol_full.py --n-base 64 --jobs 4 --out results/sobol_quick.parquet

# Varredura completa (paper-grade, várias horas)
python scripts/run_sobol_full.py --n-base 1024 --jobs -1 --out results/sobol_full.parquet
```

## Reprodutibilidade

- Toda execução longa deve gravar `results/<nome>.parquet` com colunas: parâmetros, seeds, métricas.
- O caderno `notebooks/WaaS_caderno_v2.ipynb` deve continuar executável (testado em CI via `nbval`).
- Antes de qualquer publicação, registrar release no Zenodo via `.zenodo.json`.

## Decisões em aberto (rastreadas)

Consulte `docs/DECISIONS.md` para a lista de decisões pendentes que afetam o desenho do mecanismo, incluindo:
- Reserva de lei vs. resolução infralegal
- Modelagem do Advogado/Assessoria jurídica como agente estratégico
- Calibração da topologia de redes intra-firma (instrumento empírico)
- Co-autoria com Felipe Roquete (origem da hipótese, vide histórico do autor)
