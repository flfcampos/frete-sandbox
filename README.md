# dev-factory-sandbox

Biblioteca Python pequena para cálculo de frete, usada como sandbox.

## Uso

```python
from frete import calcular_frete

cotacao = calcular_frete(peso_kg=2, distancia_km=100, modalidade="expressa")
print(cotacao.valor, cotacao.prazo_dias)  # 30.00 2

# Frete grátis na modalidade padrão para pedidos a partir de R$ 300
cotacao = calcular_frete(peso_kg=2, distancia_km=100, valor_pedido=300)
print(cotacao.valor, cotacao.prazo_dias)  # 0.00 5
```

## Regras

- `valor = (10.00 + peso_kg * 2.50 + distancia_km * 0.05) * multiplicador`
- Modalidades: `padrao` (x1.0, 5 dias) e `expressa` (x1.5, 2 dias)
- Prazo: +1 dia a cada 500 km completos
- Peso entre 0 (exclusivo) e 30 kg; distância >= 0
- Valor arredondado para 2 casas (ROUND_HALF_UP)
- Frete grátis: parâmetro opcional `valor_pedido` (default `0`). Na modalidade
  `padrao`, se `valor_pedido >= 300`, o valor do frete é `0.00` (o prazo não
  muda). Nas demais modalidades o frete é cobrado normalmente.
- `valor_pedido` não pode ser negativo

## Desenvolvimento

```bash
pip install -e ".[dev]"
pytest
```
