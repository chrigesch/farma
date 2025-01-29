# Import the required libraries
import pandas as pd
import streamlit as st

# Import local modules
from utils import convertir_precios, to_excel

# Set default values
if "factor_de_multiplicacion" not in st.session_state:
    st.session_state.factor_de_multiplicacion = None

if "proveedor" not in st.session_state:
    st.session_state.proveedor = None

if "tabla_adaptada" not in st.session_state:
    st.session_state.tabla_adaptada = None


def main():
    # Page setup
    st.set_page_config(
        page_title="Farma",
        layout="wide",
    )

    st.title(body="Farma")

    # Create file uploader object
    uploaded_file = st.file_uploader(label="Carga el Excel", type=["xls", "xlsx"])
    if uploaded_file is None:
        st.session_state.factor_de_multiplicacion = None
        st.session_state.proveedor = None
        st.session_state.tabla_adaptada = None
        st.stop()

    if uploaded_file.name[-3:] == "xls":
        data_original = pd.read_csv(
            filepath_or_buffer=uploaded_file,
            sep="\t",
            encoding="latin-1",
            decimal=",",
        )
    elif uploaded_file.name[-4:] == "xlsx":
        data_original = pd.read_excel(io=uploaded_file)

    slider = st.slider(
        label="Selecciona el factor de multiplicación",
        min_value=1.0,
        max_value=2.0,
        value=1.7,
    )
    button = st.button(label="Haz clic para calcular la tabla adaptada")

    if button:
        data_final_dict = convertir_precios(
            data=data_original,
            factor_de_multiplicacion=slider,
        )
        st.session_state.factor_de_multiplicacion = slider
        st.session_state.proveedor = data_final_dict["proveedor"]
        st.session_state.tabla_adaptada = data_final_dict["tabla"]

    if (
        (st.session_state.factor_de_multiplicacion is None)
        | (st.session_state.proveedor is None)
        | (st.session_state.tabla_adaptada is None)
    ):
        st.stop()

    st.subheader(body="Tabla original")
    st.dataframe(data_original)

    st.subheader(
        body=f"Tabla adaptada - {st.session_state.proveedor} - factor de multiplicación: {st.session_state.factor_de_multiplicacion}"  # noqa E501
    )
    st.download_button(
        label="Descargar la tabla adaptada",
        data=to_excel(st.session_state.tabla_adaptada.set_index("codigo")),
        file_name=f"tabla_adaptada_{st.session_state.proveedor}.xlsx",
    )
    st.table(
        st.session_state.tabla_adaptada.style.format(
            {
                "codigo": "{:.0f}",  # Show no formatting
                "barra": "{:.0f}",  # Show no formatting
                "precio": "{:.2f}",  # Show a float with two decimals
            }
        )
    )


if __name__ == "__main__":
    main()
