# Import the required libraries
import pandas as pd
import streamlit as st

# Import local modules
from utils import convertir_precios, to_excel


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
    data_final_dict = convertir_precios(
        data=data_original,
        factor_de_multiplicacion=slider,
    )

    st.subheader(body="Tabla original")
    st.dataframe(data_original)

    st.subheader(body="Tabla adaptada")
    st.download_button(
        label="Descargar la tabla adaptada",
        data=to_excel(data_final_dict["tabla"].set_index("codigo")),
        file_name=f"tabla_adaptada_{data_final_dict['proveedor']}.xlsx",
    )
    st.table(
        data_final_dict["tabla"].style.format(
            {
                "codigo": "{:.0f}",  # Show no formatting
                "barra": "{:.0f}",  # Show no formatting
                "precio": "{:.2f}",  # Show a float with two decimals
            }
        )
    )


if __name__ == "__main__":
    main()
