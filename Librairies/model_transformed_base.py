from sqlalchemy import Column, String, Float, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()


class Capacity(Base):
    __tablename__ = "capacity"
    id = Column(String(255), primary_key=True)
    country = Column(String(255), nullable=False)
    zone_type = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    total_renewable_energy = Column(Float)
    version_id = Column(Integer, nullable=False)  # nv
    version_date = Column(DateTime, default=datetime.now)  # nv


# PrimaryKeyConstraint('id', 'version_id'),
# Ajouter des contraintes d'unicité ou d'index si nécessaire
# UniqueConstraint('id', 'version_id', name='_id_version_uc') )


class Investments(Base):
    __tablename__ = "investment"
    id = Column(String(255), primary_key=True)
    country = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    zone_type = Column(String(255), nullable=False)
    version_id = Column(Integer, nullable=False)  # nv
    version_date = Column(DateTime, default=datetime.now)  # nv
    Wind_energy = Column(Float)
    Solar_energy = Column(Float)
    Hydropower = Column(Float)
    Geothermal_energy = Column(Float)
    Marine_energy = Column(Float)
    Bioenergy = Column(Float)
    total_renewable_energy = Column(Float)


class Cost(Base):
    __tablename__ = "cost"
    id = Column(String(255), primary_key=True)
    country = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    zone_type = Column(String(255), nullable=False)
    version_id = Column(Integer, nullable=False)  # nv
    version_date = Column(DateTime, default=datetime.now)  # nv
    Bioenergy = Column(Float)
    Geothermal_energy = Column(Float)
    Hydropower = Column(Float)
    Wind_energy = Column(Float)
    Solar_energy = Column(Float)
    total_cost = Column(Float)


class Patents(Base):
    __tablename__ = "patents"
    id = Column(String(255), primary_key=True)
    country = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    zone_type = Column(String(255), nullable=False)
    version_id = Column(Integer, nullable=False)  # nv
    version_date = Column(DateTime, default=datetime.now)  # nv
    Wind_energy = Column(Integer)
    Solar_energy = Column(Integer)
    Hydropower = Column(Integer)
    Geothermal_energy = Column(Integer)
    Marine_energy = Column(Integer)
    Bioenergy = Column(Integer)
    Enabling_Technologies = Column(Integer)
    total_patents = Column(Integer)
