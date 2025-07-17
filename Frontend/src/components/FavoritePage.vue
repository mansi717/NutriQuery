<template>
  <div class="favorite-page">
    <div v-if="likedRecipes.length === 0" class="no-favorites">
        <p class="message-title">😢 No Favorites Yet!</p>
        <p class="message-subtitle">Go like some delicious dishes and they’ll show up here 🍽️</p>
    </div>

    <div v-else class="grid">
      <div class="card" v-for="recipe in likedRecipes" :key="recipe.name">
        <img :src="recipe.image" :alt="recipe.name" class="image" />
        <p class="recipe-name">{{ recipe.name }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { recipes } from '@/store/recipes.js'

const likedRecipes = computed(() =>
  recipes.filter(recipe => recipe.liked)
)
</script>

<style scoped>
.favorite-page {
  padding: 20px;
}

.no-favorites {
  text-align: center;
  margin-top: 60px;
  color: #555;
  font-family: 'Jua', sans-serif;
}

.message-title {
  font-size: 28px;
  font-weight: bold;
  color: #87B67A;
  margin-bottom: 10px;
}

.message-subtitle {
  font-size: 18px;
  color: #666;
}


.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 0 10px #eee;
  padding: 10px;
  text-align: center;
}

.image {
  width: 100%;
  border-radius: 10px;
  object-fit: cover;
}

.recipe-name {
  font-size: 16px;
  font-weight: bold;
  color: rgba(0, 0, 0, 0.7);
  margin-top: 10px;
  font-family: 'Jua', sans-serif;
}
</style>
