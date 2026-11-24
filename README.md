# dev-factory-sandbox

Biblioteca Python pequena para cálculo de frete, usada como sandbox.

## Uso

```python
from frete import calcular_frete

cotacao = calcular_frete(peso_kg=2, distancia_km=100, modalidade="expressa")
print(cotacao.valor, cotacao.prazo_dias)  # 30.00 2
```

## Regras

- `valor = (10.00 + peso_kg * 2.50 + distancia_km * 0.05) * multiplicador`
- Modalidades: `padrao` (x1.0, 5 dias) e `expressa` (x1.5, 2 dias)
- Prazo: +1 dia a cada 500 km completos
- Peso entre 0 (exclusivo) e 30 kg; distância >= 0
- Peso cubado (opcional, `dimensoes_cm=(C, L, A)`): `C × L × A / 6000` kg; o peso tarifável é `max(peso real, peso cubado)`. O limite de 30 kg vale só para o peso real; dimensões `<= 0` geram `ValueError`
- Valor arredondado para 2 casas (ROUND_HALF_UP)

## Desenvolvimento

```bash
pip install -e ".[dev]"
pytest
```
