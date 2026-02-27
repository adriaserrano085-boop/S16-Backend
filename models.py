from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from database import Base

class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    STAFF = "STAFF"
    JUGADOR = "JUGADOR"
    FAMILIA = "FAMILIA"

# Union table for parent-child relationships (FAMILIA to JUGADOR)
class FamilyPlayers(Base):
    __tablename__ = "family_players"
    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    player_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.JUGADOR, nullable=False)
    
    # User status for Staff validation
    is_active = Column(Boolean, default=True)
    is_pending_validation = Column(Boolean, default=True) # New records are pending by default
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    stats = relationship("PlayerStats", back_populates="player", uselist=False, cascade="all, delete-orphan")
    
    # A user can have multiple family links (e.g. a parent linked to multiple children)
    family_links = relationship(
        "User", 
        secondary="family_players",
        primaryjoin=id==FamilyPlayers.family_id,
        secondaryjoin=id==FamilyPlayers.player_id,
        backref="parents"
    )

class PlayerStats(Base):
    __tablename__ = "player_stats"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Melés
    scrums_won = Column(Integer, default=0)
    scrums_lost = Column(Integer, default=0)
    scrums_stolen = Column(Integer, default=0)
    
    # Touches
    lineouts_won = Column(Integer, default=0)
    lineouts_lost = Column(Integer, default=0)
    lineouts_stolen = Column(Integer, default=0)
    
    # Placajes (Tackles)
    tackles_made = Column(Integer, default=0)
    tackles_missed = Column(Integer, default=0)
    
    # Disciplina
    penalties_conceded = Column(Integer, default=0)
    yellow_cards = Column(Integer, default=0)
    red_cards = Column(Integer, default=0)
    
    # Anotaciones
    tries = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    penalty_goals = Column(Integer, default=0)
    drop_goals = Column(Integer, default=0)

    player = relationship("User", back_populates="stats")
