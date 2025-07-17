<template>
  <div class="filter-panel">
    <h2 class="title-main">find your meal!</h2>

    <div class="section">
      <p class="section-title">Nutrition Goals</p>
      <div class="slider-group">
        <label>Calories (kcal)</label>
        <input type="range" min="200" max="1000" step="200" v-model="filters.calories" :style="caloriesSliderStyle" />
        <div class="slider-values">
          <span>200</span><span>400</span><span>600</span><span>800</span><span>1000</span>
        </div>

        <label>Fat (g)</label>
        <input type="range" min="10" max="50" step="10" v-model="filters.fat" :style="fatSliderStyle" />
        <div class="slider-values">
          <span>10</span><span>20</span><span>30</span><span>40</span><span>50</span>
        </div>

        <label>Protein (g)</label>
        <input type="range" min="10" max="50" step="10" v-model="filters.protein" :style="proteinSliderStyle" />
        <div class="slider-values">
          <span>10</span><span>20</span><span>30</span><span>40</span><span>50</span>
        </div>

        <label>Carbs (g)</label>
        <input type="range" min="20" max="100" step="20" v-model="filters.carbs" :style="carbsSliderStyle" />
        <div class="slider-values">
          <span>20</span><span>40</span><span>60</span><span>80</span><span>100</span>
        </div>
      </div>
    </div>

    <div class="section">
      <p class="section-title">Ready In</p>
      <div class="radio-grid">
        <label><input type="radio" name="time" value="10" v-model="filters.time" /> Under 10 minutes</label>
        <label><input type="radio" name="time" value="20" v-model="filters.time" /> Under 20 minutes</label>
        <label><input type="radio" name="time" value="30" v-model="filters.time" /> Under 30 minutes</label>
        <label><input type="radio" name="time" value="45" v-model="filters.time" /> Anytime</label>
      </div>
    </div>

    <div class="section dietary">
      <p class="section-title">Dietary Preferences</p>
      <div class="radio-grid">
        <label><input type="radio" name="diet" value="vegan" v-model="filters.diet" /> Vegan</label>
        <label><input type="radio" name="diet" value="meat" v-model="filters.diet" /> Meat</label>
        <label><input type="radio" name="diet" value="vegetarian" v-model="filters.diet" /> Vegetarian</label>
        <label><input type="radio" name="diet" value="seafood" v-model="filters.diet" /> Seafood</label>
      </div>
    </div>

    <div class="section">
      <label class="main-ingredients-label">Main Ingredients</label>
      <div class="search-input-container">
        <span class="search-icon">🔍</span>
        <input
          type="text"
          placeholder="Chicken"
          v-model="ingredientSearch"
          @input="filterSuggestions"
        />
      </div>

      <div class="ingredient-suggestions">
        <span
          v-for="suggestion in filteredSuggestions"
          :key="suggestion"
          class="ingredient-pill light-green"
          @click="addIngredient(suggestion)"
        >
          {{ suggestion }}
        </span>
      </div>

      <div class="selected-ingredients-section">
        <label class="selected-label">Selected :</label>
        <div class="selected-pills-container">
          <span
            v-for="ingredient in selectedIngredients"
            :key="ingredient"
            class="ingredient-pill dark-green"
            @click="removeIngredient(ingredient)"
          >
            {{ ingredient }}
          </span>
        </div>
      </div>
    </div>

    <button class="surprise-me-button" @click="goToRecommendations">Surprise Me</button>
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const filters = reactive({
  calories: 600,
  protein: 30,
  fat: 20,
  carbs: 60,
  time: '',      
  diet: ''       
});


// These generate the CSS variable string for each slider
const caloriesSliderStyle = computed(() => {
  const min = 200;
  const max = 1000;
  const progress = ((filters.calories - min) / (max - min)) * 100;
  return `--range-progress: ${progress}%;`;
});

const fatSliderStyle = computed(() => {
  const min = 10;
  const max = 50;
  const progress = ((filters.fat - min) / (max - min)) * 100;
  return `--range-progress: ${progress}%;`;
});

const proteinSliderStyle = computed(() => {
  const min = 10;
  const max = 50;
  const progress = ((filters.protein - min) / (max - min)) * 100;
  return `--range-progress: ${progress}%;`;
});

const carbsSliderStyle = computed(() => {
  const min = 20;
  const max = 100;
  const progress = ((filters.carbs - min) / (max - min)) * 100;
  return `--range-progress: ${progress}%;`;
});


const ingredientSearch = ref('');
const allSuggestions = ref(['Chicken breast', 'Chicken wings', 'Chicken', 'Beef', 'Pork', 'Fish', 'Tofu', 'Rice', 'Pasta']); // Example suggestions
const selectedIngredients = ref(['Cheese', 'Spinach', 'Garlic']); // Example selected ingredients

const filteredSuggestions = computed(() => {
  if (!ingredientSearch.value) {
    // Show top 3 or a few common ones if search is empty, or none
    return allSuggestions.value.filter(suggestion =>
      !selectedIngredients.value.includes(suggestion)
    ).slice(0, 3); // Limit to top 3 not already selected
  }
  return allSuggestions.value.filter(suggestion =>
    suggestion.toLowerCase().includes(ingredientSearch.value.toLowerCase()) &&
    !selectedIngredients.value.includes(suggestion) // Don't suggest already selected
  ).slice(0, 5); // Limit suggestions shown
});

function addIngredient(ingredient) {
  if (!selectedIngredients.value.includes(ingredient)) {
    selectedIngredients.value.push(ingredient);
    ingredientSearch.value = ''; // Clear search after adding
  }
}

function removeIngredient(ingredient) {
  selectedIngredients.value = selectedIngredients.value.filter(item => item !== ingredient);
}
function goToRecommendations() {
  const query = {
    calories: filters.calories,
    protein: filters.protein,
    fat: filters.fat,
    carbs: filters.carbs,
    time: filters.time,
    diet: filters.diet,
    ingredients: selectedIngredients.value.join(',') 
  };

  router.push({ name: 'recommendations', query });
}


function filterSuggestions() {
  // This computed property handles the filtering based on ingredientSearch.value
}
</script>

<style scoped>
/* Import Google Font - Jua */
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

.filter-panel {
  /* Fix 1: Set fixed width and prevent stretching/shrinking */
  width: 300px; 
  flex-shrink: 0; 
  align-self: flex-start; 
  padding-left: 28px;
  padding-right: 16px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 0 10px #eee;
  box-sizing: border-box; 
  padding-bottom: 20px;
}

.title-main {
  font-size: 24px;
  color: rgba(0, 0, 0, 0.7);
  padding-top: 20px;
  font-family: 'Jua', sans-serif;
  margin-bottom: 0;
}

.section {
  margin-top: 33px;
  margin-bottom: 0px; 
}

.section-title {
  font-size: 16px;
  color: rgba(0, 0, 0, 0.7);
  margin-bottom: 10px;
  font-family: 'Jua', sans-serif;
}

.slider-group label {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.7);
  display: block;
  margin-top: 10px;
  font-family: 'Jua', sans-serif;
}

input[type="range"] {
  width: 200px;
  height: 6px; 
  -webkit-appearance: none;
  background: transparent; 
  border-radius: 2px;
  outline: none;
  margin-top: 4px;
}

/* Fix 3: Slider track coloring */
input[type="range"]::-webkit-slider-runnable-track {
  width: 100%;
  height: 6px; 
  /* Use CSS variable for dynamic progress. Default 0% */
  background: linear-gradient(to right, #A0C49D var(--range-progress, 0%), #F7FFE5 var(--range-progress, 0%));
  border-radius: 2px;
  cursor: pointer;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 14px;
  height: 14px;
  background: #A0C49D;
  border-radius: 50%;
  cursor: pointer;
  margin-top: -4px; 
}

/* Hide values for specific sliders, if not already handled or needed */
.slider-values {
  display: flex;
  justify-content: space-between;
  width: 200px; 
  font-size: 10px;
  color: rgba(0, 0, 0, 0.7);
  margin-top: 2px;
}

.radio-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.radio-grid input[type="radio"] {
  width: 16px;
  height: 16px;
  -webkit-appearance: none; /* For Safari/Chrome */
  -moz-appearance: none; /* For Firefox */
  appearance: none;
  background-color: #F7FFE5; 
  border-radius: 50%;
  border: 1px solid #A0C49D; 
  position: relative;
  cursor: pointer;
  outline: none; 
}

.radio-grid input[type="radio"]:checked {
  background-color: #A0C49D; 
  border-color: #A0C49D; 
}

.radio-grid label {
  display: flex;
  align-items: center;
  font-size: 12px;
  color: rgba(0, 0, 0, 0.7);
  font-family: 'Jua', sans-serif;
  gap: 6px; 
}

/* --- Main Ingredient Section Styles (Integrated) --- */
.main-ingredients-label {
  display: block; 
  margin-bottom: 10px;
  font-weight: bold; 
  font-size: 16px; 
  color: rgba(0, 0, 0, 0.7);
  font-family: 'Jua', sans-serif;
}

.search-input-container {
  position: relative;
  margin-bottom: 15px;
  width: 200px; 
}

.search-input-container input {
  width: 100%; 
  padding: 10px 15px 10px 40px; 
  border: none;
  border-radius: 10px;
  background-color: #F7FFE5; 
  font-size: 14px; 
  outline: none; 
  color: #333;
  font-family: 'Jua', sans-serif; 
}

.search-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #888; 
  font-size: 16px; 
}

.ingredient-suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 20px; 
  padding: 10px; 
  background-color: #F7FFE5; 
  border-radius: 10px;
  min-height: 40px; 
  width: 100%;  
  box-sizing: border-box; 
}

.selected-ingredients-section {
  display: flex;
  align-items: flex-start; 
  flex-wrap: wrap;
  margin-top: 10px; 
  width: 200px; 
  box-sizing: border-box; 
}

.selected-ingredients-section .selected-label {
  font-weight: bold;
  margin-right: 10px; 
  font-size: 12px; 
  color: rgba(0, 0, 0, 0.7);
  font-family: 'Jua', sans-serif;
  white-space: nowrap; 
  margin-top: 8px; 
}

.selected-pills-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  flex-grow: 1; 
}

.ingredient-pill {
  padding: 8px 15px;
  border-radius: 20px; 
  font-size: 12px; 
  cursor: pointer;
  transition: background-color 0.2s ease;
  white-space: nowrap; 
  font-family: 'Jua', sans-serif; 
}

.ingredient-pill:hover {
  opacity: 0.8;
}

.light-green {
  background-color: #F7FFE5; 
  color: rgba(0, 0, 0, 0.7); 
  border: 1px solid #A0C49D; 
}

.dark-green {
  background-color: #A0C49D; 
  color: white;
}

/* Surprise Me Button */
.surprise-me-button {
  background-color: rgba(0, 0, 0, 0.7); 
  color: white;
  padding: 10px 20px; 
  border: none;
  border-radius: 10px; 
  width: 100%; 
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s ease;
  margin-top: 30px; 
  font-family: 'Jua', sans-serif; 
}

.surprise-me-button:hover {
  background-color: rgba(0, 0, 0, 0.8);
}
</style>