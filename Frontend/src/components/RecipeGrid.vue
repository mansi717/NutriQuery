<template>
  <div class="grid">
    <div class="card" v-for="recipe in recipes" :key="recipe.name">
      <div class="image-wrapper">
        <img :src="recipe.image" :alt="recipe.name" />
      </div>
      <div class="card-content">
        <p class="recipe-name">{{ recipe.name }}</p>
        <button class="like-button" @click="toggleLike(recipe)">
          <span v-if="recipe.liked" class="liked-heart">❤️</span>
          <span v-else class="unliked-heart">♡</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { recipes } from '@/store/recipes.js'

function toggleLike(recipe) {
  recipe.liked = !recipe.liked
  console.log(recipe.name, 'liked:', recipe.liked)
}

</script>



<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  width: 100%;
  box-sizing: border-box;
  flex-grow: 1;
}

.card {
  background: white;
  padding: 8px;
  border-radius: 12px;
  box-shadow: 0 0 10px #eee;
  overflow: hidden;
}

.image-wrapper {
  overflow: hidden;
  border-radius: 10px;
  margin-bottom: 10px;
}

.card img {
  width: 100%;
  object-fit: cover;
  border-radius: 10px;
}

.card-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 5px;
  margin-top: auto;
}

.recipe-name {
  font-size: 16px;
  font-weight: bold;
  color: rgba(0, 0, 0, 0.7);
  margin: 0;
  text-align: left;
  flex-grow: 1;
  font-family: 'Jua', sans-serif;
  padding-right: 10px;
}

.like-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 24px;
  padding: 0; 
  line-height: 1; 
  display: flex; 
  align-items: center;
  justify-content: center;
}

.liked-heart {
  color: #ff0000; 
}

.unliked-heart {
  color: black; /* Black for the outline of the unliked heart */
  /* The '♡' character itself often provides the outline appearance */
  /* If you want a thicker outline or more specific look, you might use:
     -webkit-text-stroke: 1px black;
     -webkit-text-fill-color: transparent;
     color: transparent; // For other browsers
     But '♡' usually suffices.
  */
}
</style>