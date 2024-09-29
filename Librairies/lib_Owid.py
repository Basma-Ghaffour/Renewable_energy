import math
import pandas as pd
from typing import Dict, Set, Tuple

def table_valeur_manquante(data_ow:pd.DataFrame)-> pd.DataFrame:
    """Fonction qui nous permet d'avoir un tablau des données manquantes de chaque variable d'une base de données"""
    list_nom_variable = list(data_ow.keys())
    val_manqu = []
    perct = []
    for nom_variable in list_nom_variable:
        val_var_spe = list(getattr(data_ow, nom_variable))
        nb_val_manqu = sum(isinstance(x, float) and math.isnan(x) for x in val_var_spe)
        total_val = len(val_var_spe)
        percentage_missing = round(((nb_val_manqu / total_val) * 100),2)
        val_manqu.append(nb_val_manqu)
        perct.append(percentage_missing)
    table_res = pd.DataFrame({
        'Nom de Variable': list_nom_variable,
        'Nombre de Données Manquantes': val_manqu,
        'Pourcentage de Données Manquantes (%)': perct
    })
    return table_res


def stat_desc_pays(data:pd.DataFrame)->pd.Series:
    """Fonction qui renvoie des statistique descriptive des pays de la base de données
    qui nous ai utile pour voir chaque pays est présent combien de fois dans la base de données
    afin de déduire les observation sont présent pour un pays sur quelle période"""
    idx=data.index# prend comme valeur tous les couples d'index possible
    nb_obs_pays = idx.get_level_values('country').value_counts()#compte le nombre de fois q'un pays apparait dans la liste de couple d'index 
    descriptive_stats = nb_obs_pays.describe()#renvoie un tableau des stats descriptive de la fréquence d'observation des pays
    return descriptive_stats



def dict_pays_periode(data:pd.DataFrame):
    """fonction interne a préciser"""
    idx = data.index
    pays_annees = {} #creation d'un dictionnaire qui comprend le pays associé a une liste d'année pour lequel le pays a une observation
    for country, year in idx:
        if country not in pays_annees:
            pays_annees[country] = set()
        pays_annees[country].add(year)
    return pays_annees,idx#renvoie un index qui contiens la liste de tous les couple d'incex possible (pays avec année)
#renvoie un dictionnaire qui nous renvoie comme information la liste d'années d'observation dispo pour chaque pays



def pays_m_periode(data,num=23):    
    pays_annees,idx=dict_pays_periode(data)
    nb_obs_pays = idx.get_level_values('country').value_counts()# série qui contiens le nombre d'observation par pays
    #nous renvoie une liste des pays qui ont 23 osbervation chacun
    filtre_indice = nb_obs_pays[nb_obs_pays >= num].index.tolist()
    #sert unqiuement a tester si tout les pays ont le même nombre d'observation
    filtre_pays = {country: count for country, count in pays_annees.items() if country in filtre_indice}
    prem_list_anne = next(iter(filtre_pays.values()))#prend la liste d'années pour les premier pays de la liste des pays filtrer
    test_meme_anne = all(years == prem_list_anne for years in filtre_pays.values())# pour chacune des liste de pays associer à chaque pays test si il est identitique à la liste de pays associer au premier pays de la liste des pays filtré
    list_pays_fin=list(filtre_pays.keys())
    #pour le message d'avertissemtn t
    min_observations = nb_obs_pays[filtre_indice].min()
    max_observations = nb_obs_pays[filtre_indice].max()
    diff_observations = max_observations - min_observations
    
    if test_meme_anne:
        print("Toutes les années sont identiques pour tous les pays.")
    else:
         print(f"Attention: Les années d'observation diffèrent entre les pays. "
              f"Le nombre minimum d'observations est de {min_observations}, "
              f"le nombre maximum est de {max_observations}, "
              f"avec une différence de {diff_observations} observations.")
    return list_pays_fin,nb_obs_pays




list_region=["Africa","Africa (IRENA)","Asia","Central America and the Caribbean (IRENA)",
                "Eurasia (IRENA)", "Europe","Europe (IRENA)","European Union (27)",
                "High-income countries","Low-income countries","Lower-middle-income countries",
                "Middle East (IRENA)","North America","North America (IRENA)","Oceania (IRENA)",
                "South America","South America (IRENA)","Upper-middle-income countries",
                "World","Oceania"]

liste_continent=["Africa","Asia","Europe","North America","South America",'Oceania']

liste_international_blocs=["Africa (IRENA)","Central America and the Caribbean (IRENA)","Eurasia (IRENA)","Europe (IRENA)",
                            "European Union (27)","Middle East (IRENA)","North America (IRENA)","Oceania (IRENA)",
                            "South America (IRENA)"]

liste_economic_regroupment=["High-income countries","Low-income countries","Lower-middle-income countries",
                            "Upper-middle-income countries"]

non_national_zones = liste_continent + liste_international_blocs + liste_economic_regroupment+ ["World"]


def categorize_country(country):
    if country == 'World':
        return 'World'
    elif country not in non_national_zones:
        return 'national'
    elif country in liste_economic_regroupment:
        return 'economic_regroupment'
    elif country in liste_continent:
        return 'continent'
    elif country in liste_international_blocs:
        return 'international_bloc'
    return 'unknown'  # Assurer un retour par défaut


