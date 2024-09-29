from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
import sys
current_dir = os.path.dirname(
    os.path.abspath(__file__)
)  # chemin actuel qui doit absuluement être le dossier de travail "travail"
librairies_path = os.path.join(current_dir, "..", "Librairies")
sys.path.append(librairies_path)
from alimentation_table_mysql import alimentation_donnee  # noqa: E402
from model_indicators_base import Capacity_GAR  # noqa: E402

load_dotenv()
db_url = os.getenv("DATABASE_URL1")
db_url2 = os.getenv("DATABASE_URL2")

engine = create_engine(db_url)

# cration indicateur

data = pd.read_sql_table("capacity", con=engine)
data["Capacity_Growth"] = (
    data.groupby("country", observed=True)["total_renewable_energy"].pct_change() * 100
)
data["Capacity_Growth"] = data["Capacity_Growth"].replace([np.inf, -np.inf], np.nan)
# Remplacer tous les NaN par None
# data = data.where(pd.notnull(data), None) option qui permetterai de remplacer les NaN par NULL (NaN n'étant pas supproter par mySQL)
data = (
    data.dropna()
)  # option qui supprime les ligne avec NaN comme elle ne seron pas exploitable autant les supprimer
data = data.round(
    2
)  # il y a aura forcément des valeur nul pour la première années d'observation elle n'on pas été enlevé

engine2 = create_engine(db_url2)

alimentation_donnee(Capacity_GAR, data, db_url2)
