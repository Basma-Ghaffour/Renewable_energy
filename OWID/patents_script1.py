from owid import catalog
import pandas as pd
import sys
import os
import subprocess
from dotenv import load_dotenv
# sys.path.append(os.path.join('..', 'Librairies'))
# print(os.path.join('..', 'Librairies'))
current_dir = os.path.dirname(
    os.path.abspath(__file__)
)  # chemin actuel qui doit absuluement être le dossier de travail "travail"
librairies_path = os.path.join(current_dir, "..", "Librairies")
sys.path.append(librairies_path)
import lib_Owid as lb  # noqa: E402
import alimentation_table_mysql as atm  # noqa: E402
from model_transformed_base import Patents  # noqa: E402


cat = catalog.find("renewable")
data = cat.iloc[5].load()
data = data.reset_index()
data = data.drop(columns=["sub_technology", "sector"])  # trop précis nous intéresse pas
data = data.groupby(["country", "year", "technology"], observed=False).agg(
    {"patents": "sum"}
)  # les lignes qui ont les même country year et technologie on fait la somme des brevets pour avoir une seule ligne pour un pays et pour une seul années
data = pd.DataFrame(data)
data.reset_index(level="technology")  # technologie deviens une variable
data = data.pivot_table(
    index=["country", "year"],
    columns="technology",
    values="patents",
    aggfunc="sum",
    observed=True,
)  # a la place d'avoir une seul variable catégorielle il y a pour chaque catégorie de technologie une colonnes provisoire trouver autres chose!!!!

data = data[~(data == 0).all(axis=1)]

# on enlever les pays /zone qui ont trop peu d'obervsation par années
liste_pays_filtre, nb = lb.pays_m_periode(data, 20)
data = data[data.index.get_level_values("country").isin(liste_pays_filtre)]

data = data.copy()
data["total_patents"] = data.sum(axis=1)

data = data.reset_index()


data["zone_type"] = data["country"].apply(lb.categorize_country)

# variabke pour les jointure si nécéssaire plus tard
data["id"] = data.apply(lambda row: f"{row['country']}_{row['year']}", axis=1)

# alimentation de la base de données SQL

load_dotenv()
db_url = os.getenv("DATABASE_URL1")


for col in [
    "Bioenergy",
    "Enabling Technologies",
    "Geothermal Energy",
    "Hydropower",
    "Ocean Energy",
    "Solar Energy",
    "Wind Energy",
    "total_patents",
]:
    data[col] = data[col].astype("int32")

data = data.rename(
    columns={
        "Wind Energy": "Wind_energy",
        "Solar Energy": "Solar_energy",
        "Geothermal Energy": "Geothermal_energy",
        "Ocean Energy": "Marine_energy",
        "Enabling Technologies": "Enabling_Technologies",
    }
)


atm.alimentation_donnee(Patents, data, db_url)


try:
    print("Exécution du script2.py pour la création des indicateurs")
    subprocess.run([sys.executable, "OWID/patents_script2.py"], check=True)
    print("Script2 exécuté avec succès.")
except subprocess.CalledProcessError as e:
    print(f"Erreur lors de l'exécution de script2.py: {e}")
