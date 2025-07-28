import { reactive } from 'vue';

export const favoritesStore = reactive({
  favorites: [],

  async loadFavorites() {
    const userId = localStorage.getItem('user_id');
    if (!userId || isNaN(userId)) {
      console.error('User ID not found in localStorage. Cannot load favorites.');
      this.favorites = []; // Clear favorites if no user
      return;
    }

    try {
      const response = await fetch(`http://localhost:5050/api/user/favorites/${parseInt(userId)}`);
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Failed to load favorites:', response.status, errorText);
        this.favorites = [];
        return;
      }
      const data = await response.json();
      // Mark loaded recipes as liked (important for `isFavorited` check)
      this.favorites = data.map(recipe => ({ ...recipe, liked: true }));
      console.log('Favorites loaded:', this.favorites);
    } catch (err) {
      console.error('Error fetching favorites:', err);
      this.favorites = [];
    }
  },

  async toggleFavorite(recipe) {
    const userId = localStorage.getItem('user_id');
    if (!userId || isNaN(userId)) {
      console.error('User ID not found in localStorage. Please log in to favorite recipes.');
      alert('Please log in to favorite recipes.');
      return;
    }

    const index = this.favorites.findIndex(r => r.id === recipe.id);
    const liked = index === -1; // True if recipe is not in favorites (we want to add it)

    // Optimistically update the UI
    if (liked) {
      this.favorites.push({ ...recipe, liked: true });
    } else {
      this.favorites.splice(index, 1);
    }

    try {
      const res = await fetch('http://localhost:5050/api/user/like', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: parseInt(userId),
          recipe_id: recipe.id,
          liked, // Send boolean true/false
        }),
      });

      if (!res.ok) {
        const text = await res.text();
        console.error('Server responded with error:', res.status, text);
        // If server error, revert optimistic update
        if (liked) {
            this.favorites.pop(); // Remove it if it was added
        } else {
            this.favorites.splice(index, 0, { ...recipe, liked: true }); // Add it back if it was removed
        }
      }
    } catch (err) {
      console.error('Failed to sync like:', err);
      // If network error, revert optimistic update
      if (liked) {
          this.favorites.pop();
      } else {
          this.favorites.splice(index, 0, { ...recipe, liked: true });
      }
    }
  },

  isFavorited(recipe) {
    return this.favorites.some(r => r.id === recipe.id);
  }
});