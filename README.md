# waas-antitrust

[![CC BY-SA 4.0](https://img.shields.io/badge/license-CC%20BY--SA%204.0-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Mesa 3.x](https://img.shields.io/badge/mesa-3.x-green.svg)](https://mesa.readthedocs.io/)
[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/freirelucas/waas-antitrust/blob/main/notebooks/WaaS_caderno_v2.ipynb)

Núcleo computacional do artigo **"Rescaling Leniency Programs for Digital Markets: A Whistleblower-as-a-Service Mechanism"**.

Modelo baseado em agentes (MBA) e análise de sensibilidade global para o mecanismo *Whistleblower-as-a-Service* (WaaS) aplicado ao enforcement antitruste em mercados digitais no Brasil.

## Início rápido

```bash
# Instalação em modo desenvolvimento
pip install -e ".[dev]"

# Testes
pytest

# Caderno de demonstração
jupyter lab notebooks/WaaS_caderno_v2.ipynb

# Varredura Sobol completa (versão definitiva do artigo)
python scripts/run_sobol_full.py --n-base 1024 --jobs -1 --out results/sobol_full.parquet

# Geração das figuras implementadas como módulo (inversão e fase; demais no caderno)
python scripts/gerar_figuras.py --out figuras/
```

## Documentação

- **Site**: <https://freirelucas.github.io/waas-antitrust/> — gerado com MkDocs Material e publicado pelo workflow `docs.yml` (requer GitHub Pages habilitado no repositório).
- **Caderno no Colab**: [abrir](https://colab.research.google.com/github/freirelucas/waas-antitrust/blob/main/notebooks/WaaS_caderno_v2.ipynb) — instala as dependências automaticamente no ambiente do Colab.
- **Paper**: `paper/main.tex` (rascunho) — compilado a PDF pelo workflow `paper.yml`.
- **Backlog de pesquisa**: `docs/DECISIONS.md` (itens R01–R06 rumo ao camera-ready).

## Estrutura

```
waas-antitrust/
├── src/waas_antitrust/        # Pacote Python instalável
│   ├── agents.py              # Três classes de agentes (MBA)
│   ├── model.py               # WaaSModel + parâmetros
│   ├── viz/                   # viz como módulo: inversão e fase (demais no caderno)
│   ├── sobol/                 # Varredura paramétrica
│   └── calibracao/            # Dados CADE e Brasscom
├── tests/                     # pytest + nbval
├── notebooks/                 # Caderno reprodutível
├── scripts/                   # Execuções longas (Sobol assíncrono)
├── figuras/                   # PNG + SVG versionados
├── paper/                     # LaTeX + bib
└── docs/                      # ODD, análise jurídica, referências
```

## Citação

Veja `CITATION.cff` para metadados estruturados (Zenodo-compatível).

```
L. (2026). waas-antitrust: agent-based model for Whistleblower-as-a-Service
in digital antitrust enforcement (v1.0) [Software]. Zenodo. https://doi.org/...
```

## Licença

Código e documentação sob [Creative Commons Atribuição-CompartilhaIgual 4.0 Internacional](LICENSE) (CC BY-SA 4.0).

## Articulação institucional

Este repositório é mantido independentemente da posição institucional do autor (IPEA/DIEST/COGIT). As opiniões aqui expressas não comprometem o IPEA.
