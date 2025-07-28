<template>
  <div class="recommendation-wrapper">
    <h2>Recommended Recipes</h2>

    <div class="grid">
      <p v-if="recipes.length === 0" class="empty-msg">No recipes to display.</p>

      <div class="card" v-for="recipe in recipes" :key="recipe.id">
        <!-- <div class="image-wrapper">
          <img :src="recipe.picture_url" :alt="recipe.name" />
        </div> -->
        <div class="card-content">
          <p class="recipe-name">{{ recipe.name }}</p>
          <p class="cook-time">Cook Time: {{ recipe.cook_time || 'N/A' }}</p>
          <button class="like-btn" @click="toggleLike(recipe)">
            {{ recipe.liked ? '❤️ Liked' : '🤍 Like' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'

// Dummy list of fallback images
// const images = [
//   "https://via.placeholder.com/300x200?text=Recipe+1",
//   "https://via.placeholder.com/300x200?text=Recipe+2",
//   "https://via.placeholder.com/300x200?text=Recipe+3",
//   "https://via.placeholder.com/300x200?text=Recipe+4"
// ]

const filters = ref({
  max_calories: 500,
  max_cook_time: 30,
  diet: "vegetarian",
  include_ingredients: ["cabbage", "yogurt"]
})

const recipes = ref([])

onMounted(async () => {
  console.log("📤 Sending filters:", filters.value)
  try {
    const response = await axios.get('http://localhost:5050/recommendations', {
      params: filters.value
    })
    console.log("📥 Received recipes:", response.data)

    const recipeData = response.data.map(r => ({ ...r, liked: false }))
    // assignRandomImages(recipeData)
    recipes.value = recipeData
  } catch (error) {
    console.error("❌ API fetch failed:", error)
  }
})

// function assignRandomImages(recipes) {
//   const availableImages = [...images]
//   recipes.forEach(recipe => {
//     if (availableImages.length === 0) availableImages.push(...images)
//     const randomIndex = Math.floor(Math.random() * availableImages.length)
//     recipe.picture_url = availableImages[randomIndex]
//     availableImages.splice(randomIndex, 1)
//   })
// }

function toggleLike(recipe) {
  recipe.liked = !recipe.liked
}
</script>

<style scoped>
.recommendation-wrapper {
  padding: 1rem;
}

h2 {
  text-align: center;
  margin-bottom: 1rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.5rem;
}

.card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-5px);
}

.image-wrapper {
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-content {
  padding: 1rem;
  text-align: center;
}

.recipe-name {
  font-size: 1.1rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.cook-time {
  color: #555;
  margin-bottom: 0.5rem;
}

.like-btn {
  background-color: transparent;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
}

.empty-msg {
  color: red;
  font-size: 1.1rem;
  grid-column: 1 / -1;
  text-align: center;
}
</style>
