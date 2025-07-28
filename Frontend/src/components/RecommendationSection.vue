<template>
  <div v-if="recommendations.length === 0" class="no-favorites">
      <p class="message-title">😢 No Recommendations Yet!</p>
      <p class="message-subtitle">
        Go like some delicious dishes and we’ll find you more 🍽️
      </p>
    </div>
  <div v-else class="grid">
    <div class="card" v-for="recipe in recommendations" :key="recipe.id">
      <div class="image-wrapper">
        <img :src="recipe.picture_url" :alt="recipe.name" />
      </div>
      <div class="card-content">
        <p class="recipe-name">{{ recipe.name }}</p>
        <div class="recipe-meta">
          <p class="cook-time"> ⏰ {{ recipe.cook_time }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const recommendations = ref([]);

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
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  padding: 2rem;
}
.card {
  background-color: white;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: transform 0.2s ease;
}
.card:hover {
  transform: scale(1.03);
}
.image-wrapper img {
  width: 100%;
  height: 180px;
  object-fit: cover;
}
.card-content {
  padding: 1rem;
}
.recipe-name {
  font-weight: bold;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}
.recipe-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
