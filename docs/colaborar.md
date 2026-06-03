<span class="ato-chip">Ato 5 de 5 · A continuação</span>

# Como contribuir, discordar, ou simplesmente conversar

A versão honesta deste projeto é: **um artigo em elaboração, com cinco pendências normativas explícitas, um vão de calibração que precisa de quem entenda do CADE pós-2020, e três proposições teóricas que pediriam mais matemática**. Nada disso vai se resolver no monólogo do autor. Esta página enumera as três formas concretas pelas quais alguém pode entrar no jogo.

## Reproduzir, verificar, derrubar

O caminho mais útil — e mais barato — é **rodar o modelo, contestar a calibração e tentar quebrar a conclusão**. Tudo está aberto sob CC BY-SA 4.0.

```bash
# 60 segundos no Colab, com tudo instalado
# https://colab.research.google.com/github/freirelucas/waas-antitrust/
#   blob/main/notebooks/WaaS_demo.ipynb

# Localmente, para mexer no código
git clone https://github.com/freirelucas/waas-antitrust.git
cd waas-antitrust
pip install -e ".[dev]"
pytest                                            # 88 testes
python scripts/gerar_figura_dissuasao.py          # figura 03 do site
python scripts/run_sobol_full.py --n-base 1024    # varredura paramétrica
```

Os parâmetros adversariais — `D_disc_base_tcc`, `p_anulacao_tcc`, `custo_legal_uw` — estão expostos em `WaaSParametros`. Calibrar com seus números preferidos é uma chamada de função. Se a direção da Proposição 3 quebrar sob calibração que você considera realista, **abra uma issue** — isto é exatamente o que o projeto precisa.

## Contribuir com calibração ou texto

Há três bancos de dados externos contra os quais o modelo precisa ser ajustado, e o autor não conseguiu acesso a todos sozinho:

- **Mediana de desconto em TCCs CADE pós-Saito (2021).** Cobrir o intervalo 2020–2025 fecharia $D_{\text{base}}$ — a peça central da IC-F\* corrigida.
- **Número de funcionários em subsidiárias brasileiras de big tech.** Permitiria reescalonar a capacidade da autoridade (`taxa_capacidade`) ao universo real (R06).
- **Custos legais médios em ações trabalhistas e em representações ao CADE.** Calibraria `custo_legal_uw` contra a faixa empírica brasileira.

Se você tem esses dados ou trabalha com quem tem, abra uma issue ou um PR contra o módulo `src/waas_antitrust/calibracao/`. Toda calibração externa precisa ter fonte primária verificável no docstring — não há margem para citação não-verificável.

Há também trabalho jurídico-dogmático em aberto, particularmente a **D06** (análise dogmática "vítima-empregado" no Art. 12) e a calibração de risco de anulação (F6). Quem tenha formação em direito antitruste brasileiro encontra material para escrever — e a co-autoria é negociável.

## Discordar do desenho

Algumas decisões deste projeto são deliberadamente discutíveis. As cinco principais estão em [DECISIONS.md](DECISIONS.md) como **R09–R13**. Cada uma alteraria material e Proposições; cada uma exige conversa explícita, não execução por piloto automático.

- **R09 (Eco A):** endogeneizar $g_i(t) = \pi R / (p S)$. Eu não fiz porque mudaria a Prop. 3.
- **R10 (Eco A):** IC-F\* completa $W + p_{\text{pago}}(S-D) < p_{\text{não pago}}S$. Não fiz porque mudaria a Prop. 1.
- **R11 (Eco A):** Hirschman como elevação de $W_{\text{esperado}}$, não subtração de $g_i$. Equivalência analítica é alegada mas não testada.
- **R12 (Mat B):** substituir o arquétipo racional pelo limiar de switching $x^*$ do jogo global. Integraria a Prop. 2 ao ABM.
- **R13 (PM, Designer, Eco B, Adv A):** distribuição Pareto/lognormal de fatia de mercado; sankey real do mecanismo; três condutas-piloto com fixtures; `p_anulacao_tcc` como variável de varredura Sobol.

Se você acha que uma dessas decisões é errada — ou se você tem um argumento que invalida o desenho como um todo — abra uma issue **com o argumento**, não só com a discordância. Texto é mais barato de discutir do que código.

## A história institucional do projeto

A hipótese original deste projeto surgiu numa conversa de 06 de setembro de 2022 com **Felipe Roquete**, Superintendente-Adjunto do CADE e doutorando em Direito da Regulação na FGV. A possibilidade de co-autoria está rastreada em **D04**; o repositório é mantido independentemente, mas a origem intelectual é explícita.

O autor — eu — trabalha no IPEA (DIEST/COGIT). Este repositório **não vincula o IPEA**. As posições aqui defendidas são minhas, e a intenção é submeter o artigo a revista internacional indexada (*Journal of Competition Law & Economics* ou similar) com aprovação prévia da chefia institucional.

## Citação, licença, contato

Veja [`CITATION.cff`](https://github.com/freirelucas/waas-antitrust/blob/main/CITATION.cff) para metadados estruturados (Zenodo via release futura). Código e documentação sob **Creative Commons CC BY-SA 4.0**. Issues e PRs no [repositório no GitHub](https://github.com/freirelucas/waas-antitrust). Para contato direto sobre co-autoria ou discussão acadêmica, o e-mail está no `CITATION.cff`.

<div class="ato-fim" markdown>
**Fim dos cinco atos.** Se você chegou até aqui, o sistema funcionou — para o que ele era: um convite a entrar num argumento que precisa ser apertado por mãos diferentes da do autor.

[Voltar ao Ato 1 →](index.md)
</div>
