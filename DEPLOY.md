# Arquitetura de deploy do site

Este projeto serve documentação MkDocs Material em
<https://freirelucas.github.io/waas-antitrust/>. O processo é
**inteiramente automatizado via GitHub Actions** e exige uma única
configuração manual no painel de Settings do repositório, descrita
abaixo.

## Fluxo

```
push em main (paths: docs/**, mkdocs.yml, src/**, workflow)
    │
    ▼
.github/workflows/docs.yml
    │
    ├─ build:
    │    1. checkout
    │    2. setup-python 3.12
    │    3. pip install -e ".[docs]"
    │    4. mkdocs build --strict --site-dir _site
    │    5. touch _site/.nojekyll          (anti-Jekyll)
    │    6. actions/configure-pages@v5
    │    7. actions/upload-pages-artifact@v3 (path: _site)
    │
    ▼
deploy:
    actions/deploy-pages@v4
    └─→ ambiente github-pages, output page_url
```

## Configuração única no GitHub (uma vez por repositório)

A primeira vez (e somente a primeira) é preciso configurar a *source*
do GitHub Pages:

1. Abra **Settings → Pages** no GitHub
   (`https://github.com/freirelucas/waas-antitrust/settings/pages`).
2. Em **Source**, selecione **`GitHub Actions`** (NÃO "Deploy from a
   branch").
3. Salve. O próximo push em `main` vai disparar o workflow e o site
   aparece em poucos minutos no `Environments → github-pages` da
   página principal do repo.

> **Por que isso é necessário.** O setting anterior do projeto era
> `Deploy from a branch · main · /docs`, que faz o GitHub processar o
> conteúdo de `docs/` com o **Jekyll padrão**. Como o tema MkDocs
> Material exige render Jinja2 + assets que o Jekyll não conhece, o
> resultado era a página em estilo "raw markdown". A mudança para
> `GitHub Actions` desliga o Jekyll automático e serve diretamente
> o artefato `_site/` produzido pelo workflow.

## Garantias do desenho atual

- **Sem branch `gh-pages`.** O modelo Actions dispensa o branch
  histórico `gh-pages`; o artefato é servido diretamente. Se houver
  uma branch `gh-pages` legada (criada por execuções anteriores de
  `mkdocs gh-deploy --force`), ela é ignorada e pode ser apagada com
  `git push origin --delete gh-pages` quando confortável.
- **`.nojekyll` em dois lugares.** O arquivo está em `docs/.nojekyll`
  (versionado) e é também criado em `_site/.nojekyll` durante o build
  (step "Garantir que Jekyll não interfira"). Redundância intencional
  caso o setting de Pages mude de novo no futuro.
- **Build em modo estrito.** `mkdocs build --strict` falha em links
  quebrados ou anchors ausentes — o deploy só sai se `mkdocs --strict`
  passa.
- **Concorrência controlada.** `concurrency: pages` cancela o deploy
  anterior se um novo push chegar antes do anterior terminar, evitando
  corrida.

## Verificação rápida

Após push em `main`, verificar:

1. **Status do workflow:** `Actions → docs` no GitHub.
2. **Ambiente github-pages:** painel `Environments` do repo mostra o
   último deploy bem-sucedido com link clicável.
3. **Conteúdo do site:** abrir `https://freirelucas.github.io/waas-antitrust/`
   — o título do navegador deve ser `LCMC · Leniência Condicionada à
   Massa Crítica` (do `site_name` em `mkdocs.yml`), não `waas-antitrust`
   (o nome do repo). Se mostrar `waas-antitrust`, o setting de Pages
   continua em modo Jekyll.

## Histórico

- **Anterior (até jun/2026):** `mkdocs gh-deploy --force` publicando
  em branch `gh-pages` + Settings provavelmente apontando para
  `main/docs` (Jekyll). Funcionava em algumas situações mas tinha
  duas fontes da verdade incompatíveis.
- **Atual (jun/2026):** Actions Pages modelo `actions/deploy-pages@v4`.
  Uma única fonte da verdade: o artefato do workflow é o que vai ao
  ar. Resolve definitivamente o ciclo "deploy ok mas site mostra
  Jekyll bruto".
