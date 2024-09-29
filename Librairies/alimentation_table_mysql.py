from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Type, Protocol
from sqlalchemy.engine.base import Engine
from sqlalchemy.sql.schema import Table
from sqlalchemy.orm import Session as SessionType
import pandas as pd


# définie suite au problème du typage de mod qui est une sous class de Base, et détermine le shéma pour une table d'une base de données
class ModelProtocol(Protocol):
    __table__: Table
    __tablename__: str
    version_id: int

#Fonctions interne
def _cree_table(mod: Type[ModelProtocol], engine: Engine) -> None:
    """La fonction prend un modèle (comme `Capacity` par exemple) et un moteur de base de données en entrée.
    Elle vérifie si la table associée existe déjà et la crée si ce n'est pas le cas.
    En cas d'échec lors de la création, elle lève une exception `ValueError` avec un message d'erreur détaillé.
    """
    try:
        mod.__table__.create(bind=engine, checkfirst=True)
        print(f"Table '{mod.__tablename__}' créée avec succès.")
    except Exception as e:
        raise ValueError(
            f"Erreur lors de la création de la table '{mod.__tablename__}': {e}"
        )


def _determine_version_id(session: SessionType, mod: Type[ModelProtocol]) -> int:
    """La fonction `_determine_version_id` détermine le numéro de version d'une table en fonction des enregistrements
    existants. Si la table est vide, elle renvoie 0 ; sinon, elle retourne le numéro de version le plus élevé, augmenté de 1.
    """
    try:
        count = session.query(mod).count()
        if count == 0:
            return 0
        else:
            # version_id = session.query(mod.version_id).distinct().scalar() pour contourner le problème de typagae qui n'arrive pas acceder a l'attribue version_id
            version_id = session.query(getattr(mod, "version_id")).distinct().scalar()
            return version_id + 1
    except (
        Exception
    ) as e:  # pour l'instant pas de raisValue error car le numéro de la version n'est vraiment utiliser
        session.rollback()
        raise ValueError(f"Erreur lors de la détermination du numéro de version : {e}")


def _validation_colonnes(mod: Type[ModelProtocol], dataframe: pd.DataFrame) -> None:
    """Vérifie si les colonnes du DataFrame correspondent aux colonnes du modèle."""
    model_columns = set(
        mod.__table__.columns.keys()
    )  # sous ensemble des nom des variable du shéma du modèle
    dataframe_columns = set(
        dataframe.columns
    )  # sous esnemble des nom des variables de la base de données en question
    if not dataframe_columns.issubset(
        model_columns
    ):  # si le nom des variables de la base de donnée en qeustion n'est pas inclue
        # dans le sous ensemble des nom des variable du schéma
        invalid_columns = dataframe_columns - model_columns  # peut être a modifier
        raise ValueError(f"Colonnes invalides dans le DataFrame : {invalid_columns}")
    print("Colonnes validées avec succès.")


def _suppression_table(
    session: SessionType, mod: Type[ModelProtocol], version: int
) -> None:
    """Supprime les données de la table si elle n'est pas vide."""
    if version != 0:
        session.query(mod).delete()
        session.commit()
        print(f"Anciennes données de la table '{mod.__tablename__}' supprimées.")


def _insertion_donnee(
    session: SessionType,
    mod: Type[ModelProtocol],
    dataframe: pd.DataFrame,
    version: int,
) -> None:
    """Fonction qui permet d'inséré les données d'une base de données dans la table de données de la base de données
    mySQL que l'on souhaite. Insère les données ligne par ligne en vérifiant que les conditions
    du shéma définie soient respecter."""
    for _, row in dataframe.iterrows():
        record_data = row.to_dict()
        record_data["version_id"] = version
        record = mod(**record_data)
        session.add(record)
    session.commit()
    print(
        f"Données insérées avec succès dans la table '{mod.__tablename__}' avec version {version}."
    )

#fonction externe
def alimentation_donnee(
    mod: Type[ModelProtocol], dataframe: pd.DataFrame, db_url: str
) -> None:
    """Fonction qui permet d'alimenter une table de données mySQL en fonction du shéma de la table en question,
    de la base de données que l'on souhaite inséré dans la table, et de l'url pour se connecter à
    la base de données mySQL que l'on souhaite alimenter."""
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    _cree_table(mod, engine)
    version = _determine_version_id(session, mod)
    try:
        _validation_colonnes(mod, dataframe)
        _suppression_table(session, mod, version)
        _insertion_donnee(session, mod, dataframe, version)
    except Exception as e:
        session.rollback()
        raise ValueError(f"Erreur lors de l'insertion des données : {e}")
    finally:
        session.close()
