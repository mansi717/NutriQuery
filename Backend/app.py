from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_, func
from sqlalchemy.orm import aliased, query

from models import db, Recipes, NutriFacts, RecipeIngredients, Ingredients

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

# MySQL configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysqlpassword@localhost/nutriquery'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/recommendations')
def get_recommendations():
    print("📥 Received query params:", request.args)

    # --- Get filters ---
    max_calories = request.args.get('calories', type=float)
    max_fat = request.args.get('fat', type=float)
    max_protein = request.args.get('protein', type=float)
    max_carbs = request.args.get('carbs', type=float)
    time_limit = request.args.get('time', type=int)
    diet = request.args.get('diet')
    
    # FIX 1: Handle comma-separated string for ingredients
    ingredients_str = request.args.get('ingredients')
    ingredient_list = [ing.strip() for ing in ingredients_str.split(',')] if ingredients_str else []

    query = db.session.query(Recipes)

    # --- Nutrition filter ---
    if any([max_calories, max_fat, max_protein, max_carbs]):
        query = query.outerjoin(NutriFacts)
        filters = []
        if max_calories:
            filters.append(or_(NutriFacts.calories_kcal <= max_calories, NutriFacts.calories_kcal.is_(None)))
        if max_fat:
            filters.append(or_(NutriFacts.fat_g <= max_fat, NutriFacts.fat_g.is_(None)))
        if max_protein:
            filters.append(or_(NutriFacts.protein_g <= max_protein, NutriFacts.protein_g.is_(None)))
        if max_carbs:
            filters.append(or_(NutriFacts.carbs_g <= max_carbs, NutriFacts.carbs_g.is_(None)))
        if filters:
            query = query.filter(and_(*filters))

    # --- Cook time filter ---
    if time_limit is not None and time_limit > 0 and time_limit < 45:
        # Assuming Recipes.total_minutes is a pre-calculated integer column
        query = query.filter(Recipes.total_minutes <= time_limit)
        print(f"✅ Time filter applied: total_minutes <= {time_limit}")

    # --- Diet filter ---
    if diet:
        # Note: This logic assumes a recipe is "vegan" if none of its ingredients are non-vegan.
        # This can be complex. A subquery is often more robust here.
        subquery = db.session.query(RecipeIngredients.recipe_id)
        subquery = subquery.join(Ingredients, RecipeIngredients.ingredient_id == Ingredients.ingredient_id)
        
        if diet in ['vegan', 'vegetarian']:
            exclude = ['meat', 'chicken', 'beef', 'fish', 'pork', 'egg']
            subquery = subquery.filter(or_(*[Ingredients.name.ilike(f'%{kw}%') for kw in exclude]))
            query = query.filter(Recipes.recipe_id.notin_(subquery))
        elif diet == 'meat':
            include = ['chicken', 'pork', 'beef', 'meat']
            subquery = subquery.filter(or_(*[Ingredients.name.ilike(f'%{kw}%') for kw in include]))
            query = query.filter(Recipes.recipe_id.in_(subquery))
        elif diet == 'seafood':
            include = ['fish', 'shrimp', 'prawn', 'salmon', 'tuna']
            subquery = subquery.filter(or_(*[Ingredients.name.ilike(f'%{kw}%') for kw in include]))
            query = query.filter(Recipes.recipe_id.in_(subquery))

    # --- Ingredient search ---
    if ingredient_list:
        # For each ingredient, the recipe must contain it.
        for ingredient_name in ingredient_list:
            if not ingredient_name: continue
            # Use a subquery to find recipes containing this specific ingredient
            sq = db.session.query(RecipeIngredients.recipe_id).join(Ingredients).filter(Ingredients.name.ilike(f'%{ingredient_name}%')).subquery()
            query = query.filter(Recipes.recipe_id.in_(sq))

    # FIX 2: Execute the query only ONCE after all filters are applied
    query = query.distinct()
    
    # Print the final, complete query for debugging
    print(" النهائية Final SQL Query:")
    print(str(query.statement.compile(compile_kwargs={"literal_binds": True})))

    recipes = query.limit(10).all()

    # --- Format result ---
    response_data = [{
        'id': r.recipe_id,
        'name': r.name,
        'cook_time': r.cook_time,
        'picture_url': r.picture_url,
        'directions': r.directions
    } for r in recipes]

    print(f"📤 Sending {len(response_data)} recipes.")
    return jsonify(response_data)

def build_time_in_minutes():
    # Convert 'cook_time' VARCHAR to total minutes
    hours = func.ifnull(
        func.regexp_substr(Recipes.cook_time, r'(\d+)\s*hour'),
        0
    )
    minutes = func.ifnull(
        func.regexp_substr(Recipes.cook_time, r'(\d+)\s*minute'),
        0
    )
    return (
        func.cast(hours, db.Integer) * 60 +
        func.cast(minutes, db.Integer)
    )

# ✅ This must come last
if __name__ == '__main__':
    app.run(debug=True, port=5050)
