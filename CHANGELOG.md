# Changelog

Todas as mudanças notáveis deste projeto são registradas aqui.

O formato segue, de forma adaptada, o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/);
as mensagens de commit seguem *Conventional Commits* em português. O versionamento
semântico será adotado a partir da primeira release (Zenodo).

## [Não lançado]

Trabalho desde a importação inicial do projeto (`563588c`, "Add files via upload"),
agrupado por tema. O hash de cada commit aparece entre parênteses.

### Estrutura e empacotamento
- Descompacta o projeto do tarball para a raiz do repositório e passa a versionar os
  arquivos (`src/`, `tests/`, `docs/`, `paper/`, …) em vez do `.tar.gz` (`04eb127`).

### Integridade científica e correção de método
- **Fase 1** — corrige defeitos que invalidavam as alegações: contaminação de seed na
  varredura de Sobol (estimador de Saltelli), separação de métricas de fluxo × estoque,
  remoção de código morto, substituição do teste tautológico da Proposição 1, RNG único
  (Mesa 3.5) e alinhamento das alegações infladas (`9c146b9`).
- Sincroniza o CLI `waas-sobol` com a replicação (`--n-replicas`) e adiciona ajuda a
  todos os argumentos (`50c9705`).
- Corrige `scripts/run_sobol_full.py`, quebrado após o conserto do Sobol
  (`n_seeds` → `n_replicas`; índices replicados); README com instruções de instalação
  (`d318613`).

### Modelo e mecanismo (pesquisa)
- **Fase 2** — bem-estar com significado, autoridade com acurácia sensível à qualidade
  da prova e capacidade da autoridade ancorada na vazão do CADE (`fdf9ba5`).
- **R04** — canal de falso reporte: não-violadoras podem ser reportadas, então os falsos
  positivos deixam de ser identicamente nulos (`be911b3`).
- **R01** — dissuasão endógena (à la Harrington–Chang): a firma viola enquanto sua
  atratividade `g_i` supera a detecção percebida; expõe `dano_acumulado` (`c2dc8b5`).
- **R05** — bem-estar redefinido como o negativo do custo social (dano + falsos
  positivos), creditando a prevenção em vez de premiar a detecção (`233797e`).
- **R02** — jogo global estilizado: limiar de switching único derivado em forma fechada,
  com convergência verificada quando τ → 0 (exploratório) (`2d0102c`).
- **R07** — Hirschman exit-with-equity: novo módulo `hirschman.py` (puro, testado) +
  integração em P0 (camada preventiva: firmas com cláusula contratual de vesting
  acelerado têm `g_i` efetivo menor) e P3 (IC-F* ampliada: `D + custo_exodo > W`,
  parametrizada por padrões YC — vesting 4y/1y cliff, substituição ~50% w_a, equity
  ~50% w_a, ~50% non-vested). Novos reporters `n_firmas_sob_ameaca_exodo` e
  `custo_exodo_acum`. Teste de integração confirma direcionalmente: dissuasão
  preventiva reduz o dano social com cláusulas ativas.
- **R08** — Heterogeneidade conduta × ator crítico: novo módulo `condutas.py` com
  catálogo de 7 condutas canônicas digitais (self_preferencing, tying, predatory
  pricing, killer acquisitions, dark patterns, acesso API/dados, MFN), cada uma
  com atores primários (eng/produto/design/growth/comercial/juridico/corpdev).
  `TrabalhadorAgent` ganha `papel`, `EmpresaAgent` ganha `conduta_potencial`, e a
  observabilidade em P0 passa a depender do par (papel, conduta). Teste
  end-to-end confirma direcionalmente que engenheiros observam mais
  self_preferencing que designers. Glossário ganha 10 termos.

### Documentação, site e paper
- **Fase 3** — registra o backlog de pesquisa (R01–R06) em `docs/DECISIONS.md`
  (`07991aa`).
- Site de documentação MkDocs Material e exportação de figuras em PDF (`1fe4f5d`).
- Paper: rascunho das seções estáveis (introdução e mecanismo), figuras reais e build
  LaTeX via Tectonic (`b171899`).
- README aponta para o site, o Colab e o paper (`8906892`).
- Site: figuras na página inicial e navegação reorganizada (`e40ed9b`).
- Adiciona e mantém este `CHANGELOG.md`, com uma entrada por commit, agrupada por tema.
- **Banho de loja de UX**: landing reescrita para o leigo (o problema → a ideia →
  resultado real → para quem), novas páginas **Resultados**, **Limitações** e
  **Glossário**, figura de resultado real do modelo (dissuasão + bem-estar) no site
  e no README, botão "editar esta página" (`edit_uri`), e README com "por quê/como"
  antes do quickstart.

### Ferramentas, Colab e testes
- Skill de execução `run-waas-antitrust` com driver de fumaça (`89bc38b`).
- Caderno instala as dependências automaticamente no Google Colab (`0f05e24`).
- Cobertura de testes ≥ 80% — análise de Sobol e stubs de visualização (`666fa13`).
- Caderno-demo limpo, baseado no pacote, como companheiro canônico para Colab/CI
  (`b4f91ce`).
- Refresh da skill `run-waas-antitrust`: driver ganha a camada `jogo_global` (R02);
  `SKILL.md` atualizado (4 camadas, demo, métricas de dano/bem-estar) e corrige a
  gotcha obsoleta "FP≡0" (o R04 introduziu falsos positivos).
