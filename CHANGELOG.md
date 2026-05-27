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

### Documentação, site e paper
- **Fase 3** — registra o backlog de pesquisa (R01–R06) em `docs/DECISIONS.md`
  (`07991aa`).
- Site de documentação MkDocs Material e exportação de figuras em PDF (`1fe4f5d`).
- Paper: rascunho das seções estáveis (introdução e mecanismo), figuras reais e build
  LaTeX via Tectonic (`b171899`).
- README aponta para o site, o Colab e o paper (`8906892`).
- Site: figuras na página inicial e navegação reorganizada (`e40ed9b`).
- Adiciona e mantém este `CHANGELOG.md`, com uma entrada por commit, agrupada por tema.

### Ferramentas, Colab e testes
- Skill de execução `run-waas-antitrust` com driver de fumaça (`89bc38b`).
- Caderno instala as dependências automaticamente no Google Colab (`0f05e24`).
- Cobertura de testes ≥ 80% — análise de Sobol e stubs de visualização (`666fa13`).
- Caderno-demo limpo, baseado no pacote, como companheiro canônico para Colab/CI
  (`b4f91ce`).
