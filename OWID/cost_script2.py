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
from model_indicators_base import Capacity_GAR  # noqa: E402


load_dotenv()
db_url = os.getenv("DATABASE_URL1")
db_url2 = os.getenv("DATABASE_URL2")

engine=create_engine(db_url)
engine2=create_engine(db_url2)

data = pd.read_sql_table('cost', con=engine)
data= data.set_index(['year', 'country','id'])

#création 1er indicateurs

#data_percentage = data.iloc[:, 0:5].div(data["total_cost"], axis=0) * 100
#data_percentage=data_percentage.reset_index()
#data_percentage=data_percentage.round(2)
#data_percentage.to_sql('cost_percentage_by_energy', con=engine2, if_exists='replace', index=False)

 
#création du 2nd indicateurs

#data_total_cost=data.reset_index()[['year', 'country','total_cost','id']]
#data_total_cost['Cost Growth (%)'] = data_total_cost['total_cost'].pct_change() * 100
#data_total_cost.to_sql('cost_growth_all_renewable_energy', con=engine2, if_exists='replace', index=False)