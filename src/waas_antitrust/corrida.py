"""Mecânica de corrida por leniência coletiva interna (R20, exploratório).

Sob `WaaSParametros.modo_corrida = True`, o WaaS deixa de ser apenas
"incentivo ao denunciante interno" e vira **leniência coletiva interna
condicionada**:

1. Dentro de cada firma, trabalhadores competem por **ordem de
   cooperação interna**. Quem chega primeiro ganha recompensa total;
   posições posteriores ganham fração decrescente.

2. Entre firmas, a primeira a satisfazer um gatilho de massa crítica
   interna (`q_min` × `n_trabalhadores`) ganha a **posição 1 na fila
   de leniência inter-firma**, com desconto pleno do TCC.

Ambos os decaimentos usam o **mesmo dado empírico**: o gradiente
calibrado contra Saito (2021) — médias de desconto por posição na fila
do CADE (Imagem 23, p. 38), reproduzidas verbatim em
`calibracao.saito.MEDIA_DESCONTO_SG_POR_POSICAO`.

Postura epistêmica:

- Sob `modo_corrida = False` (default), nada deste módulo é consultado
  — caminho histórico preservado integralmente.
- Sob `modo_corrida = True`, o cenário ativo deixa explícito que se
  trata de **proposta normativa** (resolução CADE complementar à
  21/2018), não desenho neutro.

Caveat empírico:

- Saito reporta médias **por posição na fila**, não por janela
  temporal. Aqui assumimos ordem de cooperação ≡ ordem temporal.
- O gradiente vem de **cartel**, não conduta unilateral; uso como
  proxy enquanto CADE não publica TCCs de conduta unilateral
  decompostos por posição (E04 + R03b).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from waas_antitrust.calibracao import saito


def decaimento_D(posicao_firma: int, perfil: str = "saito") -> float:
    """Desconto da firma como fração de S, função da posição na fila
    de leniência inter-firma.

    Calibrado contra Saito (2021), Imagem 23, p. 38. Posição ≥ 9 ou
    ausência de cooperação interna caem para o teto Tribunal/CADE
    (15%, Saito Imagem 25, p. 39).
    """
    if perfil != "saito":
        raise ValueError(f"perfil desconhecido: {perfil!r}. Válidos: 'saito'.")
    return saito.MEDIA_DESCONTO_SG_POR_POSICAO.get(
        posicao_firma, saito.MEDIA_DESCONTO_TRIBUNAL_1A_POSICAO
    )


def decaimento_W(posicao_trabalhador: int, W_base: float, perfil: str = "saito") -> float:
    """Recompensa do trabalhador `W_efetivo = W_base × f_W(k)`.

    `f_W` espelha o gradiente Saito normalizado pela 1ª posição:

        f_W(1) = D(1)/D(1) = 1.00
        f_W(2) = D(2)/D(1) ≈ 0.795
        f_W(3) = D(3)/D(1) ≈ 0.466
        ...

    Justificativa: o mesmo dado empírico que calibra a fila do CADE
    (inter-firma) ancora a fila intra-firma — paralelismo intencional
    com a leniência clássica, transposto para o microcosmo interno.
    """
    if perfil != "saito":
        raise ValueError(f"perfil desconhecido: {perfil!r}. Válidos: 'saito'.")
    if posicao_trabalhador < 1:
        raise ValueError(f"posicao_trabalhador deve ser ≥ 1; recebeu {posicao_trabalhador}.")
    d_k = saito.MEDIA_DESCONTO_SG_POR_POSICAO.get(
        posicao_trabalhador, saito.MEDIA_DESCONTO_TRIBUNAL_1A_POSICAO
    )
    d_1 = saito.MEDIA_DESCONTO_SG_1A_POSICAO
    return float(W_base * (d_k / d_1))


@dataclass
class FilaInternaCooperacao:
    """Ordem de cooperação interna a uma firma.

    Cada trabalhador entra com um tique único; a posição é determinada
    pela ordem de chegada (tique crescente). Para empate em tique
    (vários cooperadores simultâneos), usa-se ordem de inserção.
    """

    empresa_id: int
    cooperadores: list[tuple[int, int]] = field(default_factory=list)
    """Lista de (trabalhador_id, tique) na ordem de cooperação."""

    def registrar(self, trabalhador_id: int, tique: int) -> int:
        """Registra `trabalhador_id` cooperando em `tique` e devolve sua
        posição (1-indexada).

        Idempotente: se o mesmo `trabalhador_id` já estiver registrado,
        devolve a posição existente sem duplicar.
        """
        for k, (tid, _) in enumerate(self.cooperadores, start=1):
            if tid == trabalhador_id:
                return k
        self.cooperadores.append((trabalhador_id, tique))
        return len(self.cooperadores)

    def posicao(self, trabalhador_id: int) -> int | None:
        """Posição (1-indexada) de `trabalhador_id`; None se não cooperou."""
        for k, (tid, _) in enumerate(self.cooperadores, start=1):
            if tid == trabalhador_id:
                return k
        return None

    def __len__(self) -> int:
        return len(self.cooperadores)


@dataclass
class FilaLeniencia:
    """Ordem em que firmas atingiram massa crítica interna (`q_min`).

    A primeira firma a fechar o gatilho ganha posição 1 (desconto 43%);
    a segunda, posição 2 (34%); etc. Empates em tique são quebrados
    pela ordem de inserção.
    """

    posicoes: list[tuple[int, int]] = field(default_factory=list)
    """Lista de (empresa_id, tique_atingiu_massa_critica)."""

    def registrar(self, empresa_id: int, tique: int) -> int:
        """Registra firma e devolve sua posição (1-indexada). Idempotente."""
        for k, (eid, _) in enumerate(self.posicoes, start=1):
            if eid == empresa_id:
                return k
        self.posicoes.append((empresa_id, tique))
        return len(self.posicoes)

    def posicao(self, empresa_id: int) -> int | None:
        for k, (eid, _) in enumerate(self.posicoes, start=1):
            if eid == empresa_id:
                return k
        return None

    def __len__(self) -> int:
        return len(self.posicoes)


def massa_critica_interna_atingida(
    n_cooperadores: int,
    n_trabalhadores: int,
    q_min: float,
) -> bool:
    """Devolve True se a fração de cooperadores atingiu o gatilho de
    leniência coletiva interna.

    Sob `modo_corrida = True`, o atenuante do Art. 12 da Res. 21/2018
    é condicionado a `n_cooperadores ≥ q_min × n_trabalhadores`.
    """
    if n_trabalhadores <= 0:
        return False
    if not 0.0 < q_min <= 1.0:
        raise ValueError(f"q_min deve estar em (0, 1]; recebeu {q_min}.")
    return n_cooperadores / n_trabalhadores >= q_min
