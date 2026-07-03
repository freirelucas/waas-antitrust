# Checklist camera-ready — v0.2.0

Estado de prontidão do trabalho para circulação pública (working paper /
SSRN / seminário) e para submissão a periódico. Atualizado a cada rodada
de fechamento.

## Definição de camera-ready adotada

Duas metas distintas, com barras diferentes:

- **Circulação pública** (SSRN, seminário, blog jurídico, apreciação de
  público hostil informal): a barra é *coerência interna completa, sem
  buracos de redação, predições rigorosamente enquadradas*. **Atingida.**
- **Submissão a periódico com referee** (JCLE, Antitrust LJ, RIO): a barra
  adiciona *calibração confrontada com dado real e DOI*. **Bloqueada por
  dois itens que dependem de ação humana** (ver §"Depende de você").

## Pronto (verificado automaticamente)

- [x] **Paper completo** — dez seções escritas e coerentes; §3 e §4 (antes
  reportados como "primeira redação" no mirror do site) estão completos no
  LaTeX. Nenhuma seção incompleta.
- [x] **Zero citações órfãs** — as 26 chaves citadas em `paper/main.tex`
  têm entrada em `paper/refs.bib` (a entrada `hirschman1970exit`, que
  faltava, foi adicionada).
- [x] **Citações do paper todas verificáveis** — as 12 referências marcadas
  `[?]` (não-verificadas) estão apenas na bibliografia estendida do site
  (`docs/REFERENCES.md`), nenhuma é citada no paper.
- [x] **Predição N\* enquadrada com rigor** — `N* ≈ 1.679` é apresentada
  como predição *derivada* (não ajustada), com teste de falsificação
  especificado e teste de sanidade que ela sobrevive (73 investigações
  instauradas em 2024 = 4,3% de cobertura anual do universo latente, ordem
  de grandeza plausível). Ver §5.1 do paper (`\label{sec:nstar}`).
- [x] **Limitações declaradas** — Proposição 2 forte como conjectura aberta;
  Proposição 5 forte refutada empiricamente (sobrevive a fraca); calibração
  de capacidade internacional não fechada. Todas explícitas no paper e em
  [Limitações](docs/limitacoes.md).
- [x] **Reprodutibilidade** — 385 testes verdes, 94% de cobertura, piso 85%
  no CI, `mkdocs build --strict` limpo, `ruff`/`black` limpos.
- [x] **PDF sem bloqueadores de compilação** — o bloqueador que mantinha o
  `paper.yml` vermelho (a figura 03 lia `results/alpha_erosao_grade.parquet`,
  ignorado pelo git, ausente no checkout limpo do CI) está resolvido: o
  parquet foi versionado por exceção no `.gitignore` e as quatro figuras
  regeneram a partir dele num estado limpo (verificado localmente). A
  auditoria de integridade do paper não encontra bloqueadores de compilação
  (zero citação órfã, zero `[?]` no corpo, todas as `\includegraphics` no
  gerador, sem Unicode que quebre o Tectonic, `\ref`/`\label` íntegros).
  *Pendência de observação:* o run verde do `paper.yml` só ocorre em push a
  `main` — o gatilho não roda em ramo de feature e o `workflow_dispatch` está
  fora do alcance da integração desta sessão. Confirmar o verde e baixar o
  artifact `paper/main.pdf` no próximo push a `main`.
- [x] **Hierarquia LCMC > WaaS consistente** — auditoria de regressão
  concluída; "WaaS" aparece apenas como instrumento monetário opcional,
  nunca como o mecanismo central.
- [x] **Linguagem limpa** — códigos internos de backlog (R-XX, F6, v2.X)
  e nomes de variável Python removidos do corpo das páginas de leitura
  primária.
- [x] **Autoria e licença visíveis** — [Sobre](docs/sobre.md), `CITATION.cff`,
  `.zenodo.json` prontos; sem atribuição institucional indevida.

## Depende de você (ação humana — não automatizável)

Estes dois itens são o que separa "circula publicamente" de "submissível a
periódico com referee hostil". Nenhum pode ser feito por trabalho autônomo.

### 1. DOI Zenodo (≈ 10 minutos)

Sem DOI, revisor acadêmico não cita. Passo a passo em
[`DEPLOY.md`](DEPLOY.md) §"Arquivamento Zenodo". Resumo:

```bash
# 1. Ligar a integração (uma vez): https://zenodo.org/account/settings/github/
#    → ligar o repositório freirelucas/waas-antitrust
# 2. Criar a release:
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin v0.2.0
# 3. Publicar a release pela UI do GitHub (release notes prontas abaixo).
#    O DOI sai em minutos. Depois, colar o DOI em CITATION.cff, docs/sobre.md e README.md.
```

### 2. Cruzar N\* com dado real (≈ meia diária, requer dataset)

O teste de *sanidade* de N\* já está feito e sobrevive. O teste *definitivo*
requer o cadastro real de jurisdicionados — **dataset que não está no
repositório**. Receita completa em
[`docs/calibracao_pendente.md`](docs/calibracao_pendente.md) §1: filtrar
IBGE-RAIS por CNAE 62/63 + faturamento ≥ R\$ 75 mi (limiar Art. 88 da Lei
12.529), comparar com 1.679. Se cair no intervalo [~500, ~5.000], a predição
está confirmada; fora, a calibração de capacidade precisa revisão.

## Opcional (fortalece, mas não bloqueia)

- [ ] Trabalhar a doutrina brasileira (Forgioni, Salomão Filho, Ferraz Jr.)
  de *citação por nome* para *engajamento do argumento* — fortalece contra
  parecer jurídico adversário.
- [ ] Fechar as 12 citações `[?]` da bibliografia estendida do site.
- [ ] Formalizar a Proposição 2 forte (unicidade global sob heterogeneidade).

## Release notes v0.2.0 (prontas para colar na UI do GitHub)

```markdown
## v0.2.0 — Leniência Condicionada à Massa Crítica (LCMC)

Primeira versão consolidada do modelo e do paper de trabalho.

**Mecanismo.** Canal de depósito condicional (information escrow,
Ayres-Unkovic 2012; análogo Callisto) operado pelo CADE, com cinco
instrumentos opcionais de internalização acopláveis — recompensa via TCC
(WaaS) entre eles. Base normativa autônoma no Art. 4º II/III da Lei
12.529/2011 c/c Lei 9.784/99, dispensando lei nova.

**Modelo.** ABM em Mesa 3.x, três populações, 385 testes verdes, 94% de
cobertura, 27 cenários canônicos, 23 figuras reproduzíveis. Calibração
formal Nelder-Mead em (0,323; 0,481), erro relativo 6,65%, N* ≈ 1.679
firmas como predição falsificável (sobrevive a teste de sanidade).

**Extensões.** Janela de adesão pós-abertura com desconto progressivo;
sinergia entre autoridades internacionais (consolidação cross-jurisdicional
+ amplificação Schelling); recompensa coletiva como salvaguarda anti-erosão.

**Limitações declaradas.** Proposição 5 forte refutada empiricamente
(sobrevive fraca); Proposição 2 forte conjectura aberta; calibração de
capacidade internacional pendente.

Software sob CC BY-SA 4.0. Não citar como resultado final.
```
