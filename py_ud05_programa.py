# =============================================================================
# PROGRAMA: Análisis de ventas diarias — Lectura y escritura de archivos
# MÓDULO:   Python optativo — UD05
# AUTOR:    Esteban Ospina
# FECHA:    Marzo 2026
# =============================================================================
# DESCRIPCIÓN:
#   Script de análisis de ventas que:
#     1. Lee los datos del archivo "ventas_diarias.txt"
#     2. Calcula el total de unidades vendidas por producto
#     3. Guarda los resultados en "resumen_ventas.txt"
#     4. Muestra un informe por consola
#
# FORMATO DEL ARCHIVO DE ENTRADA:
#   Cada línea contiene: nombre_producto,cantidad
#   Ejemplo: Monitor 4K,15
# =============================================================================

import os  # Para comprobar si el archivo de entrada existe


# =============================================================================
# CONSTANTES — rutas de los archivos
# =============================================================================
ARCHIVO_ENTRADA = "ventas_diarias.txt"
ARCHIVO_SALIDA = "resumen_ventas.txt"


# =============================================================================
# FUNCIONES
# =============================================================================


def leer_ventas(ruta_archivo):
    """
    Lee el archivo de ventas línea a línea y devuelve una lista de tuplas
    con (nombre_producto, cantidad).

    Parámetros:
        ruta_archivo (str): Ruta al archivo de entrada

    Retorna:
        list[tuple]: Lista de (producto, cantidad) o lista vacía si hay error

    Lanza:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si alguna línea tiene formato incorrecto
    """
    # Comprobamos que el archivo existe antes de intentar abrirlo
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"No se encontró el archivo: '{ruta_archivo}'")

    registros = []  # Lista que acumulará los pares (producto, cantidad)

    # Abrimos el archivo en modo lectura con codificación UTF-8
    # El bloque 'with' cierra el archivo automáticamente al salir
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        for numero_linea, linea in enumerate(archivo, start=1):

            # .strip() elimina saltos de línea y espacios al inicio/final
            linea_limpia = linea.strip()

            # Ignorar líneas vacías (por ejemplo, al final del archivo)
            if not linea_limpia:
                continue

            # Separamos por coma — esperamos exactamente dos campos
            partes = linea_limpia.split(",")

            if len(partes) != 2:
                print(
                    f"  ⚠  Línea {numero_linea} ignorada (formato incorrecto): '{linea_limpia}'"
                )
                continue

            nombre_producto = partes[0].strip()  # Nombre del producto
            cantidad_str = partes[1].strip()  # Cantidad como texto

            # Convertimos la cantidad a entero con validación
            try:
                cantidad_vendida = int(cantidad_str)
            except ValueError:
                print(
                    f"  ⚠  Línea {numero_linea}: cantidad no válida '{cantidad_str}' — ignorada."
                )
                continue

            # Validar que la cantidad sea positiva
            if cantidad_vendida < 0:
                print(
                    f"  ⚠  Línea {numero_linea}: cantidad negativa ({cantidad_vendida}) — ignorada."
                )
                continue

            # Añadimos la tupla (producto, cantidad) a la lista
            registros.append((nombre_producto, cantidad_vendida))

    return registros


def calcular_totales(registros):
    """
    Calcula el total de unidades vendidas por producto acumulando
    las cantidades de todos los registros.

    Parámetros:
        registros (list[tuple]): Lista de (producto, cantidad)

    Retorna:
        dict: Diccionario {nombre_producto: total_vendido}
    """
    totales_por_producto = {}  # Diccionario acumulador

    for nombre_producto, cantidad_vendida in registros:

        # Si el producto ya existe, sumamos la nueva cantidad
        # Si no existe, .get() devuelve 0 como valor por defecto
        total_actual = totales_por_producto.get(nombre_producto, 0)
        totales_por_producto[nombre_producto] = total_actual + cantidad_vendida

    return totales_por_producto


def guardar_resumen(totales_por_producto, ruta_archivo):
    """
    Guarda el diccionario de totales en un archivo de texto.
    Los productos se ordenan alfabéticamente antes de guardar.

    Formato de salida: nombre_producto,total_vendido

    Parámetros:
        totales_por_producto (dict): Diccionario {producto: total}
        ruta_archivo (str): Ruta del archivo de salida
    """
    # Ordenamos el diccionario alfabéticamente por nombre de producto
    # sorted() devuelve una lista de pares (clave, valor) ordenada
    productos_ordenados = sorted(totales_por_producto.items())

    # Abrimos en modo escritura ('w') — crea el archivo si no existe,
    # lo sobreescribe si ya existe
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:

        # Cabecera del archivo de salida
        archivo.write("RESUMEN DE VENTAS POR PRODUCTO\n")
        archivo.write("=" * 40 + "\n")
        archivo.write("Producto,Total vendido\n")
        archivo.write("-" * 40 + "\n")

        # Escribimos una línea por cada producto
        for nombre_producto, total_vendido in productos_ordenados:
            archivo.write(f"{nombre_producto},{total_vendido}\n")

    print(f"  ✅ Resultados guardados en '{ruta_archivo}'.")


def mostrar_informe(totales_por_producto):
    """
    Muestra por consola un informe formateado con los totales
    y estadísticas adicionales.

    Parámetros:
        totales_por_producto (dict): Diccionario {producto: total}
    """
    print("\n" + "=" * 55)
    print("   INFORME DE VENTAS POR PRODUCTO")
    print("=" * 55)

    # Ordenar por total vendido de mayor a menor para el informe
    productos_por_ventas = sorted(
        totales_por_producto.items(),
        key=lambda par: par[1],  # Ordena por el valor (total)
        reverse=True,  # De mayor a menor
    )

    print(f"  {'Producto':<25} {'Total vendido':>14}")
    print("  " + "-" * 42)

    for nombre_producto, total_vendido in productos_por_ventas:
        print(f"  {nombre_producto:<25} {total_vendido:>12} ud.")

    # --- Estadísticas adicionales -----------------------------------
    total_global = sum(totales_por_producto.values())
    producto_mas_vendido = max(totales_por_producto, key=totales_por_producto.get)
    producto_menos_vendido = min(totales_por_producto, key=totales_por_producto.get)
    numero_productos = len(totales_por_producto)

    print("  " + "-" * 42)
    print(f"\n  Total productos distintos: {numero_productos}")
    print(f"  Total unidades vendidas:   {total_global}")
    print(
        f"  Producto más vendido:      {producto_mas_vendido} ({totales_por_producto[producto_mas_vendido]} ud.)"
    )
    print(
        f"  Producto menos vendido:    {producto_menos_vendido} ({totales_por_producto[producto_menos_vendido]} ud.)"
    )
    print("=" * 55)


# =============================================================================
# BLOQUE PRINCIPAL
# =============================================================================

if __name__ == "__main__":

    print("=" * 55)
    print("   ANÁLISIS DE VENTAS DIARIAS — UD05")
    print("=" * 55)
    print(f"  Archivo de entrada: {ARCHIVO_ENTRADA}")
    print(f"  Archivo de salida:  {ARCHIVO_SALIDA}")

    try:
        # PASO 1: Leer los registros del archivo de entrada
        print(f"\n  Leyendo '{ARCHIVO_ENTRADA}'...")
        registros_ventas = leer_ventas(ARCHIVO_ENTRADA)
        print(f"  ✅ {len(registros_ventas)} registros leídos correctamente.")

        # PASO 2: Calcular totales por producto
        totales = calcular_totales(registros_ventas)
        print(f"  ✅ Totales calculados para {len(totales)} productos.")

        # PASO 3: Guardar resultados en el archivo de salida
        guardar_resumen(totales, ARCHIVO_SALIDA)

        # PASO 4: Mostrar informe en consola
        mostrar_informe(totales)

    except FileNotFoundError as error:
        # Error controlado: el archivo de entrada no existe
        print(f"\n  ❌ ERROR: {error}")
        print(
            "  Asegúrate de que 'ventas_diarias.txt' está en la misma carpeta que el script."
        )

    except Exception as error:
        # Cualquier otro error inesperado
        print(f"\n  ❌ Error inesperado: {error}")
