<template>
  <RecipeDetail
    v-if="selectedRecipe"
    :recipe="selectedRecipe"
    @close-detail="selectedRecipe = null"
  />

  <div v-else-if="recommendations.length === 0" class="no-favorites">
    <p class="message-title">😢 No Recommendations Yet!</p>
    <p class="message-subtitle">
      Go like some delicious dishes and we’ll find you more 🍽️
    </p>
  </div>

  <div v-else class="grid">
    <div
      class="card"
      v-for="recipe in recommendations"
      :key="recipe.id"
      @click="viewDetail(recipe)"
    >
      <div class="image-wrapper">
        <img :src="recipe.picture_url" :alt="recipe.name" />
      </div>
      <div class="card-content">
        <p class="recipe-name">{{ recipe.name }}</p>
        <div class="recipe-meta">
          <p class="cook-time"> ⏰ {{ recipe.cook_time }}</p>
          <button class="like-button" @click.stop="toggleFavorite(recipe)">
              <span v-if="recipe.liked" class="liked-heart">❤️</span>
              <span v-else class="unliked-heart">♡</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { favoritesStore } from '@/store/favorite';
import RecipeDetail from './RecipeDetail.vue';

const recommendations = ref([]);
const selectedRecipe = ref(null);
const likedRecipes = ref([]);

function viewDetail(recipe) {
  selectedRecipe.value = recipe;
}

function toggleFavorite(recipe) {
  favoritesStore.toggleFavorite(recipe);
}

onMounted(async () => {
  const userId = localStorage.getItem('user_id');
  if (!userId) {
    console.warn("User not logged in.");
    return;
  }

  try {
    const res = await fetch(`http://localhost:5050/api/user/recommendations/${userId}`);
    if (res.ok) {
      const data = await res.json();
      recommendations.value = data;
    } else {
      console.error("Failed to fetch recommendations");
    }
  } catch (err) {
    console.error("Error fetching recommendations:", err);
  }
  await favoritesStore.loadFavorites();
  likedRecipes.value = favoritesStore.favorites;
});
</script>

<style scoped>

.no-favorites {
  text-align: center;
  margin-top: 60px;
  color: #555;
  font-family: 'Jua', sans-serif;
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
}</style>
