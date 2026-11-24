"""Regras de cálculo de frete.

Fórmula:
    valor = (TAXA_BASE + peso_kg * PRECO_POR_KG + distancia_km * PRECO_POR_KM)
            * multiplicador_da_modalidade

Se ``dimensoes_cm`` for informado, ``peso_kg`` na fórmula é substituído pelo
peso tarifável: ``max(peso_real, peso_cubado)``, onde
``peso_cubado = comprimento * largura * altura / FATOR_CUBAGEM``.

O resultado é arredondado para 2 casas decimais (ROUND_HALF_UP).
"""

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

TAXA_BASE = Decimal("10.00")
PRECO_POR_KG = Decimal("2.50")
PRECO_POR_KM = Decimal("0.05")
PESO_MAXIMO_KG = Decimal("30")
FATOR_CUBAGEM = Decimal("6000")
VALOR_MINIMO_FRETE_GRATIS = Decimal("300")
MODALIDADES_FRETE_GRATIS = frozenset({"padrao"})


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


def _peso_cubado(dimensoes_cm: tuple[float, float, float]) -> Decimal:
    """Calcula o peso cubado (kg) a partir de (comprimento, largura, altura) em cm."""
    if len(dimensoes_cm) != 3:
        raise ValueError("dimensoes_cm deve ter 3 valores: (comprimento, largura, altura)")
    c, l, a = (Decimal(str(d)) for d in dimensoes_cm)
    if c <= 0 or l <= 0 or a <= 0:
        raise ValueError("dimensoes_cm devem ser maiores que zero")
    return c * l * a / FATOR_CUBAGEM


def calcular_frete(
    peso_kg: float | Decimal,
    distancia_km: float | Decimal,
    modalidade: str = "padrao",
    valor_pedido: float | Decimal = 0,
    dimensoes_cm: tuple[float, float, float] | None = None,
) -> Cotacao:
    """Calcula o valor e o prazo do frete.

    Se ``dimensoes_cm`` (comprimento, largura, altura) for informado, o valor é
    calculado sobre o maior entre o peso real e o peso cubado. O limite de peso
    máximo é aplicado apenas ao peso real.

    Pedidos com ``valor_pedido`` a partir de R$ 300 na modalidade ``padrao``
    têm frete grátis (o prazo não muda).

    Raises:
        ValueError: se peso/distância/valor do pedido/dimensões forem inválidos
            ou a modalidade não existir.
    """
    peso = Decimal(str(peso_kg))
    distancia = Decimal(str(distancia_km))
    pedido = Decimal(str(valor_pedido))

    if peso <= 0:
        raise ValueError("peso_kg deve ser maior que zero")
    if peso > PESO_MAXIMO_KG:
        raise ValueError(f"peso_kg excede o máximo de {PESO_MAXIMO_KG} kg")
    if distancia < 0:
        raise ValueError("distancia_km não pode ser negativa")
    if pedido < 0:
        raise ValueError("valor_pedido não pode ser negativo")
    if modalidade not in MODALIDADES:
        raise ValueError(
            f"modalidade inválida: {modalidade!r}. "
            f"Opções: {', '.join(sorted(MODALIDADES))}"
        )

    peso_tarifavel = peso
    if dimensoes_cm is not None:
        peso_tarifavel = max(peso, _peso_cubado(dimensoes_cm))

    mod = MODALIDADES[modalidade]
    bruto = TAXA_BASE + peso_tarifavel * PRECO_POR_KG + distancia * PRECO_POR_KM
    valor = (bruto * mod.multiplicador).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if modalidade in MODALIDADES_FRETE_GRATIS and pedido >= VALOR_MINIMO_FRETE_GRATIS:
        valor = Decimal("0.00")

    return Cotacao(
        valor=valor,
        prazo_dias=_prazo(distancia, mod.prazo_base_dias),
        modalidade=modalidade,
    )
