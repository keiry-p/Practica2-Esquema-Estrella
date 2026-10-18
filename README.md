# Práctica 2: Generación de un Esquema Estrella

## Objetivo
Transformar datos transaccionales OLTP en un esquema estrella para un Data Warehouse de ventas usando Python, Pandas y NumPy.

## Tecnologías
- Python 3.12
- Pandas
- NumPy

## Modelo dimensional
- Dim_Cliente
- Dim_Producto
- Dim_Tiempo
- Fact_Ventas

## Resultados
Se procesaron 500 transacciones simuladas y se generaron:
- Dim_Cliente: 9 registros
- Dim_Producto: 27 registros
- Dim_Tiempo: 21 registros
- Fact_Ventas: 500 registros

Se añadieron los atributos dia_semana y es_fin_semana a Dim_Tiempo.

## Instalación
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

## Ejecución
python esquema_estrella.py

## Nota
El modelo se construye con Pandas. La carga a PostgreSQL es una extensión opcional y no se implementó.
