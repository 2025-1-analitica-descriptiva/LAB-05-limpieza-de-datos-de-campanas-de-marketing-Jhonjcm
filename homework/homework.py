"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


# homework.py

import os
import zipfile
import pandas as pd
from io import TextIOWrapper
from datetime import datetime


def clean_campaign_data():
    input_folder = os.path.join("files", "input")
    output_folder = os.path.join("files", "output")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    dataframes = []

    # Procesar todos los archivos .zip de entrada
    for i in range(10):
        zip_filename = f"bank-marketing-campaing-{i}.csv.zip"
        zip_path = os.path.join(input_folder, zip_filename)

        with zipfile.ZipFile(zip_path, "r") as z:
            for name in z.namelist():
                with z.open(name) as f:
                    df = pd.read_csv(TextIOWrapper(f, encoding="utf-8"), index_col=False)
                    dataframes.append(df)

    # Unir todos los dataframes
    df_total = pd.concat(dataframes, ignore_index=True)

    # ================================
    # Client.csv
    # ================================
    client = df_total[[
        "client_id", "age", "job", "marital", "education", "credit_default", "mortgage"
    ]].copy()

    client["job"] = client["job"].str.replace(".", "", regex=False).str.replace("-", "_", regex=False)
    client["education"] = client["education"].str.replace(".", "_", regex=False)
    client["education"] = client["education"].replace("unknown", pd.NA)
    client["credit_default"] = client["credit_default"].apply(lambda x: 1 if x == "yes" else 0)
    client["mortgage"] = client["mortgage"].apply(lambda x: 1 if x == "yes" else 0)

    client.to_csv(os.path.join(output_folder, "client.csv"), index=False)

    # ================================
    # Campaign.csv
    # ================================
    campaign = df_total[[
        "client_id", "number_contacts", "contact_duration",
        "previous_campaign_contacts", "previous_outcome",
        "campaign_outcome", "day", "month"
    ]].copy()

    campaign["previous_outcome"] = campaign["previous_outcome"].apply(lambda x: 1 if x == "success" else 0)
    campaign["campaign_outcome"] = campaign["campaign_outcome"].apply(lambda x: 1 if x == "yes" else 0)

    # Convertir a formato fecha YYYY-MM-DD
    month_map = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04",
        "may": "05", "jun": "06", "jul": "07", "aug": "08",
        "sep": "09", "oct": "10", "nov": "11", "dec": "12"
    }
    campaign["month"] = campaign["month"].str.lower().map(month_map)
    campaign["day"] = campaign["day"].astype(str).str.zfill(2)
    campaign["last_contact_date"] = "2022-" + campaign["month"] + "-" + campaign["day"]

    # Filtrar columnas finales
    campaign = campaign[[
        "client_id", "number_contacts", "contact_duration",
        "previous_campaign_contacts", "previous_outcome",
        "campaign_outcome", "last_contact_date"
    ]]

    campaign.to_csv(os.path.join(output_folder, "campaign.csv"), index=False)

    # ================================
    # Economics.csv
    # ================================
    economics = df_total[[
        "client_id", "cons_price_idx", "euribor_three_months"
    ]].copy()

    economics.to_csv(os.path.join(output_folder, "economics.csv"), index=False)




    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """

    return

if __name__ == "__main__":
    clean_campaign_data()
