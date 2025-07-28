<template>
  <div class="favorite-page">
    <div v-if="favoritesStore.favorites.length === 0" class="no-favorites">
      <p class="message-title">😢 No Favorites Yet!</p>
      <p class="message-subtitle">Go like some delicious dishes and they’ll show up here 🍽️</p>
    </div>

    <div v-else class="grid">
      <div class="card" v-for="recipe in favoritesStore.favorites" :key="recipe.id">
        <div class="image-wrapper">
          <img :src="recipe.picture_url" :alt="recipe.name" />
        </div>
        <div class="card-content">
          <p class="recipe-name">{{ recipe.name }}</p>
          <div class="recipe-meta">
            <p class="cook-time"> ⏰ {{ recipe.cook_time }}</p>
            <button class="like-button" @click="toggleFavorite(recipe)">
              <span v-if="recipe.liked" class="liked-heart">❤️</span>
              <span v-else class="unliked-heart">♡</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { favoritesStore } from '@/store/favorite'; // Adjust path if necessary

const likedRecipes = ref([]);
// Removed userId local variable as it's not directly used here after store.loadFavorites()

function toggleFavorite(recipe) {
  favoritesStore.toggleFavorite(recipe);
}
onMounted(async () => {
  await favoritesStore.loadFavorites(); // Load favorites into the store
  likedRecipes.value = favoritesStore.favorites; // Sync local ref with store's favorites
});
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
