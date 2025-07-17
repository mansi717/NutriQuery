from sqlalchemy.exc import IntegrityError


def insert_recipe_from_xml(xml_file_path):
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    import xml.etree.ElementTree as ET
    from models import db, Users, Recipes, Ingredients, RecipeIngredients, NutriFacts, UserPreferences
    from app import app

    with app.app_context():
        try:
            tree = ET.parse('recipe.xml')
            root = tree.getroot()
            recipe = root

            # Basic info
            name = recipe.find('recipe_name').text
            directions_elem = recipe.find('directions')
            directions = "\n".join([d.text.strip() for d in directions_elem.findall('direction') if d.text]) if directions_elem else None
            cook_time = recipe.find('time').text
            picture_url = recipe.find('url').text
            last_scraped_date = recipe.find('scraped_time').text

            # Create Recipe object
            new_recipe = Recipes(
                name=name,
                directions=directions,
                cook_time=cook_time,
                picture_url=picture_url,
                last_scraped_date=last_scraped_date
            )
            db.session.add(new_recipe)
            db.session.flush()  # get new_recipe.id without committing

            # Ingredients
            for item in recipe.find('ingredients').findall('ingredient'):
                ingredient_name = item.find('name').text.strip()
                amount_elem = item.find('amount')
                amount = amount_elem.text.strip() if amount_elem is not None and amount_elem.text else None

                # Find or create Ingredient
                ingredient = Ingredients.query.filter_by(name=ingredient_name).first()
                if not ingredient:
                    try:
                        ingredient = Ingredients(name=ingredient_name)
                        db.session.add(ingredient)
                        db.session.flush()
                    except IntegrityError:
                        db.session.rollback()
                        # Another insert in the same session might have added it; fetch again
                        ingredient = Ingredients.query.filter_by(name=ingredient_name).first()
                        if not ingredient:
                            raise  # Something else went wrong

                # Link recipe and ingredient
                recipe_ingredient = RecipeIngredients(
                    recipe_id=new_recipe.recipe_id,
                    ingredient_id=ingredient.ingredient_id,
                    amount=amount
                )
                db.session.add(recipe_ingredient)


            def extract_number(text):
                if text:
                    return float(''.join(c for c in text if c.isdigit() or c == '.'))
                return None

            # Nutrition facts
            nutri = recipe.find('nutrition_facts_per_serving')
            if nutri is not None:
                nutrition = NutriFacts(
                    recipe_id=new_recipe.recipe_id,
                    calories_kcal=extract_number(nutri.findtext('calories')),
                    fat_g=extract_number(nutri.findtext('fat')),
                    carbs_g=extract_number(nutri.findtext('carbs')),
                    protein_g=extract_number(nutri.findtext('protein')),
                    sugar_g=extract_number(nutri.findtext('sugar'))
                )
                db.session.add(nutrition)

            db.session.commit()
            print("✅ All recipe data successfully inserted using SQLAlchemy.")

        except IntegrityError as e:
            db.session.rollback()
            print(f"⚠️ Skipped recipe due to integrity error (likely duplicate): {e}")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Skipped recipe due to unexpected error: {e}")