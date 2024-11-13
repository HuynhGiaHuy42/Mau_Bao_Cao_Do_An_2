# models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ChuyenNganh(Base):
    __tablename__ = 'ChuyenNganhs'
    ChuyenNganhID = Column(String(20), primary_key=True)
    TenChuyenNganh = Column(String(100), nullable=False)
    
    sinh_viens = relationship("SinhVien", back_populates="chuyen_nganh")

class SinhVien(Base):
    __tablename__ = 'SinhViens'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    Ten = Column(String(100), nullable=False)
    Tuoi = Column(Integer, nullable=False)
    GioiTinh = Column(Boolean, nullable=False)
    ChuyenNganhID = Column(String(20), ForeignKey('ChuyenNganhs.ChuyenNganhID'), nullable=False)
    
    chuyen_nganh = relationship("ChuyenNganh", back_populates="sinh_viens")

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)