from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
import os
import sys
current_dir = os.path.dirname(
    os.path.abspath(__file__)
)  # chemin actuel qui doit absuluement être le dossier de travail "travail"
librairies_path = os.path.join(current_dir, "..", "Librairies")
sys.path.append(librairies_path)
from alimentation_table_mysql import alimentation_donnee  # noqa: E402
from model_indicators_base import Investments_PBE, Investments_GARE  # noqa: E402

load_dotenv()
db_url = os.getenv("DATABASE_URL1")
db_url2 = os.getenv("DATABASE_URL2")

engine = create_engine(db_url)

data = pd.read_sql_table('investment', con=engine)

# premier table d'indicateur



data[["Solar_energy", "Wind_energy", "Hydropower", "Geothermal_energy", "Bioenergy", "Marine_energy"]] = data[["Solar_energy", "Wind_energy", "Hydropower", "Geothermal_energy", "Bioenergy", "Marine_energy"]].div(data["total_renewable_energy"], axis=0) * 100
data=data.round(2)
#peut etre supprimer la colonne total_rene... qui ne serai finalement pas utile pour réaliser les graphiques


alimentation_donnee(Investments_PBE,data,db_url2)


# second indicateur

data2 = pd.read_sql_table('investment', con=engine)
data2['Investment_Growth'] = data2['total_renewable_energy'].pct_change() * 100
col_sup = [ 'Wind_energy', 'Solar_energy', 'Hydropower', 'Geothermal_energy',
       'Marine_energy', 'Bioenergy','total_renewable_energy']
data2=data2.drop(columns=col_sup)
data2=data2.dropna()


alimentation_donnee(Investments_GARE,data2,db_url2)