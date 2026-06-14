<span class="ato-chip">Ato 1 de 5 · O problema</span>

# Quando a infração é unilateral, quem denuncia?

<p class="sublinha-tese"><em>A resposta não está em incentivar a empresa nem em recompensar denúncia isolada. Está em dar ao CADE um <strong>canal de depósito condicional</strong> onde a denúncia individual só se abre quando há massa crítica de cooperadores — eliminando "ninguém quer ser o primeiro".</em></p>

## A leniência clássica acabou de bater num muro

Por quase trinta anos, programas de leniência foram a peça-mestre do enforcement antitruste. A lógica é simples: dois ou mais conspiradores fizeram um cartel; quem entregar primeiro escapa da multa. **O cartel se denuncia sozinho** — é a beleza do desenho.

Mas o abuso de mercado digital costuma ter **uma única empresa**. *Self-preferencing* do Google, *anti-steering* da Apple, exclusividade do iFood, *killer acquisition* da Meta. Não há segunda firma cúmplice para delatar; a conduta é executada pela própria firma dominante, pelos seus próprios times.

A informação existe — nos *commits* do engenheiro, nas *slides* da reunião comercial, no *deck* do *corp dev*. Mas ela não circula. Pelo Brasil de hoje, o trabalhador que fala arrisca emprego, carreira, tranquilidade, e ganha **nada de previsível** em troca.

<div class="pull-quote" markdown>
A leniência só funciona quando há cumplicidade entre firmas. Quando a infração é unilateral, é como esperar que o ladrão se entregue porque tem medo do espelho.
</div>

## A resposta deste projeto: LCMC como canal de depósito condicional

Em mercados digitais com **moat**, a cumplicidade existe — mas é **intra-firma**, entre engenharia, produto, jurídico, *corp dev*. O problema central não é "como punir a firma" nem "como pagar o denunciante"; é **como resolver a coordenação dos trabalhadores que veem a conduta mas não querem brigar a luta sozinhos**.

A proposta deste projeto, em uma frase:

!!! tip "LCMC — canal de depósito condicional"

    O **CADE opera um canal qualificado de recepção de denúncias** com cláusula de abertura condicional. O trabalhador entrega ao CADE sua denúncia com prova específica e diz: *"esta denúncia só é instaurada se houver ao menos `q_min · n` outros trabalhadores do mesmo setor/firma que também depositarem denúncias compatíveis dentro de uma janela `Δt`"*. As denúncias ficam em **escrow** — não notificam a firma, não viram processo, não vazam — até que o gatilho de massa crítica seja atingido. Quando o é, **todas se abrem simultaneamente**: ninguém foi o primeiro isoladamente.

A LCMC é **mecanismo de coordenação**, não de pagamento. Resolve diretamente o problema clássico de Olson (1965): em grupos pequenos, ninguém quer arcar sozinho com o risco de denunciar; cada um espera o outro. O canal de depósito condicional **elimina sub-iniciação por construção** — a denúncia individual nunca fica exposta enquanto a massa crítica não se forma.

O análogo prático mais próximo é a plataforma **[Callisto](https://www.callisto.org)** (callisto.org), que opera nos Estados Unidos para denúncias de assédio sexual em campus universitário: a identidade de uma vítima só é revelada ao mesmo agressor se duas ou mais denúncias coincidirem. Em direito, o conceito teórico é **information escrow** (Ayres & Unkovic, *Michigan Law Review* 111:145, 2012). Em estrutura de pagamento, o paralelo é o **Kickstarter all-or-nothing**: o pledge só cobra se a meta de apoiadores é atingida.

## O que vem depois da abertura — instrumentos

Quando o canal abre (massa crítica atingida), o procedimento administrativo se instaura: a firma é notificada com prova qualificada e coletiva; o CADE conduz a investigação; eventualmente assina TCC ou aplica multa. Esta parte usa o ferramental jurídico **já existente** — Art. 85 (TCC), Art. 86 (leniência), Art. 45 (dosimetria).

**Os instrumentos monetários abaixo são incrementos** ao canal — aumentam a probabilidade de adesão, não são o mecanismo central. Sem nenhum deles, o canal ainda funciona; com eles, opera com taxas de adesão maiores.

| Instrumento incremental | Quem paga | Para quem | Quando |
|---|---|---|---|
| **WaaS — recompensa via TCC** | Firma | Trabalhador | Ex-post: firma paga sob TCC; pagamento re-caracterizado como ressarcimento (Art. 12 Res. 21/2018) |
| **Hirschman — vesting acelerado** | Firma (via equity) | Trabalhador | Ex-ante: cláusula contratual dispara ao gatilho de ação coletiva |
| **Crédito tributário** | Estado (renúncia fiscal) | Trabalhador | Pós-instauração (R22 stub) |
| **Leniência criminal individual** | Estado (não-persecução) | Trabalhador-partícipe | Pós-instauração (R23 stub) |
| **Nenhum — só o canal** | — | — | O canal funciona pela coordenação per se |

A linha **"Nenhum — só o canal"** é a configuração mais conservadora juridicamente: o canal exige apenas regulamentação por Resolução CADE de procedimento de recepção (Art. 4º, II e III da Lei 12.529 c/c Lei 9.784/99). Não cria categoria sancionatória nova; estrutura *como o CADE recebe* informação. O risco de anulação judicial (F6) cai materialmente.

## A figura central do projeto

A figura abaixo é a **saída literal** de uma execução do modelo computacional. Não é estilizada — vem do `WaaSModel.executar()`, *seed* 11, regimes A/B/C lado a lado.

<figure markdown>
  ![Dissuasão endógena e bem-estar — 3 regimes ao longo de 40 trimestres](img/03_dissuasao_bem_estar.png){ .figura-empirica }
  <figcaption>
    <strong>(A)</strong> Violadoras ativas ao longo do tempo. Regime A (cinza) cresce e estabiliza alto;
    regimes B/C (verde/roxo) caem a zero em ~17 tiques. <strong>(B)</strong> Bem-estar social agregado.
    ΔW (B sobre A) = +1363%. <br><br>
    <em>Leitura sob LCMC corrigida:</em> a queda de violadoras em B/C é resultado de <strong>denúncias coletivas
    abrindo do escrow</strong>. Cada vez que o canal abre, o sinal Schelling se propaga (detecção percebida
    sobe em todas as firmas). O instrumento WaaS está ativo nas curvas verdes/roxas como incentivo
    incremental à adesão ao canal — não é a causa primeira da queda.
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

| Regime | Como implementado | Status normativo | Instrumentos disponíveis |
|---|---|---|---|
| **A** — status quo | Sem LCMC | — | Nenhum |
| **B** — Resolução CADE | Resolução complementar à 21/2018, **sem mudar a lei** | **de lege lata** (interpretação infralegal) | WaaS (recompensa via TCC sob Art. 12) |
| **C** — Lei ordinária federal | Extensão da Lei 13.608/2018 ao antitruste | **de lege ferenda** (lei nova) | WaaS + Hirschman (vesting acelerado) |
| **Cᵩ** — LC tributária | Lei complementar Art. 146 + LRF Art. 14 | **de lege ferenda** (LC + LRF) | + Crédito tributário (R22 stub) |
| **Cₚ** — Lei penal estrita | Reserva penal Art. 5º XXXIX | **de lege ferenda** (lei penal) | + Leniência criminal individual (R23 stub) |

O **Regime B** é a aposta política deste projeto: usar o que o CADE pode fazer sozinho com a Resolução 21/2018 vigente. O **Regime C** é mais robusto juridicamente mas exige Congresso — e a [viabilidade política 2024-2027](viabilidade_regime_c.md) é incerta. Os sub-regimes Cᵩ e Cₚ são exploratórios.

## Por onde seguir — entrada por papel profissional

<div class="grid cards" markdown>

-   **Jornalista**

    O lead em 30s, comparação BR×EUA×UE em 1 figura, autor e contato.

    [Kit de imprensa →](imprensa.md) · [Generalidade EUA e UE →](internacional.md)

-   **Advogado / advogada**

    Litígio: vetores jurídicos atacáveis (F6, reserva de lei, custo legal). Público: base autônoma Art. 4º Lei 12.529 + Lei 9.784/99. Compliance: implicações corporativas.

    [Análise institucional →](INSTITUTIONAL.md) · [Limitações §jurídica →](limitacoes.md)

-   **Economista**

    Equações em uma tela (IC-F\* nas 3 formas, bem-estar, calibração formal R03 com $(0{,}323; 0{,}481)$). Reprodução com seeds explícitas.

    [Formulário matemático →](formulario.md) · [Transparência →](transparencia.md)

-   **Autoridade**

    Decisor (CADE/PFE): tabela A/B/C com status normativo + base legal autônoma. Operacional (SG): fluxograma processual. Técnico (DEE): calibração com sensibilidade a N\*.

    [Análise institucional →](INSTITUTIONAL.md) · [Procedimento administrativo →](procedimento_cade.md)

-   **Big Tech (PM, engenharia, compliance)**

    Aritmética em R$ por receita da empresa, arquitetura do modelo, exposição esperada. Cenário canônico `eua_doj_atr_rewards_2025` para comparação direta com Dodd-Frank §922.

    [Ato 2 · O mecanismo →](mecanismo.md) · [Compliance corporativo →](compliance_corporativo.md)

-   **Academia / sociedade civil**

    LCMC sob lente Ostrom-Coleman-Olson. Falsificação numérica da Prop. 5 forte. 18 figuras com seeds reproduzíveis. Como contestar em código.

    [Bem coletivo →](bem_publico.md) · [Como contestar →](colaborar.md)

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
[![331 testes](https://img.shields.io/badge/pytest-331%20passed-brightgreen)](https://github.com/freirelucas/waas-antitrust/actions)
[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/freirelucas/waas-antitrust/blob/main/notebooks/WaaS_demo.ipynb)

Este repositório acompanha um **artigo acadêmico em elaboração** —
*Critical Mass as a Quasi-Public Good in Antitrust Enforcement of Digital Markets*. Não citar como resultado final. Veja `CITATION.cff` para metadados estruturados (Zenodo via release futura).
</small>
