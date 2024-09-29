from owid import catalog
import sys
import os
import pandas as pd
import subprocess
from dotenv import load_dotenv

current_dir = os.path.dirname(
    os.path.abspath(__file__)
)  # chemin actuel qui doit absuluement être le dossier de travail "travail"
librairies_path = os.path.join(current_dir, "..", "Librairies")
sys.path.append(librairies_path)
import lib_Owid as lb  # noqa: E402
from model_transformed_base import Cost  # noqa: E402
from alimentation_table_mysql import alimentation_donnee  # noqa: E402

cat = catalog.find("renewable")
data = cat.iloc[8].load()


# nettoyage/preparation de la base de données
list_pays = list(lb.dict_pays_periode(data)[0].keys())

tab_vm = lb.table_valeur_manquante(data)
data = pd.DataFrame(data)
missing_percentage = data.groupby("country", observed=True).apply(
    lambda x: x.isna().mean() * 100
)
# print(missing_percentage)
data_world = data[data.index.get_level_values("country") == "World"]
tab_vm2 = lb.table_valeur_manquante(data_world)
data_world = data_world[data_world.index.get_level_values("year") >= 2012]

data_world = data_world.rename(
    columns={
        "bioenergy": "Bioenergy",
        "geothermal": "Geothermal_energy",
        "hydropower": "Hydropower",
    }
)
data_world["Wind_energy"] = data_world["offshore_wind"] + data_world["onshore_wind"]
data_world["Solar_energy"] = (
    data_world["solar_photovoltaic"] + data_world["concentrated_solar_power"]
)
data_world.drop(
    columns=[
        "offshore_wind",
        "onshore_wind",
        "solar_photovoltaic",
        "concentrated_solar_power",
    ],
    inplace=True,
)

data_world["total_cost"] = data_world.sum(axis=1)
data_world = data_world.reset_index()
data_world["zone_type"] = data_world["country"].apply(lb.categorize_country)

data_world["id"] = data_world.apply(
    lambda row: f"{row['country']}_{row['year']}", axis=1
)

print(
    "Attention cette base de données ne contiens pas de données sur les coûts associée au énergie marine"
)

load_dotenv()
db_url = os.getenv("DATABASE_URL1")

alimentation_donnee(Cost, data_world, db_url)

# lancement du second script des indicateurs automatiquement pour l'instant le script 2 n'est pas d'actualité
try:
    print("Exécution du script2.py pour la création des indicateurs")
    subprocess.run([sys.executable, "OWID/cost_script2.py"], check=True)
    print("Script2 exécuté avec succès.")
except subprocess.CalledProcessError as e:
    print(f"Erreur lors de l'exécution de script2.py: {e}")
