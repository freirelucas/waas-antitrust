<span class="ato-chip">Ato 1 de 5 · O problema</span>

# Quando a infração é unilateral, quem denuncia?

<p class="sublinha-tese"><em>A resposta não está em incentivar a empresa. Está em reconhecer que a cooperação dos próprios funcionários é o bem coletivo que falta — e que pode ser internalizado por mais de um instrumento.</em></p>

## A leniência clássica acabou de bater num muro

Por quase trinta anos, programas de leniência foram a peça-mestre do enforcement antitruste. A lógica é simples: dois ou mais conspiradores fizeram um cartel; quem entregar primeiro escapa da multa. **O cartel se denuncia sozinho** — é a beleza do desenho.

Mas o abuso de mercado digital costuma ter **uma única empresa**. *Self-preferencing* do Google, *anti-steering* da Apple, exclusividade do iFood, *killer acquisition* da Meta. Não há segunda firma cúmplice para delatar; a conduta é executada pela própria firma dominante, pelos seus próprios times.

A informação existe — nos *commits* do engenheiro, nas *slides* da reunião comercial, no *deck* do *corp dev*. Mas ela não circula. Pelo Brasil de hoje, o trabalhador que fala arrisca emprego, carreira, tranquilidade, e ganha **nada de previsível** em troca.

<div class="pull-quote" markdown>
A leniência só funciona quando há cumplicidade entre firmas. Quando a infração é unilateral, é como esperar que o ladrão se entregue porque tem medo do espelho.
</div>

## A resposta deste projeto: LCMC

Em mercados digitais com **moat**, a cumplicidade existe — mas é **intra-firma**, entre engenharia, produto, jurídico, *corp dev*. A proposta deste projeto, em uma frase:

!!! tip "Leniência Condicionada à Massa Crítica (LCMC)"

    O atenuante regulatório (Art. 12 da Res. CADE 21/2018; analogia LAC Art. 7º VII-VIII) é concedido **se e somente se** a firma tiver recebido cooperação interna de ao menos uma fração `q_min` de seus funcionários, dentro de uma janela `Δt`.

A LCMC é **princípio regulatório**, não instrumento. Diz *o que* deve ser reconhecido como atenuante — cooperação interna de massa crítica — sem prescrever *como* essa cooperação é remunerada (se é).

## LCMC e WaaS são coisas diferentes

Esta distinção é a inovação editorial deste projeto, e ela costuma ser ignorada quando alguém confunde "LCMC" com "pagar denunciante". Não são equivalentes:

| Configuração | LCMC ativo? | Trabalhador recebe pagamento? | Como o regulador identifica |
|---|---|---|---|
| **LCMC sem instrumento monetário** | Sim | Não | Reconhecimento dogmático puro (analogia LAC). Funcionários cooperam por norma; firma ganha atenuante por ter substrato cooperativo. |
| **LCMC + WaaS (recompensa via TCC)** | Sim | Sim, pela firma | Funcionários cooperam por incentivo monetário + norma; firma paga e ganha atenuante. |
| **LCMC + Hirschman (vesting acelerado)** | Sim | Sim, via equity | Cláusula contratual padrão dispara vesting ao gatilho de ação coletiva. Custo crível de êxodo dissuade preventivamente. |
| **LCMC + crédito tributário** | Sim | Sim, pelo Estado | Estado financia o trabalhador por renúncia fiscal (Cᵩ; R22 stub). |
| **LCMC + leniência criminal individual** | Sim | Não (imunidade) | Estado oferece não-persecução penal ao partícipe cooperador (Cₚ; R23 stub). |
| **WaaS sem LCMC** | Não | Sim | Recompensa monetária pulverizada — cada denúncia individual. Sem gatilho coletivo. **Modelo histórico pré-LCMC; é o que o projeto questiona.** |

O **WaaS é um instrumento** — apenas um dos cinco que internalizam o capital social organizacional (Coleman 1990) que produz a cooperação. O Ato 2 detalha cada um. A página [Bem coletivo](bem_publico.md) é o anexo conceitual.

## A figura central do projeto

A figura abaixo é a **saída literal** de uma execução do modelo computacional. Não é estilizada — vem do `WaaSModel.executar()`, *seed* 11, regimes A/B/C lado a lado.

<figure markdown>
  ![Dissuasão endógena e bem-estar — 3 regimes ao longo de 40 trimestres](img/03_dissuasao_bem_estar.png){ .figura-empirica }
  <figcaption>
    <strong>(A)</strong> Violadoras ativas ao longo do tempo. Regime A (cinza) cresce e estabiliza alto;
    regimes B/C (verde/roxo) caem a zero em ~17 tiques. <strong>(B)</strong> Bem-estar social agregado.
    ΔW (B sobre A) = +1363%. <br><br>
    <em>Leitura sob LCMC:</em> a cascata de cooperação interna que faz B/C funcionarem dispara antes
    de qualquer firma decidir pagar. O instrumento WaaS está ativo nas curvas verdes e roxas, mas o
    fenômeno medido (queda de violadoras) é a propagação Schelling de detecção percebida, não o
    pagamento em si.
  </figcaption>
</figure>

## Reproduzir esta figura em três comandos

Toda a página acima é gerada por código aberto sob CC BY-SA 4.0. O leitor pode reproduzir a figura central em três passos:

```bash
# 1. Clonar e instalar
git clone https://github.com/freirelucas/waas-antitrust.git
cd waas-antitrust && pip install -e ".[dev]"

# 2. Rodar a varredura nos três regimes (60 segundos)
python scripts/gerar_figura_dissuasao.py

# 3. Saída em figuras/03_dissuasao_bem_estar.png
```

Para inspecionar o estado interno do modelo de forma direta:

```python
from waas_antitrust.model import WaaSModel, WaaSParametros

# Regime B padrão
m = WaaSModel(WaaSParametros(n_empresas=20, n_tiques=40, seed=11, regime="B"))
df = m.executar()

# Reporters macro (DataFrame com 40 linhas)
print(df[["n_sinais", "n_empresas_notif", "n_violadoras_ativas",
          "valor_dissuasao_difusa_acum", "capital_social_residual",
          "bem_estar"]].tail())

# Inspeção micro: arquétipos sorteados, papéis, posições na fila intra-firma
for t in m.trabalhadores_por_empresa[0][:5]:
    print(f"  {t.arquetipo:13s} · papel={t.papel:9s} · sinalizou={t.sinaliza_agora}")
```

A simulação produz 288 reporters em 40 colunas de pandas. Tudo é inspecionável; nada está escondido em variáveis privadas opacas. Ver [Modelagem multiagente](modelagem_multiagente.md) para a anatomia das três classes (`TrabalhadorAgent`, `EmpresaAgent`, `AutoridadeAgent`).

## Três regimes jurídicos, cinco instrumentos

A LCMC pode ser implementada em três regimes regulatórios distintos. Os instrumentos disponíveis dependem do regime — e cada instrumento exige reserva constitucional diferente (Art. 22 I, Art. 146 LC, Art. 5º XXXIX).

| Regime | Como implementado | Instrumentos disponíveis |
|---|---|---|
| **A** — status quo | Sem LCMC | Nenhum |
| **B** — Resolução CADE | Resolução complementar à 21/2018, **sem mudar a lei** | WaaS (recompensa via TCC sob Art. 12) |
| **C** — Lei ordinária federal | Extensão da Lei 13.608/2018 ao antitruste | WaaS + Hirschman (vesting acelerado) |
| **Cᵩ** — LC tributária | Lei complementar Art. 146 + LRF Art. 14 | + Crédito tributário ao denunciante (R22 stub) |
| **Cₚ** — Lei penal estrita | Reserva penal Art. 5º XXXIX | + Leniência criminal individual (R23 stub) |

O **Regime B** é a aposta política deste projeto: usar o que o CADE pode fazer sozinho. O **Regime C** é mais robusto juridicamente mas exige Congresso — e a [viabilidade política 2024-2027](viabilidade_regime_c.md) é incerta. Os sub-regimes Cᵩ e Cₚ são exploratórios.

## Por onde seguir

<div class="grid cards" markdown>

-   **Quero entender o mecanismo**

    Como a LCMC funciona, quando o WaaS é necessário, e quando massa crítica sozinha basta. Aritmética em reais (R$ 1 bi, R$ 15 mi de incremento) + três vetores de quebra modelados.

    [Ato 2: O mecanismo →](mecanismo.md)

-   **Quero ver os resultados**

    Saída literal do modelo em 20 firmas × 40 trimestres × 3 regimes. CI 95% bootstrap multi-seed. Direção da Proposição 3 não cruza zero.

    [Ato 3: O teste →](resultados.md)

-   **Sou jurista**

    Como cada instrumento cabe nas Leis 12.529/2011 + 13.608/2018 + Res. 21/2018. Decomposição do Regime C em Cₜ/Cᵩ/Cₚ. Lei 12.846/2013 (LAC) Art. 7º VII-VIII como precedente brasileiro.

    [Análise institucional →](INSTITUTIONAL.md)

-   **Sou sociólogo ou cientista político**

    LCMC sob lente Coleman 1990 (capital social com risco de erosão endógena) e Stigler-Carpenter-Moss (captura no processamento, não no gatilho). R21-R26 abertos.

    [Bem coletivo →](bem_publico.md) · [Viabilidade Regime C →](viabilidade_regime_c.md)

-   **Quero rodar o código**

    Instalação em 3 comandos, demo no Colab, 288 testes verdes, ruff/black/mkdocs-strict garantidos.

    [Como usar →](uso.md) · [Modelagem multiagente →](modelagem_multiagente.md)

-   **Quero contestar**

    Crítica x10 com 10 personas (incluindo sociólogo e cientista político na v2). Plano de melhorias categorizado. Backlog com 26 R-items abertos.

    [Crítica x10 v2 →](critica_x10_v2.md) · [Backlog →](DECISIONS.md)

</div>

<div class="ato-fim" markdown>
**Fim do Ato 1.** A tese está posta: a cooperação interna é o bem coletivo; LCMC é o princípio; existem cinco instrumentos para internalizá-la, e o WaaS é apenas um. O Ato 2 destrincha cada um com aritmética em reais e os vetores onde o argumento pode quebrar.

[Ato 2: O mecanismo →](mecanismo.md)
</div>

---

<small>
[![Licença: CC BY-SA 4.0](https://img.shields.io/badge/licen%C3%A7a-CC%20BY--SA%204.0-blue.svg)](https://github.com/freirelucas/waas-antitrust/blob/main/LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Mesa 3.x](https://img.shields.io/badge/mesa-3.x-green.svg)](https://mesa.readthedocs.io/)
[![288 testes](https://img.shields.io/badge/pytest-288%20passed-brightgreen)](https://github.com/freirelucas/waas-antitrust/actions)
[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/freirelucas/waas-antitrust/blob/main/notebooks/WaaS_demo.ipynb)

Este repositório acompanha um **artigo acadêmico em elaboração** —
*Critical Mass as a Quasi-Public Good in Antitrust Enforcement of Digital Markets*. Não citar como resultado final. Veja `CITATION.cff` para metadados estruturados (Zenodo via release futura).
</small>
