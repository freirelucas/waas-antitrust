"""§10 — robustez por reamostragem.

Implementação completa no caderno `notebooks/WaaS_caderno_v2.ipynb`, seção §10.

A migração desta visualização para módulo Python independente está prevista no
backlog do projeto (vide `docs/DECISIONS.md`). Esta é uma decisão consciente:
manter o caderno como referência canônica até a estabilização das interfaces.
"""

import warnings
from typing import NoReturn


def gerar_figura() -> NoReturn:
    """Placeholder. Veja o caderno para a implementação atual."""
    warnings.warn(
        "Implementação de bootstrap ainda no caderno. Migrar para módulo é tarefa "
        "rastreada em docs/DECISIONS.md.",
        FutureWarning,
        stacklevel=2,
    )
    raise NotImplementedError(
        "Implementação atual está em notebooks/WaaS_caderno_v2.ipynb, seção §10."
    )
