
import pandas as pd
import numpy as np

# ==========================================
# PRACTICA 2: ESQUEMA ESTRELLA
# ==========================================

# 1. DATOS OPERACIONALES (OLTP)
np.random.seed(101)
n = 500

df_operativo = pd.DataFrame({
    "id_transaccion": range(1000, 1000 + n),
    "fecha_hora": pd.date_range(
        start="2026-01-01", periods=n, freq="h"
    ),
    "cliente_nombre": np.random.choice(
        ["Juan Pérez", "María Gómez", "Carlos Ruiz"], n
    ),
    "cliente_ciudad": np.random.choice(
        ["Puebla", "CDMX", "Guadalajara"], n
    ),
    "producto_nombre": np.random.choice(
        ["Laptop Dell", "Mouse Logi", "Monitor LG"], n
    ),
    "categoria_prod": np.random.choice(
        ["Cómputo", "Accesorios", "Pantallas"], n
    ),
    "precio_unitario": np.random.choice(
        [15000.0, 350.0, 4500.0], n
    ),
    "cantidad": np.random.randint(1, 5, n)
})

# 2. DIMENSION CLIENTE
dim_cliente = df_operativo[
    ["cliente_nombre", "cliente_ciudad"]
].drop_duplicates().reset_index(drop=True)

dim_cliente["id_cliente_sk"] = dim_cliente.index + 1

# 3. DIMENSION PRODUCTO
dim_producto = df_operativo[
    ["producto_nombre", "categoria_prod", "precio_unitario"]
].drop_duplicates().reset_index(drop=True)

dim_producto["id_producto_sk"] = dim_producto.index + 1

# 4. DIMENSION TIEMPO
dim_tiempo = pd.DataFrame({
    "fecha_completa": pd.to_datetime(
        df_operativo["fecha_hora"].dt.date.unique()
    )
})

dim_tiempo["id_tiempo_sk"] = (
    dim_tiempo["fecha_completa"]
    .dt.strftime("%Y%m%d").astype(int)
)

dim_tiempo["anio"] = dim_tiempo["fecha_completa"].dt.year
dim_tiempo["mes"] = dim_tiempo["fecha_completa"].dt.month
dim_tiempo["dia"] = dim_tiempo["fecha_completa"].dt.day

# ATRIBUTOS ADICIONALES SOLICITADOS
dim_tiempo["dia_semana"] = (
    dim_tiempo["fecha_completa"].dt.day_name()
)

dim_tiempo["es_fin_semana"] = (
    dim_tiempo["fecha_completa"].dt.dayofweek >= 5
)

# 5. TABLA DE HECHOS
fact_ventas = (
    df_operativo
    .merge(
        dim_cliente,
        on=["cliente_nombre", "cliente_ciudad"],
        validate="many_to_one"
    )
    .merge(
        dim_producto,
        on=[
            "producto_nombre",
            "categoria_prod",
            "precio_unitario"
        ],
        validate="many_to_one"
    )
)

fact_ventas["fecha_completa"] = pd.to_datetime(
    fact_ventas["fecha_hora"].dt.date
)

fact_ventas = fact_ventas.merge(
    dim_tiempo,
    on="fecha_completa",
    validate="many_to_one"
)

fact_ventas["monto_total"] = (
    fact_ventas["cantidad"] *
    fact_ventas["precio_unitario"]
)

fact_table = fact_ventas[[
    "id_transaccion",
    "id_cliente_sk",
    "id_producto_sk",
    "id_tiempo_sk",
    "cantidad",
    "monto_total"
]]

# 6. COMPROBACIONES
assert len(fact_table) == n, "Se perdieron transacciones"
assert not fact_table.isnull().any().any(), "Hay claves o datos nulos"

# 7. RESULTADOS RESUMIDOS
print("=== PRACTICA 2: ESQUEMA ESTRELLA ===")
print("Transacciones originales:", len(df_operativo))
print("Dim_Cliente:", len(dim_cliente), "registros")
print("Dim_Producto:", len(dim_producto), "registros")
print("Dim_Tiempo:", len(dim_tiempo), "registros")
print("Fact_Ventas:", len(fact_table), "registros")

print("\n=== DIM_CLIENTE ===")
print(dim_cliente.head(5).to_string(index=False))

print("\n=== DIM_PRODUCTO ===")
print(dim_producto.head(5).to_string(index=False))

print("\n=== DIM_TIEMPO ===")
print(dim_tiempo.head(5).to_string(index=False))

print("\n=== FACT_VENTAS ===")
print(fact_table.head(5).to_string(index=False))

print("\nEsquema estrella generado correctamente.")
