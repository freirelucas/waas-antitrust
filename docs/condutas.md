# Catálogo das 28 condutas digitais unilaterais

<p class="deck">Catálogo declarativo das 28 condutas digitais unilaterais consideradas no modelo, com descrição substantiva, papéis funcionais primários e adjacentes responsáveis pela execução, severidade-base entre 0,5 e 0,9 e pelo menos um caso de referência verificado em fonte primária por entrada. A base da heterogeneidade conduta × papel × observabilidade que sustenta a tese de massa crítica intra-firma viável (nenhuma conduta catalogada exige mais do que dois ou três papéis primários para configurar).</p>

<p class="byline"><em>Anexo técnico</em> · catálogo de condutas · rascunho v0.2.0</p>

## Estrutura

Cada conduta é uma `Conduta` (dataclass frozen) com:

```python
nome: str                            # snake_case canônico
descricao: str                       # 1 linha substantiva
atores_primarios: tuple[str, ...]    # papéis que EXECUTAM (peso 1.0 na obs.)
atores_adjacentes: tuple[str, ...]   # papéis que OBSERVAM (peso 0.5)
severidade_base: float               # ∈ [0, 1], modula multa esperada
casos_referencia: tuple[str, ...]    # ≥ 1 fonte primária (verbatim)
```

Os papéis distais (não listados) têm observabilidade 0,1 — gradiente 3 níveis Near & Miceli (1985). O dict `N_ATORES_PRIMARIOS_NECESSARIOS` calibra `q_min_cooperacao_interna` por conduta — **nenhuma conduta exige mais que 2-3 papéis primários** no catálogo atual.

## Catálogo completo (28 condutas)

| Conduta | Descrição | Severidade · q_min | Papéis primários | Casos de referência |
|---|---|---|---|---|
| `self_preferencing` | Autopreferenciamento de produto próprio em marketplace/busca. | sev. 0,7 · q_min 2 | eng, produto | Google Shopping (UE 2017) · Amazon Buy Box (UE 2022) |
| `tying_bundling` | Vinculação de produtos para forçar compra conjunta. | sev. 0,6 · q_min 2 | produto, comercial | Microsoft Windows-Media Player · Apple App Store |
| `predatory_pricing` | Preços abaixo do custo para excluir concorrentes em adjacência. | sev. 0,8 · q_min 2 | growth, eng | Uber 2014-2019 · iFood vs concorrentes |
| `killer_acquisitions` | Aquisição de concorrente nascente para neutralizar competição. | sev. 0,9 · q_min 2 | corpdev, juridico | Meta-Instagram (2012) · Meta-WhatsApp (2014) |
| `dark_patterns` | Design de interface que dificulta saída ou induz consentimento. | sev. 0,5 · q_min 2 | design, produto | Amazon Prime cancelamento (FTC 2023) · Facebook ad opt-out |
| `acesso_api_dados` | Discriminação no acesso a API ou dados prejudicando concorrentes. | sev. 0,7 · q_min 2 | eng, produto | Twitter API 2023 · Google Maps embargos |
| `mfn_paridade` | Cláusula MFN obrigando vendedor a não cobrar menos em outros canais. | sev. 0,6 · q_min 2 | comercial, juridico | Booking.com (UE 2015) · Amazon Marketplace |
| `exclusividade_retaliacao_marketplace` | Exclusividade contratual ou retaliação contra sellers em marketplace de duas pontas. | sev. 0,8 · q_min 2 | comercial, operacoes | iFood TCC 2023 · Mercado Livre vs sellers (indícios 2024-25) |
| `anti_steering_iap` | Bloqueio de informação ou redirecionamento de pagamento fora do in-app purchase. | sev. 0,7 · q_min 2 | produto, eng | Apple Brasil — CADE dez/2025 · Epic Games v. Apple (EUA 2021) |
| `ranking_demotion_rivais` | Degradação algorítmica do ranking de rivais em busca ou feed. | sev. 0,7 · q_min 2 | eng, produto | Google Shopping CJUE 10/09/2024 · FTC v. Amazon §VI (EUA 2023) |
| `tying_ia_generativa` | Embutir assistente de IA do operador sem opção neutra de escolha. | sev. 0,7 · q_min 2 | produto, eng | Microsoft Copilot/Bing (EC RFI 2024) [?] · Google Gemini default Android [?] |
| `subsidio_cruzado_ecossistema` | Subsídio de produto em mercado adjacente financiado pelo monopólio principal. | sev. 0,7 · q_min 2 | financeiro, growth | Khan 2017 (Amazon) · CADE Caderno Plataformas Digitais 2023 |
| `reverse_killer_shelving` | Adquirir e engavetar produto que competiria com linha existente. | sev. 0,8 · q_min 2 | corpdev, produto | Cunningham-Ederer-Ma JPE 2021 · Crémer-Montjoye-Schweitzer EC 2019 [?] |
| `uso_dados_concorrentes` | Plataforma usa dados de sellers para informar produto próprio. | sev. 0,8 · q_min 2 | eng, produto | Amazon Marketplace (UE 2022) · FTC v. Amazon §V (EUA 2023) |
| `mfn_inverso_algorithmic` | Algoritmo que detecta paridade alheia e penaliza seller via remoção de Buy Box. | sev. 0,7 · q_min 2 | eng, comercial | FTC v. Amazon §IV — Project Nessie (EUA 2023) [?] |
| `sideloading_block` | Bloquear instalação direta de apps fora da loja oficial. | sev. 0,7 · q_min 2 | produto, eng | Apple Brasil TCC CADE 2025 · DMA UE Art. 6(4) (2022) |
| `multihoming_friction` | Atrito técnico ou UX para usar serviços rivais em paralelo. | sev. 0,6 · q_min 2 | design, eng | DMA UE Art. 6(7) interoperabilidade · CMA SMS Mobile Roadmap (UK 2025) [?] |
| `degradacao_api_seletiva` | Degradar SLA de API só para integradores que competem em adjacência. | sev. 0,7 · q_min 2 | eng, operacoes | Cornell JLPP — Pulling Up the Drawbridge (2025) [?] · FTC v. Meta |
| `lock_in_credenciais` | Forçar login do ecossistema como pré-requisito para funcionalidades básicas. | sev. 0,6 · q_min 2 | produto, eng | DMA UE Art. 5(7) · Crémer-Montjoye-Schweitzer EC 2019 (capítulo SSO) [?] |
| `switching_costs_design` | Exportação proprietária, fricção de migração, ausência de portabilidade real. | sev. 0,6 · q_min 2 | eng, produto | DMA UE Art. 6(9) portabilidade · GDPR Art. 20 |
| `treino_ia_com_dados_concorrentes` | Plataforma treina IA com dados de business users rivais sem autorização. | sev. 0,8 · q_min 2 | eng, produto | Sem condenação antitruste consolidada [?] · NYT v. OpenAI (direito autoral) |
| `discriminacao_algoritmica_preco` | Preço personalizado baseado em reputação ou vulnerabilidade do usuário. | sev. 0,6 · q_min 2 | eng, produto | RealPage litigation (EUA em curso) · CMA Ticketmaster (UK 2024) |
| `surge_predatorio` | Surge pricing em cativação (chuva, fila) sem alternativa real ao consumidor. | sev. 0,5 · q_min 2 | eng, operacoes | Sem condenação formal consolidada [?] · Literatura de economia digital |
| `manipulacao_relevancia_moderacao` | Shadow-banning ou deboost seletivo via moderação algorítmica. | sev. 0,6 · q_min 2 | eng, produto | Sem condenação antitruste consolidada — preocupação regulatória [?] |
| `exclusao_app_store_seletiva` | Remoção ou atraso de aprovação de app concorrente. | sev. 0,7 · q_min 2 | produto, operacoes | Epic v. Apple Fortnite ban 2020 · Apple Brasil TCC CADE 2025 |
| `default_distribution_exclusivo` | Pagamento por default de busca ou IA excluindo concorrentes do canal principal. | sev. 0,8 · q_min 2 | comercial, corpdev | US v. Google Search — Mehta 05/08/2024 · CMA SMS Google (UK 10/10/2025) |
| `aquisicao_assets_chave` | Aquisição de patentes, talento ou dataset estratégico para travar rivais. | sev. 0,7 · q_min 2 | corpdev, juridico | Microsoft-OpenAI investment (EC RFI 2024) · Google-Waze 2013 [?] |
| `auto_deteccao_atrasada` | Compliance interna detecta a conduta mas atrasa correção até intimação externa. | sev. 0,7 · q_min 2 | juridico, operacoes | FTC v. Amazon — Project Nessie liga/desliga sob escrutínio |

**Marcação `[?]`** indica caso emergente sem condenação antitruste consolidada (vide [transparência](transparencia.md) §pendências).

## A leitura do `q_min` por conduta

O dict `N_ATORES_PRIMARIOS_NECESSARIOS` em `condutas.py` calibra o gatilho de massa crítica por tipo de conduta. **A descoberta substantiva**: nenhuma conduta no catálogo exige mais que **2-3 papéis primários** — confirma o argumento do moat ("informação reside em pequeno núcleo técnico") e operacionaliza o `q_min_cooperacao_interna` por tipo de violação, em vez de uniformizar em 10%.

## Pendências de calibração

- **E05 (em aberto)**: a distribuição de papéis por firma é estimada por preset (`BIGTECH_MADURA`, `MARKETPLACE_BR`). Calibração rigorosa exigiria survey de organogramas ou aproximação via LinkedIn público — pendência empírica rastreada em `DECISIONS.md`.
- **9 casos `[?]`**: emergentes sem condenação antitruste consolidada — auditoria explícita em `transparencia.md` § pendências.
- **Severidade-base**: ordens de grandeza, não calibração formal. Connor-Lande (overcharge mediano 15-25% em cartel) é proxy; uso de severidade unilateral exige pesquisa empírica adicional.

## Como rodar

```python
from waas_antitrust.condutas import (
    CATALOGO,
    N_ATORES_PRIMARIOS_NECESSARIOS,
    BIGTECH_MADURA,
    MARKETPLACE_BR,
)

# Listar todas as condutas com seu q_min
for c in CATALOGO:
    n_atores = N_ATORES_PRIMARIOS_NECESSARIOS[c.nome]
    print(f"{c.nome}: severidade={c.severidade_base:.2f}, "
          f"q_min={n_atores} primários, papéis={c.atores_primarios}")

# Preset de papéis BIGTECH_MADURA vs MARKETPLACE_BR
print(f"BIGTECH: {BIGTECH_MADURA}")        # 30% eng, 5% operacoes
print(f"MARKETPLACE: {MARKETPLACE_BR}")     # 18% eng, 25% operacoes
```

Para a tela visual da variedade ashbiana (BIGTECH × MARKETPLACE), ver figura 17 em [`modelagem_multiagente.md`](modelagem_multiagente.md#heuristica-de-observacao-r08-conduta-papel).
