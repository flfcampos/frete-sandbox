# dev-factory-sandbox

Biblioteca Python pequena para cálculo de frete, usada como sandbox.

## Uso

```python
from frete import calcular_frete

cotacao = calcular_frete(peso_kg=2, distancia_km=100, modalidade="expressa")
print(cotacao.valor, cotacao.prazo_dias)  # 30.00 2

# Pacote grande e leve: cobra pelo peso cubado (60×50×40 / 6000 = 20 kg)
calcular_frete(peso_kg=1, distancia_km=0, dimensoes_cm=(60, 50, 40)).valor  # 60.00
```

## Regras

- `valor = (10.00 + peso_tarifavel * 2.50 + distancia_km * 0.05) * multiplicador`
- Peso cubado (opcional): informe `dimensoes_cm=(comprimento, largura, altura)` em cm
  - `peso_cubado = C × L × A / 6000` (kg)
  - `peso_tarifavel = max(peso_kg, peso_cubado)`; sem `dimensoes_cm`, `peso_tarifavel = peso_kg`
  - O limite de 30 kg vale apenas para o peso real
  - Dimensões com qualquer valor `<= 0` levantam `ValueError`
- Modalidades: `padrao` (x1.0, 5 dias) e `expressa` (x1.5, 2 dias)
- Prazo: +1 dia a cada 500 km completos
- Peso entre 0 (exclusivo) e 30 kg; distância >= 0
- Valor arredondado para 2 casas (ROUND_HALF_UP)

## Desenvolvimento

```bash
pip install -e ".[dev]"
pytest
```
