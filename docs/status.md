# Status atual

<p class="deck">Panorama do estado do projeto em uma página: o que está fechado, o que está em andamento, o que permanece em aberto.</p>

<p class="lede">Esta página é o atalho para quem precisa entender, em poucos minutos, o estado de evidência e o ponto da agenda de pesquisa em que o projeto se encontra. Para detalhe técnico, ver <a href="DECISIONS/">decisões e backlog</a>; para histórico de mudanças, ver o <a href="https://github.com/freirelucas/waas-antitrust/blob/main/CHANGELOG.md">changelog</a>.</p>

## Numérico

| Métrica | Valor atual |
|---|---:|
| Testes verdes em `pytest -x -q` | **381** |
| Cobertura medida sobre `src/waas_antitrust/` | **94 %** |
| Piso de cobertura no CI | 85 % |
| Cenários canônicos em `cenarios.CATALOGO_CENARIOS` | **27** |
| Reporters expostos no `DataFrame` resultado | **38+** |
| Figuras reproduzíveis em `docs/img/` | **23** |
| Páginas no site (mkdocs `nav`) | **34** |
| `mkdocs build --strict` | limpa |
| `ruff check src/ tests/` | clean |
| `black --check src/ tests/` | clean |

## O mecanismo, em uma frase

A LCMC (**Leniência Condicionada à Massa Crítica**) é um canal de depósito condicional operado pelo CADE — *information escrow* no sentido de Ayres & Unkovic (*Mich. L. Rev.* 111: 145, 2012), com análogo prático em [Callisto](https://www.callisto.org) — em que denúncias individuais permanecem seladas até que uma fração mínima `q_min · n` de trabalhadores da mesma firma também tenha depositado. Quando o gatilho dispara, todas as denúncias se abrem simultaneamente, eliminando por construção o problema clássico de "ninguém quer ser o primeiro" (Olson 1965).

Sobre o canal podem ser acoplados, opcionalmente, cinco instrumentos de internalização: canal puro (sem recompensa), recompensa via TCC (*Whistleblower-as-a-Service*) sob re-caracterização do Art. 12 da Resolução CADE 21/2018, vesting acelerado de Hirschman (R07), crédito tributário (sub-regime Cᵩ) e leniência criminal individual (sub-regime Cₚ). O canal puro resolve a coordenação sozinho; os instrumentos amplificam a taxa de adesão.

## Componentes implementados

Lista dos marcos materializados no código, na documentação e na infraestrutura:

| Dimensão | Componente | Onde |
|---|---|---|
| Mecanismo | Janela de adesão pós-abertura com desconto progressivo | [Camada 5 do mecanismo](mecanismo.md) |
| Mecanismo | Adesão estocástica modulada por arquétipo | `AutoridadeAgent._decidir_adesao` |
| Mecanismo | Recompensa coletiva como salvaguarda anti-erosão (Marwell-Oliver 1993) | `WaaSParametros.recompensa_coletiva_pos_abertura` |
| Mecanismo | Sinergia entre autoridades internacionais (consolidação cross-jurisdicional + amplificação Schelling) | [`internacional.md`](internacional.md) |
| Mecanismo | Assimetria de tamanho entre jurisdições | `multiplicador_tamanho_por_firma` |
| Mecanismo | Risco de *forum shopping* por firmas | `forum_shopping_ativo` |
| Calibração | Faixas R29 contra gradiente Saito (2021) | `cascata_adesao_saito_calibrada` |
| Calibração | Cenário cruzado cascata × erosão Coleman | `cascata_adesao_com_erosao_coleman` |
| Calibração | Framework multi-target R03 (alvos 2 e 3) | `scripts/calibrar_formal_multitarget.py` |
| Institucional | Operacionalização do canal | [`operacional.md`](operacional.md) |
| Institucional | Doutrina brasileira citada | [`INSTITUTIONAL.md`](INSTITUTIONAL.md) |
| Institucional | Calibrações pendentes documentadas | [`calibracao_pendente.md`](calibracao_pendente.md) |
| Distribuição | Autoria, licença e como citar | [`sobre.md`](sobre.md) |
| Distribuição | Metadados Zenodo (release v0.2.0-draft) | `CITATION.cff`, `.zenodo.json` |
| Técnico | `WaaSModel.step()` decomposto em sub-fases | `model.py` `_fase_pX_*` |
| Técnico | Cobertura mínima de 85 % no CI + regressão visual via *pytest-mpl* | `.github/workflows/tests.yml` |
| Teoria | Esboço estendido da Proposição 2 sob heterogeneidade | [`ODD.md`](ODD.md) §1.4 |

## O que permanece em aberto

### Pesquisa substantiva

- **Calibração R03 alvos 2 e 3** — alvo único (TCCs/ano) fechado por Nelder-Mead 2D; sinais/tique e dano agregado seguem por identificabilidade fraca. Calibração formal multi-target pendente.
- **N\* × CNAE** — universo CADE implícito (1.679 firmas) ainda não cruzado com cadastro IBGE-RAIS + CNAE. Metodologia em [`calibracao_pendente.md`](calibracao_pendente.md) §1.
- **Capacidade institucional DOJ-ATR FY 2025 e DG-COMP 2024** — `taxa_capacidade` para as variantes EUA e UE ainda usa o *default* brasileiro. Metodologia em [`calibracao_pendente.md`](calibracao_pendente.md) §2.
- **Proposição 2 versão forte** — unicidade global do equilíbrio sob heterogeneidade segue conjectura aberta. Versão fraca (existência + unicidade local) tem esboço de prova em [`ODD.md`](ODD.md) §1.4.
- **Mussler-Macy multi-seed contra Prop. 5 forte** — cenário `recompensa_coletiva_anti_erosao` rodável; varredura 10 sementes × 8 valores de α ainda não executada. Receita em [`calibracao_pendente.md`](calibracao_pendente.md) §4.

### Operacional / institucional

- **DOI Zenodo formal** — integração manual Zenodo↔GitHub + tag de release v0.2.0 + atualização de `CITATION.cff` com o DOI emitido. Documentado em [`DEPLOY.md`](https://github.com/freirelucas/waas-antitrust/blob/main/DEPLOY.md).
- **Verbatim DOU dos dispositivos centrais em `normas/`** — parser parcial; expansão para Lei 13.608/2018 e Lei 13.964/2019 pendente.
- **Página `/operacional` valida pela CGAA / Tribunal CADE** — leitura técnica pela casa, sem implicar endosso institucional.

### Dívida técnica

- **Reescrita semântica do pacote** (`waas_antitrust` → `lcmc_antitrust` ou similar) — ruptura grande, ficará para v0.3.0.
- **Branch `gh-pages` legada** — pode ser apagada manualmente pela UI do GitHub.
- **Cadernos `.ipynb`** — headers internos ainda referem ao Colab e à hierarquia v2.

## Para onde olhar primeiro, por perfil de leitor

| Você é | Página primária | Por quê |
|---|---|---|
| Pesquisadora acadêmica | [`paper.md`](paper.md) → [`bem_publico.md`](bem_publico.md) | tese formal + moldura teórica Olson-Coleman |
| Advogada antitruste | [`INSTITUTIONAL.md`](INSTITUTIONAL.md) → [`operacional.md`](operacional.md) | base normativa autônoma + cláusulas contratuais afetadas |
| Conselheiro CADE | [`operacional.md`](operacional.md) → [`procedimento_cade.md`](procedimento_cade.md) | passagem do modelo ao ato administrativo |
| Compliance Big Tech | [`compliance_corporativo.md`](compliance_corporativo.md) → [`operacional.md`](operacional.md) | aritmética financeira + cláusulas defensivas |
| Economista | [`formulario.md`](formulario.md) → [`transparencia.md`](transparencia.md) → [`calibracao_pendente.md`](calibracao_pendente.md) | derivações + alvos de calibração + pendências |
| Jornalista | [`index.md`](index.md) → [`imprensa.md`](imprensa.md) | tese principal + kit de imprensa com leads e números |
| Curiosa/o | [`brincar.md`](brincar.md) | simulador in-browser, 13 sliders, ~300 ms por rodada |

## Como esta página é mantida

Esta página é **atualizada manualmente** após cada rodada substantiva do projeto. Quando os números na seção "Numérico" ficarem dessincronizados (testes < 381, cobertura < 94 %, cenários < 27 etc.), é sinal de que houve nova rodada e esta página precisa ser regenerada. Item #1.3 do [brainstorm de revisão](brainstorm_revisao.md) registra a alternativa de migrar para fonte única (`extra.yml` do MkDocs) — pendência de gravidade baixa.