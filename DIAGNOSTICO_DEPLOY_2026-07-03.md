# Diagnóstico de deploy — 03/07/2026

> **Para quem lê:** nota de diagnóstico deixada por uma sessão que foi orientada
> a **não** aplicar a correção (há outro agente/sessão tratando disso em
> paralelo). Registro apenas o que apurei ao vivo, para não colidir com esse
> trabalho. Arquivo na raiz — o MkDocs não o constrói.

## Gatilho

Dois prints sugeriam site quebrado:

1. **"404 - Not found"** (cabeçalho escuro "LCMC · Leniência Co…").
2. **Home funcionando, mas com cabeçalho verde** e jargão "IC-F\* · calibração
   R03", "Tabela A/B/C", "DOJ-ATR" — visual anterior à migração de paleta.

## O que verifiquei ao vivo

- **O site está no ar.** *Fetch* de `https://freirelucas.github.io/waas-antitrust/`
  retorna conteúdo real, "Rascunho v0.2.0", **sem 404**.

- **Print 1 (404):** a URL é a **raiz nua** `freirelucas.github.io/` (sem
  `/waas-antitrust/`). Sendo *project page*, a raiz do usuário cai no 404
  temático — **comportamento esperado**, não é o site quebrado. Mitigação
  possível: *redirect* da raiz → `/waas-antitrust/`.

- **Print 2 (verde + "IC-F\* / calibração R03"):** é aba em **cache** anterior à
  migração de paleta (o autor mantém ~80 abas abertas). Evidência: o *fetch* ao
  vivo **não** encontra mais `IC-F*`, `calibração R03` nem `DOJ-ATR`; encontra
  ainda `Tabela A/B/C`. Ou seja, o *live* é mais **novo** que o Print 2. E o
  `mkdocs.yml` no repositório já está `primary: black` / `accent: indigo`
  (commit `0592621`, presente na `main`).

## Fio aberto (o passo definitivo, para o agente paralelo)

- **Não confirmei** se os *runs* do workflow **`docs.yml`** para os commits
  `0592621` (paleta preta) e `b07f67a` (índice) **concluíram verdes**. Se algum
  falhou, o *live* pode estar **parcialmente defasado** (explicaria qualquer
  resíduo verde real, não-cache). **Conferir a conclusão desses *runs* pela aba
  Actions é o próximo passo.** Se defasado: re-disparar `docs.yml`
  (`workflow_dispatch`) ou repushar tocando `docs/`/`mkdocs.yml`.
- Avaliar o *redirect* da raiz nua para eliminar o 404 do Print 1.

## Correções de documentação pendentes (anotadas, não aplicadas aqui)

- `CHECKLIST_CAMERA_READY.md` afirma **"PDF compilável — paper.yml compila"** —
  **falso**: `paper.yml` está **vermelho** (a figura 03 lê um parquet ausente no
  CI; ver `HANDOFF_SESSAO.md` §1, que já registra isso corretamente).
- A ideia de "deploy íntegro" que afirmei antes deve virar **"carrega; sucesso
  do último *run* `docs.yml` a confirmar"** — eu havia dado o site como íntegro
  **sem** ter verificado os *runs* de deploy.

## Estado do repositório neste registro

Sem qualquer correção aplicada. Este arquivo é **novo** e não toca nenhum outro —
seguro perante o trabalho em paralelo.
