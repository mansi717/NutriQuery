<template>
  <div>
    <h2 class="welcome-text">Recommended Recipes</h2>
    <div class="main-content">
      <FilterPanel />
      <div class="grid">
        <div class="card" v-for="recipe in recipes" :key="recipe.id">
          <div class="image-wrapper">
            <img :src="recipe.picture_url" :alt="recipe.name" />
          </div>
          <div class="card-content">
            <p class="recipe-name">{{ recipe.name }}</p>
            <div class="recipe-meta">
              <p class="cook-time"> ⏰ {{ recipe.cook_time }}</p>
              <button class="like-button" @click="toggleLike(recipe)">
                <span v-if="recipe.liked" class="liked-heart">❤️</span>
                <span v-else class="unliked-heart">♡</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import FilterPanel from './FilterPanel.vue';
import { useRoute } from 'vue-router';
import { computed, ref, onMounted } from 'vue';
import axios from 'axios';
import {images} from "@/store/recipes";

const route = useRoute();
const recipes = ref([]);

const filters = computed(() => ({
  calories: Number(route.query.calories),
  protein: Number(route.query.protein),
  fat: Number(route.query.fat),
  carbs: Number(route.query.carbs),
  time: route.query.time,
  diet: route.query.diet,
  ingredients: route.query.ingredients?.split(',') || []
}));

function assignRandomImages(recipes) {
  const availableImages = [...images];

  recipes.forEach(recipe => {
    if (availableImages.length === 0) {
      // If more recipes than images, restart image pool
      availableImages.push(...images);
    }

    // Pick a random index
    const randomIndex = Math.floor(Math.random() * availableImages.length);
    recipe.picture_url = availableImages[randomIndex];

    // Remove the selected image so it's not reused immediately
    availableImages.splice(randomIndex, 1);
  });

  return recipes;
}
onMounted(async () => {
  console.log("🔍 Sending filters:", filters.value);
  try {
    const response = await axios.get('http://localhost:5050/recommendations', {
      params: filters.value
    });
    recipes.value = response.data.map(r => ({ ...r, liked: false }));
    console.log(recipes.value)
    recipes.value = assignRandomImages(recipes.value);
    recipes.value.forEach(recipe => {
      console.log(recipe.picture_url);
    });
  } catch (error) {
    console.error('❌ Failed to fetch recipes:', error);
  }
});

function toggleLike(recipe) {
  recipe.liked = !recipe.liked;
  console.log(recipe.name, 'liked:', recipe.liked);
}

</script>

<style scoped>

.welcome-text {
  font-family: 'Jua', sans-serif;
  font-size: 20px;
  font-weight: 600;
  color: #A0C49D;
  margin: 16px 0 16px 32px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}


.main-content {
  display: flex;
  gap: 16px;
  padding: 0 32px 32px 32px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  width: 100%;
  box-sizing: border-box;
  flex-grow: 1;  /* Reserve height for 3 rows, adjust 250px to card height */
}

.card {
 background: white;
  padding: 8px;
  border-radius: 12px;
  box-shadow: 0 0 10px #eee;
  overflow: hidden;  /* fixed height */
}

.image-wrapper img {
  width: 100%;
  height: 230px;
  object-fit: cover;
}

.card img {
  width: 100%;
  object-fit: cover;
  border-radius: 10px;
}

.card-content {
  display: flex;
  flex-direction: column;  /* Stack vertically */
  align-items: flex-start;
  padding: 0.5rem;
}

.recipe-name {
  font-size: 16px;
  font-weight: bold;
  color: rgba(0, 0, 0, 0.7);
  margin: 0.5rem 0 0.25rem 0;
  text-align: left;
  font-family: 'Jua', sans-serif;
}

.recipe-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.cook-time {
  font-size: 0.9rem;
  color: #666;
}

.like-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 20px;
  padding: 0;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.liked-heart {
  color: red;
}

.unliked-heart {
  color: #aaa;
}
</style>
