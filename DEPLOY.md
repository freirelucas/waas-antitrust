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

## Arquivamento Zenodo (DOI)

A integração Zenodo é independente do GitHub Pages e usa o arquivo
`.zenodo.json` na raiz para preencher os metadados de cada release.

### Configuração manual única

1. Abra <https://zenodo.org/account/settings/github/> autenticado com a
   mesma conta GitHub que mantém o repositório.
2. Em *Repositories*, localize `freirelucas/waas-antitrust` e ligue a
   chave ON.
3. Salve.

A partir disso, toda *Release* publicada na página de GitHub →
*Releases* dispara automaticamente um arquivamento no Zenodo com DOI
permanente, derivado dos campos em `.zenodo.json` (título, criadores,
licença, *keywords*, comunidade, etc.).

### Criar release v0.2.0

Quando o conjunto v0.2.0 estiver pronto para arquivamento:

```bash
git tag -a v0.2.0 -m "Release v0.2.0 — R29 + R30 + atenuação editorial + Pages via Actions"
git push origin v0.2.0
```

Depois, ir em <https://github.com/freirelucas/waas-antitrust/releases/new>,
selecionar a tag `v0.2.0`, preencher título e *release notes* (extrair
do `CHANGELOG.md` rodada "R30 + banho de loja" e "R29 + simulador").
Publicar. O Zenodo cria o registro e devolve o DOI em poucos minutos.

Após o DOI sair, atualizar:
- `CITATION.cff` (campo `doi:`)
- `docs/sobre.md` (seção "DOI")
- `README.md` (badge DOI no hero)

## Regressão visual (pytest-mpl)

Testes marcados com `@pytest.mark.mpl_image_compare` em `tests/test_viz.py`
comparam o PNG produzido pela função `gerar_figura()` contra um baseline
versionado em `tests/baseline_images/`.

### Gerar/atualizar baselines (procedimento manual, fora do CI)

```bash
pytest tests/test_viz.py --mpl-generate-path=tests/baseline_images
git add tests/baseline_images/
git commit -m "test(viz): atualiza baselines de regressão visual"
```

### Rodar a comparação no CI

A comparação não roda no workflow padrão (`tests.yml`). Para ativar,
adicionar uma matriz separada com a flag `--mpl`:

```bash
pytest tests/test_viz.py --mpl
```

Sem a flag, os testes marcados apenas executam como smoke test (sem
comparar bytes).

### Cobertura mínima

O workflow `tests.yml` exige `--cov-fail-under=85` em `pytest-cov`.
A cobertura atual da `src/waas_antitrust/` é de aproximadamente 94 %
(medida em jun/2026); o piso de 85 % deixa folga de 9 pontos para
evolução sem quebrar o CI.
