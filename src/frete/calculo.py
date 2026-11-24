"""Regras de cálculo de frete.

Fórmula:
    valor = (TAXA_BASE + peso_kg * PRECO_POR_KG + distancia_km * PRECO_POR_KM)
            * multiplicador_da_modalidade

O resultado é arredondado para 2 casas decimais (ROUND_HALF_UP).
"""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

TAXA_BASE = Decimal("10.00")
PRECO_POR_KG = Decimal("2.50")
PRECO_POR_KM = Decimal("0.05")
PESO_MAXIMO_KG = Decimal("30")


@dataclass(frozen=True)
class Modalidade:
    multiplicador: Decimal
    prazo_base_dias: int


MODALIDADES: dict[str, Modalidade] = {
    "padrao": Modalidade(multiplicador=Decimal("1.0"), prazo_base_dias=5),
    "expressa": Modalidade(multiplicador=Decimal("1.5"), prazo_base_dias=2),
    "economica": Modalidade(multiplicador=Decimal("0.8"), prazo_base_dias=8),
}


@dataclass(frozen=True)
class Cotacao:
    valor: Decimal
    prazo_dias: int
    modalidade: str


def _prazo(distancia_km: Decimal, prazo_base: int) -> int:
    """Soma 1 dia extra a cada 500 km completos."""
    return prazo_base + int(distancia_km // 500)


def calcular_frete(
    peso_kg: float | Decimal,
    distancia_km: float | Decimal,
    modalidade: str = "padrao",
) -> Cotacao:
    """Calcula o valor e o prazo do frete.

    Raises:
        ValueError: se peso/distância forem inválidos ou a modalidade não existir.
    """
    peso = Decimal(str(peso_kg))
    distancia = Decimal(str(distancia_km))

    if peso <= 0:
        raise ValueError("peso_kg deve ser maior que zero")
    if peso > PESO_MAXIMO_KG:
        raise ValueError(f"peso_kg excede o máximo de {PESO_MAXIMO_KG} kg")
    if distancia < 0:
        raise ValueError("distancia_km não pode ser negativa")
    if modalidade not in MODALIDADES:
        raise ValueError(
            f"modalidade inválida: {modalidade!r}. "
            f"Opções: {', '.join(sorted(MODALIDADES))}"
        )

    mod = MODALIDADES[modalidade]
    bruto = TAXA_BASE + peso * PRECO_POR_KG + distancia * PRECO_POR_KM
    valor = (bruto * mod.multiplicador).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return Cotacao(
        valor=valor,
        prazo_dias=_prazo(distancia, mod.prazo_base_dias),
        modalidade=modalidade,
    )
