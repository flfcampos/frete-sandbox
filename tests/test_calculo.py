from decimal import Decimal

import pytest

from frete import calcular_frete


def test_frete_padrao_valor_e_prazo():
    # 10 + 2*2.50 + 100*0.05 = 20.00
    cotacao = calcular_frete(peso_kg=2, distancia_km=100)
    assert cotacao.valor == Decimal("20.00")
    assert cotacao.prazo_dias == 5
    assert cotacao.modalidade == "padrao"


def test_frete_expresso_aplica_multiplicador():
    # 20.00 * 1.5 = 30.00
    cotacao = calcular_frete(peso_kg=2, distancia_km=100, modalidade="expressa")
    assert cotacao.valor == Decimal("30.00")
    assert cotacao.prazo_dias == 2


def test_prazo_aumenta_a_cada_500_km():
    assert calcular_frete(1, 499).prazo_dias == 5
    assert calcular_frete(1, 500).prazo_dias == 6
    assert calcular_frete(1, 1250).prazo_dias == 7


def test_arredondamento_duas_casas():
    # 10 + 1.333*2.50 + 0 = 13.3325 -> 13.33
    assert calcular_frete(1.333, 0).valor == Decimal("13.33")


@pytest.mark.parametrize(
    "peso, distancia, modalidade",
    [
        (0, 10, "padrao"),
        (-1, 10, "padrao"),
        (31, 10, "padrao"),
        (1, -5, "padrao"),
        (1, 10, "teletransporte"),
    ],
)
def test_entradas_invalidas_levantam_value_error(peso, distancia, modalidade):
    with pytest.raises(ValueError):
        calcular_frete(peso, distancia, modalidade)


def test_peso_cubado_maior_que_real():
    assert calcular_frete(1, 0, dimensoes_cm=(60, 50, 40)).valor == Decimal("60.00")


def test_peso_real_maior_que_cubado():
    assert calcular_frete(5, 0, dimensoes_cm=(10, 10, 10)).valor == Decimal("22.50")


def test_dimensoes_invalidas():
    with pytest.raises(ValueError):
        calcular_frete(1, 0, dimensoes_cm=(0, 10, 10))


def test_cubado_nao_afeta_limite_de_peso_real():
    assert calcular_frete(30, 0, dimensoes_cm=(10, 10, 10)).valor == Decimal("85.00")
