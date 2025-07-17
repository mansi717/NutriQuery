<template>
  <div>
    <h1 class="welcome-text">Welcome, {{ username }}!</h1>
    <div class="main-content">
      <FilterPanel />
      <RecipeGrid />
    </div>
  </div>
</template>

<script setup>
import FilterPanel from './FilterPanel.vue';
import RecipeGrid from './RecipeGrid.vue';
import { ref, onMounted } from 'vue';

const username = ref('User');

onMounted(() => {
  const storedName = localStorage.getItem('username');
  if (storedName) {
    username.value = storedName;
  }
});
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
</style>
