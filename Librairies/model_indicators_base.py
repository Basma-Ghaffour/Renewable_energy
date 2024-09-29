from sqlalchemy import Column, String, Float, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()


class Capacity_GAR(Base):
    __tablename__ = "capcity_growth_all_renewable_energy"
    id = Column(String(255), primary_key=True)
    country = Column(String(255), nullable=False)
    zone_type = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    total_renewable_energy = Column(Float)
    Capacity_Growth = Column(Float, nullable=True)
    version_id = Column(Integer, nullable=False)  # nv
    version_date = Column(DateTime, default=datetime.now)  # nv


class Investments_PBE(Base):
    __tablename__ = "investments_percentage_by_energy"
    id = Column(String(255), primary_key=True)
    country = Column(String(255), nullable=False)
    zone_type = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    version_id = Column(Integer, nullable=False)  # nv
    version_date = Column(DateTime, default=datetime.now)  # nv
    Wind_energy = Column(Float)
    Solar_energy = Column(Float)
    Hydropower = Column(Float)
    Geothermal_energy = Column(Float)
    Marine_energy = Column(Float)
    Bioenergy = Column(Float)
    total_renewable_energy = Column(Float)


class Investments_GARE(Base):
    __tablename__ = "investments_growth_all_renewable_energy"
    id = Column(String(255), primary_key=True)
    country = Column(String(255), nullable=False)
    zone_type = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    version_id = Column(Integer, nullable=False)  # nv
    version_date = Column(DateTime, default=datetime.now)  # nv
    Investment_Growth = Column(Float, nullable=True)


class Patents_PBE(Base):
    __tablename__ = "patents_percentage_by_energy"
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
    Enabling_Technologies = Column(Float)


class Patents_GARE(Base):
    __tablename__ = "patents_growth_all_renewable_energy"
    id = Column(String(255), primary_key=True)
    country = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    zone_type = Column(String(255), nullable=False)
    version_id = Column(Integer, nullable=False)  # nv
    version_date = Column(DateTime, default=datetime.now)  # nv
    total_patents_growth = Column(Float)
