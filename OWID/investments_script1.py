from owid import catalog
import pandas as pd
import subprocess
from dotenv import load_dotenv
import os
import sys
current_dir = os.path.dirname(
    os.path.abspath(__file__)
)  # chemin actuel qui doit absuluement être le dossier de travail "travail"
librairies_path = os.path.join(current_dir, "..", "Librairies")
sys.path.append(librairies_path)
import lib_Owid as lb  # noqa: E402
import alimentation_table_mysql as atm  # noqa: E402
from model_transformed_base import Investments  # noqa: E402



cat=catalog.find("renewable")
data=cat.iloc[3].load()

#Préparation de la base de données
data=data.rename(columns={'wind':'Wind_energy','solar':'Solar_energy','small_hydro':"Hydropower",'geothermal':"Geothermal_energy",'marine':'Marine_energy'})
data['Bioenergy'] = data['biofuels'] + data['biomass_and_waste']
data=data.drop(columns=['biofuels', 'biomass_and_waste'])
data['total_renewable_energy'] = data.sum(axis=1)
data=pd.DataFrame(data)
data=data.round(2)
data=data.reset_index()
data['id'] = data.apply(lambda row: f"{row['country']}_{row['year']}", axis=1)
data["zone_type"] = data["country"].apply(lb.categorize_country)


load_dotenv()
db_url = os.getenv("DATABASE_URL1")

atm.alimentation_donnee(Investments, data, db_url)


try:
    print("Exécution du script2.py pour la création des indicateurs")
    subprocess.run([sys.executable, "OWID/investments_script2.py"], check=True)
    print("Script2 exécuté avec succès.")
except subprocess.CalledProcessError as e:
    print(f"Erreur lors de l'exécution de script2.py: {e}")