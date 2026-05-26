# Decisões em aberto e backlog

Decisões rastreadas que afetam o desenho do mecanismo ou a arquitetura do código.

## Conceituais

| # | Decisão | Status | Observação |
|---|---|---|---|
| D01 | Caminho via Resolução vs. via Lei | aberta | Preferência inicial: Resolução. Reverificar com falsificador F6. |
| D02 | Modelar a Assessoria jurídica como agente estratégico? | aberta | Hoje colapsada em intermediário transparente. |
| D03 | Calibrar topologia de redes intra-firma via instrumento empírico | aberta | Requer survey ou aproximação via LinkedIn (aprovação ética). |
| D04 | Co-autoria com Felipe Roquete | aberta | Hipótese original surgiu em conversa de 06/09/2022. |
| D05 | Versão completa da IC-F* (não simplificada) | aberta | Hoje usa D > W; versão completa requer modelar p_detecção endógeno. |

## Técnicas

| # | Decisão | Status | Observação |
|---|---|---|---|
| T01 | Migrar viz 3 a 11 do caderno para módulos | aberta | Hoje só inversão e fase têm módulo. |
| T02 | Adotar Mesa 3.x space classes para a rede intra-firma | aberta | Hoje uso direto de NetworkX. |
| T03 | Integração contínua com Zenodo | aberta | Workflow `.github/workflows/release.yml` pronto; falta vincular conta. |
| T04 | Adicionar DVC para versionamento de dados brutos | aberta | Pasta `data/raw/` reservada. |
| T05 | Cobertura de testes acima de 80% | aberta | Hoje só smoke tests. |

## Empíricas

| # | Decisão | Status | Observação |
|---|---|---|---|
| E01 | Triangular número de empregados em subsidiárias Big Tech BR | aberta | RAIS/CAGED via MTE. |
| E02 | Construir série temporal completa de TCCs do CADE | aberta | Saito 2021 cobre 2012-2019; estender até 2024. |
| E03 | Levantar série de represálias trabalhistas em casos relevantes | aberta | TST + CGU + MPT. |
| E04 | Verificar texto integral da Resolução 21/2018, Art. 12 | aberta | Conferir contra publicação no Diário Oficial. |

## Histórico de decisões fechadas

| # | Decisão | Resolução | Data |
|---|---|---|---|
| F01 | Linguagem: anglicismos? | Sem anglicismos quando houver termo português. Siglas mantidas. | 2026-05-26 |
| F02 | Licença | CC-BY-SA 4.0 | 2026-05-26 |
| F03 | Estrutura do pacote | src/ layout, Python 3.10+ | 2026-05-26 |
