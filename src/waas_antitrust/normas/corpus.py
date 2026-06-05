"""Corpus local de normas — três textos-base do WaaS.

**Status de cada norma**: ver cabeçalho de cada arquivo em
`data/normas/`. Resumo:

- **Lei 12.529/2011 Art. 85 caput**: verbatim verificado contra
  `docs/INSTITUTIONAL.md`. Demais dispositivos: redação consolidada
  para teste interno, pendente verificação DOU (E04 em DECISIONS).
- **Lei 13.608/2018 Arts. 4º-A a 4º-C**: paráfrases consistentes com
  análise institucional do projeto; redação consolidada pendente DOU.
- **Resolução CADE 21/2018 Art. 12**: charneira jurídica do Regime B.
  E04 segue **aberto** — verificação verbatim contra DOU é
  pré-requisito para citação no paper.

Decisão de design: **não fetch em tempo de execução**. Toda integridade
do corpus vem do versionamento Git. Quando uma norma muda (ou é
verificada), o snapshot é atualizado num commit dedicado, rastreável.
"""

from __future__ import annotations

from importlib import resources
from pathlib import Path

from waas_antitrust.normas.urn import (
    URN_LEI_12529,
    URN_LEI_13608,
    URN_RESOLUCAO_CADE_21_2018,
    URNLex,
)


def _data_dir() -> Path:
    """Diretório `data/normas/` na raiz do repositório."""
    return Path(__file__).resolve().parents[3] / "data" / "normas"


#: Mapeamento URN canônica → arquivo no corpus local.
NORMAS_INDEXADAS: dict[str, str] = {
    str(URN_LEI_12529): "lei_12529_2011_arts_85_a_87.txt",
    str(URN_LEI_13608): "lei_13608_2018_arts_4a_a_4c.txt",
    str(URN_RESOLUCAO_CADE_21_2018): "resolucao_cade_21_2018_art_12.txt",
}


def carregar_norma(urn: URNLex | str) -> str:
    """Carrega o texto bruto de uma norma a partir do corpus local.

    Aceita objeto `URNLex` ou sua representação string. Levanta
    `KeyError` se a URN não estiver indexada.
    """
    urn_str = str(urn) if isinstance(urn, URNLex) else urn
    nome = NORMAS_INDEXADAS.get(urn_str)
    if nome is None:
        validas = ", ".join(NORMAS_INDEXADAS.keys())
        raise KeyError(
            f"URN {urn_str!r} não está indexada no corpus local. " f"Disponíveis: {validas}"
        )
    caminho = _data_dir() / nome
    if not caminho.is_file():
        # Fallback via importlib.resources (caso o pacote esteja instalado
        # sem data/ acessível pelo Path relativo).
        try:
            return (
                resources.files("waas_antitrust")
                .joinpath(f"../../data/normas/{nome}")
                .read_text(encoding="utf-8")
            )
        except Exception as exc:
            raise FileNotFoundError(
                f"Corpus local de normas não encontrado em {caminho}; "
                f"verifique data/normas/ no repositório."
            ) from exc
    return caminho.read_text(encoding="utf-8")


def listar_normas() -> list[str]:
    """URNs canônicas indexadas no corpus."""
    return list(NORMAS_INDEXADAS.keys())
