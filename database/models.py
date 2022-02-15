from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from database.db import Base


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    frames = relationship('Frame', back_populates='location')


class Frame(Base):
    __tablename__ = 'frames'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)

    location_id = Column(Integer, ForeignKey('locations.id'))

    location = relationship('Location', back_populates='frames')
    boxes = relationship('Box', back_populates='frame')


class Box(Base):
    __tablename__ = 'boxes'

    id = Column(Integer, primary_key=True)
    frame_id = Column(Integer, ForeignKey('frames.id'))
    class_name = Column(String(20), nullable=False)
    confidence = Column(Float)
    x_min = Column(Float)
    y_min = Column(Float)
    x_max = Column(Float)
    y_max = Column(Float)

    frame = relationship('Frame', back_populates='boxes')


class Preference(Base):
    __tablename__ = 'preferences'

    key = Column(String(20), primary_key=True)
    value = Column(String(50), nullable=True)


PREFERENCE_FPS = 'FPS'
