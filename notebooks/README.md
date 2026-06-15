# Cadernos

Esta pasta contém cadernos Jupyter mantidos como artefatos do projeto.
A partir de jun/2026, o caminho recomendado para uma primeira aproximação
do modelo é o [**simulador in-browser**](https://freirelucas.github.io/waas-antitrust/brincar/) — não estes cadernos.

## Status atual de cada caderno

- `WaaS_brincar.ipynb` — versão Jupyter do simulador (12 sliders + painel
  2×2). Mantido para quem prefere rodar localmente em Python; o simulador
  in-browser é mais rápido e cobre a regra R29 (janela de adesão).
- `WaaS_caderno_v2.ipynb` — caderno didático do reframe v2 ("massa
  crítica como bem quase-público"). Validado em CI via `nbval`.
- `WaaS_demo.ipynb` — caderno mínimo de demonstração (instala, roda
  cenário canônico, plota figura 03). Útil para validar instalação local.

## Hierarquia LCMC × WaaS

Cabeçalhos antigos destes cadernos podem mencionar o WaaS como
mecanismo central — esta era a leitura **v1/v2**. A partir da correção
v3 (jun/2026), a LCMC (canal de depósito condicional) é o mecanismo
central; WaaS é um dos cinco instrumentos opcionais de internalização.
Para o entendimento atual, ver:

- [`docs/index.md`](../docs/index.md) — visão geral
- [`docs/mecanismo.md`](../docs/mecanismo.md) — formalização em 5 camadas
- [`docs/aprendizados_v3.md`](../docs/aprendizados_v3.md) — registro
  da correção radical
