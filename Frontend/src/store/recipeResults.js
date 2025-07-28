// src/store/recipeResults.js
import { ref } from 'vue'
import { favoritesStore } from './favorite.js'

export const recipeResults = ref([])

export async function setRecipeResults(newRecipes) {
  // Ensure favorites are loaded before syncing
  if (favoritesStore.favorites.length === 0) {
    await favoritesStore.loadFavorites()
  }

  const favoriteIds = favoritesStore.favorites.map(r => r.id)

  // Mark liked recipes
  recipeResults.value = newRecipes.map(recipe => ({
    ...recipe,
    liked: favoriteIds.includes(recipe.id),
  }))
}