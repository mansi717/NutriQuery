from typing import List, Optional

from sqlalchemy import Date, Float, ForeignKeyConstraint, Index, Integer, String, Text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Base(DeclarativeBase):
    pass


class Ingredients(db.Model):
    __tablename__ = 'ingredients'

    ingredient_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    recipe_ingredients: Mapped[List['RecipeIngredients']] = relationship('RecipeIngredients', back_populates='ingredient')


class Recipes(db.Model):
    __tablename__ = 'recipes'

    recipe_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    directions: Mapped[Optional[str]] = mapped_column(Text)
    cook_time: Mapped[Optional[str]] = mapped_column(String(100))
    picture_url: Mapped[Optional[str]] = mapped_column(String(500))
    last_scraped_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    total_minutes: Mapped[Optional[int]] = mapped_column(Integer)

    nutri_facts: Mapped[List['NutriFacts']] = relationship('NutriFacts', back_populates='recipe')
    recipe_ingredients: Mapped[List['RecipeIngredients']] = relationship('RecipeIngredients', back_populates='recipe')
    user_preferences: Mapped[List['UserPreferences']] = relationship('UserPreferences', back_populates='recipe')


class Users(db.Model):
    __tablename__ = 'users'
    __table_args__ = (
        Index('email', 'email', unique=True),
    )

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255))
    password_hash: Mapped[str] = mapped_column(String(255))

    user_preferences: Mapped[List['UserPreferences']] = relationship('UserPreferences', back_populates='user')


class NutriFacts(db.Model):
    __tablename__ = 'nutri_facts'
    __table_args__ = (
        ForeignKeyConstraint(['recipe_id'], ['recipes.recipe_id'], ondelete='CASCADE', name='nutri_facts_ibfk_1'),
        Index('recipe_id', 'recipe_id')
    )

    nutri_fact_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recipe_id: Mapped[Optional[int]] = mapped_column(Integer)
    calories_kcal: Mapped[Optional[float]] = mapped_column(Float)
    fat_g: Mapped[Optional[float]] = mapped_column(Float)
    carbs_g: Mapped[Optional[float]] = mapped_column(Float)
    protein_g: Mapped[Optional[float]] = mapped_column(Float)
    sugar_g: Mapped[Optional[float]] = mapped_column(Float)

    recipe: Mapped[Optional['Recipes']] = relationship('Recipes', back_populates='nutri_facts')


class RecipeIngredients(db.Model):
    __tablename__ = 'recipe_ingredients'
    __table_args__ = (
        ForeignKeyConstraint(['ingredient_id'], ['ingredients.ingredient_id'], ondelete='CASCADE', name='recipe_ingredients_ibfk_2'),
        ForeignKeyConstraint(['recipe_id'], ['recipes.recipe_id'], ondelete='CASCADE', name='recipe_ingredients_ibfk_1'),
        Index('ingredient_id', 'ingredient_id')
    )

    recipe_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ingredient_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    amount: Mapped[Optional[str]] = mapped_column(String(100))

    ingredient: Mapped['Ingredients'] = relationship('Ingredients', back_populates='recipe_ingredients')
    recipe: Mapped['Recipes'] = relationship('Recipes', back_populates='recipe_ingredients')


class UserPreferences(db.Model):
    __tablename__ = 'user_preferences'
    __table_args__ = (
        ForeignKeyConstraint(['recipe_id'], ['recipes.recipe_id'], ondelete='CASCADE', name='user_preferences_ibfk_1'),
        ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE', name='fk_user_pref_user'),
        Index('fk_user_pref_user', 'user_id'),
        Index('recipe_id', 'recipe_id')
    )

    preference_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    recipe_id: Mapped[Optional[int]] = mapped_column(Integer)
    liked_status: Mapped[Optional[int]] = mapped_column(TINYINT(1))
    user_id: Mapped[Optional[int]] = mapped_column(Integer)

    recipe: Mapped[Optional['Recipes']] = relationship('Recipes', back_populates='user_preferences')
    user: Mapped[Optional['Users']] = relationship('Users', back_populates='user_preferences')
