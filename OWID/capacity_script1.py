from owid import catalog
import pandas as pd
import sys
import os
import subprocess
from dotenv import load_dotenv

# from sqlalchemy import create_engine
# from model_transformed_base import Base
# sys.path.append(os.path.join('..', 'Librairies'))
# print(os.path.join('..', 'Librairies'))
current_dir = os.path.dirname(
    os.path.abspath(__file__)
)  # chemin actuel qui doit absuluement être le dossier de travail "travail"
librairies_path = os.path.join(current_dir, "..", "Librairies")
sys.path.append(librairies_path)
import lib_Owid as lb  # noqa: E402
import alimentation_table_mysql as atm  # noqa: E402
from model_transformed_base import Capacity  # noqa: E402


# preparation/nettoyage base de données
cat = catalog.find("renewable")
data = cat.iloc[0].load()
data = pd.DataFrame(data)
lb.table_valeur_manquante(data)
lb.stat_desc_pays(data)
liste_pays_filtre, nb_obs_pays = lb.pays_m_periode(data)
data = data[data.index.get_level_values("country").isin(liste_pays_filtre)]
data = data["total_renewable_energy"]
data = data.reset_index()

data["zone_type"] = data["country"].apply(lb.categorize_country)
data["id"] = data.apply(lambda row: f"{row['country']}_{row['year']}", axis=1)

load_dotenv()
db_url = os.getenv("DATABASE_URL1")

atm.alimentation_donnee(Capacity, data, db_url)

try:
    subprocess.run([sys.executable, "OWID/capacity_script2.py"], check=True)
except subprocess.CalledProcessError as e:
    raise ValueError(
        f"Erreur lors de l'exécution du script OWID/capacity_script2.py: {e}"
    )
