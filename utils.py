# Import the required libraries
from io import BytesIO
import pandas as pd


COLS_PROVEEDORES = {
    "babelito": [
        "CODIGO",
        "DESCRIPCION",
        "COD.DE BARRAS",
        "COMERCIO S/IVA",
        "PUBLICO",
    ],
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
    cols_df = df.columns.to_list()

    resultado = {"proveedor": str, "tabla": pd.DataFrame}

    # Only check the first 5 columns to verify the conditions
    if df.iloc[6, :].to_list()[:5] == COLS_PROVEEDORES["babelito"]:
        df = adaptar_tabla_babelito(data=df)
        resultado["proveedor"] = "babelito"
    # Only check the first 3 columns to verify the conditions
    elif cols_df[:2] == COLS_PROVEEDORES["dispita"][:2]:
        df = adaptar_tabla_dispita(data=df)
        resultado["proveedor"] = "dispita"

    elif cols_df[:2] == COLS_PROVEEDORES["suizo"][:2]:
        df = adaptar_tabla_suizo(data=df)
        resultado["proveedor"] = "suizo"

    else:
        raise ValueError("Proveedor no existe o el formato de la tabla cambió")

    df.columns = ["codigo", "barra", "descripcion", "precio"]
    df["precio"] = df["precio"] * factor_de_multiplicacion
    resultado["tabla"] = df

    return resultado


def adaptar_tabla_babelito(data: pd.DataFrame) -> pd.DataFrame:

    idx_colnames = data.index[data.iloc[:, 0] == "CODIGO"][0]

    df_1 = pd.DataFrame(data.iloc[idx_colnames + 1 :, :5])  # noqa E203
    df_2 = pd.DataFrame(data.iloc[1:, 6:])
    df_final = pd.concat(
        [pd.DataFrame(dfi.values) for dfi in [df_1, df_2]],
        ignore_index=True,
    )
    df_final.columns = COLS_PROVEEDORES["babelito"]
    df_final = df_final[["CODIGO", "COD.DE BARRAS", "DESCRIPCION", "COMERCIO S/IVA"]]
    for col in ["CODIGO", "COD.DE BARRAS", "COMERCIO S/IVA"]:
        df_final[col] = pd.to_numeric(df_final[col], errors="coerce")
    return df_final


def adaptar_tabla_dispita(data: pd.DataFrame) -> pd.DataFrame:

    idx_primer_producto = data.index[data.iloc[:, 3] == "MAYOR"][0] + 1

    data = data.iloc[idx_primer_producto:, [0, 6, 1, 3]]
    data.iloc[:, -1] = pd.to_numeric(data.iloc[:, -1], errors="coerce")
    data = data.dropna()
    return data


def adaptar_tabla_suizo(data: pd.DataFrame) -> pd.DataFrame:
    return data.iloc[:, :4]


def to_excel(df: pd.DataFrame):
    in_memory_fp = BytesIO()
    df.to_excel(in_memory_fp)
    # Write the file out to disk to demonstrate that it worked.
    in_memory_fp.seek(0, 0)
    return in_memory_fp.read()
