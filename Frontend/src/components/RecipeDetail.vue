<template>
  <div class="recipe-detail">
    <button class="back-button" @click="$emit('close-detail')">← Back to Recipes</button>
    <div class="detail-card">
      <div class="detail-header">
        <img :src="recipe.picture_url" :alt="recipe.name" class="detail-image" />
        <h3 class="detail-name">{{ recipe.name }}</h3>
      </div>

      <div class="detail-body">
        <p class="detail-meta">⏰ Cook Time: {{ recipe.cook_time || 'N/A' }}</p>

        <h4>Ingredients</h4>
        <ul class="ingredient-list">
          <li v-for="(ingredient, index) in recipe.ingredients" :key="index">{{ ingredient }}</li>
        </ul>

        <h4>Directions</h4>
        <ul class="directions-list">
          <li v-for="(direction, index) in directionsList" :key="index" class="direction-step-item">
            {{ direction }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, computed } from 'vue';

const props = defineProps({
  recipe: {
    type: Object,
    required: true
  }
});


const directionsList = computed(() => {
  if (Array.isArray(props.recipe.directions)) {
    return props.recipe.directions;
  }

  const directionsString = props.recipe.directions || '';

  return directionsString
    .split(/[\n]+/)  // Split on both newlines and periods
    .map(s => s.trim())
    .filter(s => s.length > 0);
});
</script>

<style scoped>
.recipe-detail {
  position: fixed;           /* Full screen */
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: white;
  z-index: 9999;             /* Above all other content */
  overflow-y: auto;
  padding: 2rem;
  box-sizing: border-box;
}

.back-button {
  background: #A0C49D;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 8px;
  cursor: pointer;
  margin-bottom: 20px;
  font-family: 'Jua', sans-serif;
}

.detail-card {
  max-width: 800px;
  margin: 0 auto;           /* Center horizontally */
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.detail-header {
  text-align: center;
  position: relative;
}

.detail-image {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.detail-name {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 1rem;
  margin: 0;
  font-family: 'Jua', sans-serif;
}

.detail-body {
  padding: 1.5rem;
}

.detail-meta {
  font-style: italic;
  color: #555;
}

.ingredient-list,
.directions-list {
  padding-left: 20px;
  margin-bottom: 1rem;
  list-style-type: none;
}

.directions-list {
  padding-left: 0;
}

.direction-step-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  margin-bottom: 10px;
  line-height: 1.5;
}

.direction-step-item::before {
  content: " ";
  flex-shrink: 0;
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #A0C49D;
  margin-top: 8px;
}
</style>