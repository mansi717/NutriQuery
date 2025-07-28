from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_, func
from sqlalchemy.orm import aliased, query
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, Recipes, NutriFacts, RecipeIngredients, Ingredients, Users, UserPreferences

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

# MySQL configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysqlpassword@localhost/nutriquery'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if Users.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 409

    hashed_pw = generate_password_hash(password)
    new_user = Users(name=name, email=email, password_hash=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': 'User created successfully',
        'username': name,
        'user_id': new_user.user_id  # ← add this
    }), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = Users.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login successful', 'username': user.name, 'user_id': user.user_id}), 200

@app.route('/recommendations')  # ✅ this must be here
def get_recommendations():

    print("📥 Received query params:")

    # --- Get filters ---
    max_calories = request.args.get('calories', type=float)
    max_fat = request.args.get('fat', type=float)
    max_protein = request.args.get('protein', type=float)
    max_carbs = request.args.get('carbs', type=float)
    time_limit = request.args.get('time', type=int)
    diet = request.args.get('diet')
    ingredients_raw = request.args.get('ingredients')
    ingredient_list = ingredients_raw.split(',') if ingredients_raw else []
    query = db.session.query(Recipes)

    # --- Nutrition filter ---
    if any([max_calories, max_fat, max_protein, max_carbs]):
        query = query.outerjoin(NutriFacts)
        filters = []
        if max_calories:
            filters.append(or_(NutriFacts.calories_kcal <= max_calories, NutriFacts.calories_kcal == None))
        if max_fat:
            filters.append(or_(NutriFacts.fat_g <= max_fat, NutriFacts.fat_g == None))
        if max_protein:
            filters.append(or_(NutriFacts.protein_g <= max_protein, NutriFacts.protein_g == None))
        if max_carbs:
            filters.append(or_(NutriFacts.carbs_g <= max_carbs, NutriFacts.carbs_g == None))
        query = query.filter(and_(*filters))

    print(f"Selected time_limit filter: {time_limit} (type: {type(time_limit)})")
    print(f"👉 After nutrition filter: {query.count()}")

    # --- Cook time filter ---
    if time_limit is not None and time_limit < 45:
        query = query.filter(Recipes.total_minutes <= time_limit)
        print(f"✅ Time filter applied: total_minutes <= {time_limit}")
    else:
        print("⏰ No time limit applied — showing all recipeResults.")

    recipes = query.distinct().limit(10).all()
    print(str(query.statement.compile(compile_kwargs={"literal_binds": True})))
    print(f"👉 After time filter: {query.count()}")
    # --- Diet filter ---
    # --- Diet Filter ---
    if diet:
        diet_ri = aliased(RecipeIngredients)  # alias 1
        diet_ing = aliased(Ingredients)  # alias 2
        query = query.join(diet_ri, Recipes.recipe_id == diet_ri.recipe_id)
        query = query.join(diet_ing, diet_ri.ingredient_id == diet_ing.ingredient_id)

        if diet in ['vegan', 'vegetarian']:
            exclude = ['meat', 'chicken', 'beef', 'fish', 'pork', 'egg']
            for kw in exclude:
                query = query.filter(~diet_ing.name.ilike(f'%{kw}%'))
        elif diet == 'meat':
            query = query.filter(
                or_(
                    diet_ing.name.ilike('%chicken%'),
                    diet_ing.name.ilike('%pork%'),
                    diet_ing.name.ilike('%beef%'),
                    diet_ing.name.ilike('%meat%')
                )
            )
        elif diet == 'seafood':
            query = query.filter(
                or_(
                    diet_ing.name.ilike('%fish%'),
                    diet_ing.name.ilike('%shrimp%'),
                    diet_ing.name.ilike('%prawn%')
                )
            )
    print(f"👉 After diet filter: {query.count()}")
    # --- Ingredient search ---
    if ingredient_list:
        ing_ri = aliased(RecipeIngredients)  # alias 3
        ing_ing = aliased(Ingredients)  # alias 4
        query = query.join(ing_ri, Recipes.recipe_id == ing_ri.recipe_id)
        query = query.join(ing_ing, ing_ri.ingredient_id == ing_ing.ingredient_id)

        query = query.filter(
            or_(*[ing_ing.name.ilike(f'%{ing}%') for ing in ingredient_list])
        )

    recipes = query.distinct().limit(10).all()

    # --- Format result ---
    response_data = []

    for r in recipes:
        # Query ingredients for this recipe
        ingredient_names = db.session.query(Ingredients.name) \
            .join(RecipeIngredients, Ingredients.ingredient_id == RecipeIngredients.ingredient_id) \
            .filter(RecipeIngredients.recipe_id == r.recipe_id) \
            .all()

        ingredient_list = [name for (name,) in ingredient_names]

        response_data.append({
            'id': r.recipe_id,
            'name': r.name,
            'cook_time': r.cook_time,
            'picture_url': r.picture_url,
            'directions': r.directions,
            'ingredients': ingredient_list  # ✅ added
        })

    print("📤 Sending recipeResults:", response_data)

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

@app.route('/api/user/like', methods=['POST'])
def like_recipe():
    data = request.get_json()
    user_id = data['user_id']
    recipe_id = data['recipe_id']
    liked = data['liked']

    pref = UserPreferences.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()

    if liked:
        if not pref:
            new_pref = UserPreferences(user_id=user_id, recipe_id=recipe_id, liked_status=1)
            db.session.add(new_pref)
        else:
            pref.liked_status = 1
    else:
        if pref:
            pref.liked_status = 0  # soft delete (or db.session.delete(pref) if you want hard delete)

    db.session.commit()
    return jsonify({'status': 'success'})


# ✅ This must come last
if __name__ == '__main__':
    app.run(debug=True, port=5050)
