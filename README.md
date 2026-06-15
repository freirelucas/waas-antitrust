<div align="center">

# LCMC

### Leniência Condicionada à Massa Crítica

**Canal de depósito condicional · operado pelo CADE · sem necessidade de lei nova**

*Aplicada ao antitruste de mercados digitais brasileiros*

[![Site](https://img.shields.io/badge/site-freirelucas.github.io%2Fwaas--antitrust-1e8449?style=for-the-badge&logo=readthedocs&logoColor=white)](https://freirelucas.github.io/waas-antitrust/)
[![Brincar in-browser](https://img.shields.io/badge/brincar%20in--browser-simulador%20JS-27AE60?style=for-the-badge&logo=googlechrome&logoColor=white)](https://freirelucas.github.io/waas-antitrust/brincar/)
[![Paper](https://img.shields.io/badge/paper-rascunho%20v0.2.0-blue?style=for-the-badge&logo=overleaf&logoColor=white)](https://github.com/freirelucas/waas-antitrust/blob/main/paper/main.tex)

[![CI](https://img.shields.io/badge/pytest-354%20passed-brightgreen?style=flat-square)](https://github.com/freirelucas/waas-antitrust/actions)
[![Licença](https://img.shields.io/badge/licen%C3%A7a-CC%20BY--SA%204.0-blue?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12+-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Mesa](https://img.shields.io/badge/mesa-3.x-green?style=flat-square)](https://mesa.readthedocs.io/)

</div>

---

## A pergunta

Em mercados digitais, **o abuso vem de uma firma só**: auto-preferência do Google, *anti-steering* da Apple, exclusividade do iFood, *killer acquisition* da Meta. Não há cúmplice externo para delatar. A leniência clássica — que sempre foi a peça-mestre do enforcement antitruste — não funciona.

A informação existe **dentro da própria empresa**: no Slack do time de produto, na ata do comitê de aquisições, no slide-deck da reunião comercial. Mas ela não circula. No Brasil de hoje, o trabalhador que falaria arrisca emprego, carreira, tranquilidade — e ganha **nada de previsível** em troca.

## A resposta: LCMC

A **Leniência Condicionada à Massa Crítica (LCMC)** é um *canal de depósito condicional* operado pelo CADE. O trabalhador deposita uma denúncia que **só se abre** quando outros trabalhadores da mesma firma também depositarem. Sem cooperação suficiente, ninguém é exposto. Com cooperação, todas as denúncias se abrem simultaneamente.

Em três paralelos:

|  |  |
|---|---|
| 🎯 **Kickstarter** | seu cartão só é cobrado se o projeto atingir a meta de apoiadores |
| 🛡️ **Callisto** ([callisto.org](https://www.callisto.org)) | em operação nos EUA desde 2015 — denúncia de assédio só revela o nome se outra vítima identificar o **mesmo** agressor |
| 📦 **Caixa-cofre** | envelopes com denúncias só abrem quando há ao menos N envelopes parecidos contra a mesma empresa |

O nome acadêmico desse desenho é ***information escrow***, formalizado por **Ian Ayres e Cait Unkovic** (Yale Law School) em *Michigan Law Review* 111:145 (2012). A LCMC aplica esse desenho ao antitruste brasileiro, com o CADE como o "terceiro confiável" que opera a caixa-cofre.

**Base normativa autônoma**: Art. 4º, II e III da Lei 12.529/2011 c/c Lei 9.784/99 — o CADE pode disciplinar o procedimento **sem lei nova** e sem depender da re-caracterização do Art. 12 da Resolução 21/2018.

## A LCMC é um mecanismo de coordenação, não de pagamento

A LCMC resolve o problema clássico de Olson (1965): em grupos pequenos, ninguém quer ser o primeiro a se expor; cada um prefere esperar o outro começar. O canal **elimina esse impasse por construção** — a denúncia individual nunca fica exposta sozinha enquanto a massa crítica não se forma.

**Acoplados opcionalmente ao canal**, cinco instrumentos de internalização podem amplificar a adesão:

| Instrumento | Quem paga · Para quem · Como |
|---|---|
| **Canal puro (LCMC sem instrumento)** | Configuração mais conservadora: só o procedimento administrativo do CADE. Sem categoria sancionatória nova. Risco F6 (anulação judicial) cai materialmente |
| **WaaS — recompensa via TCC** | Firma paga trabalhador; pagamento re-caracterizado como ressarcimento sob Art. 12 Res. 21/2018 |
| **Hirschman — vesting acelerado** | Firma paga via equity; gatilho contratual de ação coletiva (R07, requer Regime C) |
| **Crédito tributário** | Estado paga via renúncia fiscal (R22 stub; requer LC + LRF) |
| **Leniência criminal individual** | Estado oferece não-persecução (R23 stub; reserva penal estrita Art. 5º XXXIX CF) |

O **WaaS é apenas um dos cinco instrumentos**. Quando ele é o acoplamento ativo, emerge a aritmética IC-F\*: a firma compara desconto $D$ contra recompensa $W$. Mas o canal LCMC funciona **mesmo sem nenhum instrumento monetário** — operando puramente pela coordenação que o escrow institucionaliza.

## Os números

<div align="center">

| **R$ 12,3 mi** | **1.679 firmas** | **+1.363%** | **343 testes** |
|:---:|:---:|:---:|:---:|
| margem da firma sob TCC-WaaS (instrumento monetário) para receita de R$ 1 bi | universo CADE implícito após calibração formal R03 | ΔW de Regime B sobre A em bem-estar agregado | verdes em ~25s · 21 figuras reproduzíveis |

</div>

## A figura central

![Dissuasão endógena e bem-estar — 3 regimes A/B/C ao longo de 40 trimestres, saída direta do modelo executado](docs/img/03_dissuasao_bem_estar.png)

> **Saída literal** do modelo, *seed* 11, regimes A/B/C lado a lado. **(A)** Violadoras ativas ao longo do tempo: regime A (cinza) cresce e estabiliza alto; regimes B/C (verde/roxo) caem a zero em ~17 tiques sob LCMC ativa. **(B)** Bem-estar social agregado. ΔW (B sobre A) = +1363%. **Reprodução em 60 segundos**: `python scripts/gerar_figura_dissuasao.py`.

## Para quem é

| Você é | Comece por | Em ~1 clique |
|---|---|---|
| 📰 **Jornalista** | [Kit de imprensa](https://freirelucas.github.io/waas-antitrust/imprensa/) | 3 leads + 6 números com fonte + autor e contato |
| ⚖️ **Advogada/o** | [Análise institucional](https://freirelucas.github.io/waas-antitrust/INSTITUTIONAL/) | Base autônoma Art. 4º + vetores atacáveis F6, reserva de lei |
| 📐 **Economista** | [Formulário matemático](https://freirelucas.github.io/waas-antitrust/formulario/) | IC-F\* nas 3 formas + bem-estar + calibração formal R03 |
| 🏛️ **Autoridade** | [Procedimento administrativo](https://freirelucas.github.io/waas-antitrust/procedimento_cade/) | Fluxograma 7 etapas + sigilo Lei 9.784 Art. 24 |
| 🏢 **Big Tech** | [Compliance corporativo](https://freirelucas.github.io/waas-antitrust/compliance_corporativo/) | Aritmética R$ + 4 vetores corporativos materiais |
| 🎓 **Academia** | [Paper](https://freirelucas.github.io/waas-antitrust/paper/) · [Bem coletivo](https://freirelucas.github.io/waas-antitrust/bem_publico/) | Ostrom-Coleman-Olson + falsificação Prop. 5 forte |
| 🧪 **Curiosa/o** | [Brincar in-browser](https://freirelucas.github.io/waas-antitrust/brincar/) | 13 sliders + 4 gráficos em tempo real, sem download — implementa R27/R29 |

## Instalação em 3 comandos

Requer **Python 3.12+** (`mesa>=3.5`).

```bash
git clone https://github.com/freirelucas/waas-antitrust.git
cd waas-antitrust && pip install -e ".[dev]"
pytest -x -q  # 343 testes em ~25s
```

Para usar como biblioteca, sem clonar:

```bash
pip install "waas-antitrust @ git+https://github.com/freirelucas/waas-antitrust.git"
```

> O **pacote Python** mantém o nome `waas_antitrust` por compatibilidade — o nome do conceito central evoluiu para LCMC, mas renomear o pacote quebraria toda a base de código existente.

## Fluxos típicos

```bash
# 1. Brincar interativamente — abre o simulador in-browser, sem instalação
open https://freirelucas.github.io/waas-antitrust/brincar/

# 2. Reproduzir os 3 achados científicos da rodada de jun/2026
python scripts/varredura_alpha_erosao.py     # falsifica Prop. 5 forte
python scripts/identificabilidade_r03.py     # decompõe os 3 alvos do R03
python scripts/calibrar_formal.py            # calibração Nelder-Mead → (0.323; 0.481)

# 3. Regerar todas as 21 figuras do site (5-10 min)
python scripts/regerar_todas_as_figuras.py

# 4. Varredura Sobol paper-grade (várias horas)
waas-sobol --n-base 1024 --jobs -1 --out results/sobol_full.parquet

# 5. Compilar o paper
python scripts/gerar_figs_paper.py
cd paper && pdflatex main && bibtex main && pdflatex main && pdflatex main
```

## Estrutura do código

```
waas-antitrust/
├── src/waas_antitrust/
│   ├── agents.py            # TrabalhadorAgent · EmpresaAgent · AutoridadeAgent
│   │                        # (Autoridade carrega o escrow LCMC: R27)
│   ├── model.py             # WaaSModel + WaaSParametros (40+ campos opt-in)
│   ├── corrida.py           # LCMC (R20) — gradiente Saito intra/inter-firma
│   ├── cenarios.py          # 19 cenários canônicos (status quo, EUA, UE, …)
│   ├── instrumentos.py      # 5 entradas: canal LCMC + 4 instrumentos opcionais
│   ├── condutas.py          # 28 condutas digitais com casos verificados
│   ├── choques.py           # 5 catálogos de choque (Tech cíclico vs IA estrutural)
│   ├── hirschman.py         # Exit-with-equity (R07, instrumento opcional)
│   ├── normas/              # Parser LexML BR (T07 fechado, 540 linhas)
│   ├── sobol/               # Varredura paramétrica (joblib paralelo)
│   ├── calibracao/          # Saito 2021, RIG/TCU 2022-2024, Brasscom 2024
│   └── viz/                 # 20 módulos: gerar_figura(...) → 21 PNGs em docs/img/
├── scripts/                 # 10 scripts (calibração, varreduras, geração)
├── tests/                   # 343 testes + nbval
├── notebooks/               # WaaS_demo (CI) + WaaS_brincar (12 sliders)
├── data/normas/             # Corpus LexML (Lei 12.529, 13.608, Res. 21/2018)
├── paper/                   # LaTeX + bib (25 citações; rascunho v0.2.0)
└── docs/                    # MkDocs Material — 27 páginas + 21 figuras
```

## Achados científicos protegidos por teste

`tests/test_achados_rodada.py` é o gate de regressão dos 5 achados centrais:

- **Prop. 5 forte falsificada empiricamente** (varredura 10 seeds × 8 alphas × 40 tiques): dano em Regime B fica ~8× abaixo do piso A estável até $\alpha = 0{,}9$
- **Prop. 5 fraca verificada**: capital social residual decai monotonicamente com $\alpha$
- **Calibração formal R03**: ponto ótimo $(f_v, t_c) = (0{,}323; 0{,}481)$ produz 0,56 TCC/ano contra alvo normalizado 0,60 (erro 6,65%)
- **Identificabilidade dissolvida**: 175 rodadas 1D mostram `rho` ortogonal ao alvo; sai da função objetivo
- **Mapa $(\lambda, \beta_H)$**: sem evidência de bifurcação na grade — Mat A resolvido empiricamente

Cada achado é descrito em [`docs/limitacoes.md`](https://freirelucas.github.io/waas-antitrust/limitacoes/) e [`docs/transparencia.md`](https://freirelucas.github.io/waas-antitrust/transparencia/).

## Como citar

`CITATION.cff` na raiz contém metadados estruturados. DOI Zenodo após congelamento da versão de submissão.

```
L. (2026). LCMC: Leniency Conditional on Critical Mass — a conditional-deposit
channel for unilateral conduct in Brazilian digital markets (agent-based model).
URL: https://github.com/freirelucas/waas-antitrust
```

## Licença

Código e documentação sob [Creative Commons Atribuição-CompartilhaIgual 4.0 Internacional](LICENSE) (CC BY-SA 4.0).

---

<div align="center">

*Proposição acadêmica independente. O autor mantém este repositório sem vinculação institucional formal a CADE, IPEA ou qualquer organização privada.*

[Site MkDocs](https://freirelucas.github.io/waas-antitrust/) · [Brincar in-browser](https://freirelucas.github.io/waas-antitrust/brincar/) · [Paper](https://github.com/freirelucas/waas-antitrust/blob/main/paper/main.tex) · [Backlog](https://freirelucas.github.io/waas-antitrust/DECISIONS/)

</div>
