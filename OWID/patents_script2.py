from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv
import os
import sys

current_dir = os.path.dirname(
    os.path.abspath(__file__)
)  # chemin actuel qui doit absuluement être le dossier de travail "travail"
librairies_path = os.path.join(current_dir, "..", "Librairies")
sys.path.append(librairies_path)
from alimentation_table_mysql import alimentation_donnee  # noqa: E402
from model_indicators_base import Patents_PBE, Patents_GARE  # noqa: E402

load_dotenv()
db_url = os.getenv("DATABASE_URL1")
db_url2 = os.getenv("DATABASE_URL2")

engine = create_engine(db_url)


data = pd.read_sql_table("patents", con=engine)
# data= data.set_index(['year', 'country','zone_type','id'])

# création du premier indicateur

data[
    [
        "Wind_energy",
        "Solar_energy",
        "Hydropower",
        "Geothermal_energy",
        "Marine_energy",
        "Bioenergy",
        "Enabling_Technologies",
    ]
] = (
    data[
        [
            "Wind_energy",
            "Solar_energy",
            "Hydropower",
            "Geothermal_energy",
            "Marine_energy",
            "Bioenergy",
            "Enabling_Technologies",
        ]
    ].div(data["total_patents"], axis=0)
    * 100
)
data = data.round(2)
data = data.drop(columns="total_patents")


alimentation_donnee(Patents_PBE, data, db_url2)


# création de la seconde base de données d'indicateur

data2 = pd.read_sql_table("patents", con=engine)
data2["total_patents_growth"] = data2["total_patents"].pct_change() * 100
col_sup = [
    "Wind_energy",
    "Solar_energy",
    "Hydropower",
    "Geothermal_energy",
    "Marine_energy",
    "Bioenergy",
    "Enabling_Technologies",
    "total_patents",
]
data2 = data2.drop(columns=col_sup)
data2 = data2.dropna()

alimentation_donnee(Patents_GARE, data2, db_url2)
