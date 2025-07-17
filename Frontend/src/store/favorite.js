import { reactive } from 'vue';

export const favoritesStore = reactive({
  favorites: [],

  toggleFavorite(recipe) {
    const index = this.favorites.findIndex(r => r.id === recipe.id);
    if (index === -1) {
      this.favorites.push(recipe);
    } else {
      this.favorites.splice(index, 1);
    }
  },

  isFavorited(recipe) {
    return this.favorites.some(r => r.id === recipe.id);
  }
});