# movies.py
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.orm import declarative_base
from typing import Dict, Any

Base = declarative_base()


class MovieDBModel(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)  # int в БД
    name = Column(String)  # text в БД
    price = Column(Integer)  # int в БД
    description = Column(String)  # text в БД
    image_url = Column(String)  # text в БД
    location = Column(String)  # text в БД
    published = Column(Boolean)  # bool в БД
    genre_id = Column(Integer)  # int в БД
    created_at = Column(DateTime)  # timestamp в БД
    rating = Column(Integer)  # int в БД

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь"""
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'image_url': self.image_url,
            'location': self.location,
            'published': self.published,
            'genre_id': self.genre_id,
            'created_at': self.created_at,
            'rating': self.rating
        }

    def __repr__(self):
        return f"<Movie(id='{self.id}', name='{self.name}')>"
