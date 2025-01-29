# Import the required libraries
from io import BytesIO
import pandas as pd


COLS_PROVEEDORES = {
    "dispita": [
        "Unnamed: 0",
        "LINEA DISPITA",
        "Unnamed: 2",
        "Unnamed: 3",
        "Unnamed: 4",
        "Unnamed: 5",
        "Unnamed: 6",
        "Unnamed: 7",
    ],
    "suizo": [
        "Código",
        "Cód. barras",
        "Artículo",
        "Precio",
        "Precio con ofer",
        "Precio con dto",
        "PVP",
        "Proveedor",
        "cod_proveedor",
        "categoria",
        "cod_categoria",
        "subcategoria",
        "cod_subcategoria",
        "codigobarras1",
        "codigobarras2",
        "codigobarras3",
        "codigobarras4",
        "codigobarras5",
        "r",
        "s",
    ],
}


def convertir_precios(
    data: pd.DataFrame,
    factor_de_multiplicacion: float,
) -> dict:

    df = data.copy(deep=True)

    resultado = {"proveedor": str, "tabla": pd.DataFrame}

    if df.columns.to_list() == COLS_PROVEEDORES["dispita"]:

        idx_primer_producto = df.index[df.iloc[:, 1] == "PROMOCIONES"][0] + 1

        df = df.iloc[idx_primer_producto:, [0, 6, 1, 3]]
        df.iloc[:, -1] = pd.to_numeric(df.iloc[:, -1], errors="coerce")
        df = df.dropna()
        resultado["proveedor"] = "dispita"

    elif df.columns.to_list() == COLS_PROVEEDORES["suizo"]:
        df = df.iloc[:, :4]
        resultado["proveedor"] = "suizo"

    else:
        raise ValueError("Proveedor no existe o el formato de la tabla cambió")

    df.columns = ["codigo", "barra", "descripcion", "precio"]
    df["precio"] = df["precio"] * factor_de_multiplicacion
    resultado["tabla"] = df

    return resultado


def to_excel(df: pd.DataFrame):
    in_memory_fp = BytesIO()
    df.to_excel(in_memory_fp)
    # Write the file out to disk to demonstrate that it worked.
    in_memory_fp.seek(0, 0)
    return in_memory_fp.read()
