<template>
  <nav class="app-navbar">
    <img src="@/assets/NutriQueryLogo.png" alt="NutriQuery Logo" style="width: 168px; height: 52px;" />
    <div class="nav-links">
      <RouterLink to="/home" class="nav-link">Home</RouterLink>
      <RouterLink to="/about" class="nav-link">About</RouterLink>
      <RouterLink to="/recommendations" class="nav-link">Recommendations</RouterLink>
      <RouterLink to="/favorite" class="nav-link">Favourites</RouterLink>
      <RouterLink to="/contact" class="nav-link">Contact</RouterLink>
      <a href="#" class="nav-link" @click.prevent="showLogoutDialog = true">Logout</a>
    </div>

    <!-- Logout Confirmation Modal -->
  <div v-if="showLogoutDialog" class="modal-overlay" @click.self="showLogoutDialog = false">
    <div class="modal-content">
      <p>Do you really want to log out?</p>
      <div class="modal-buttons">
        <button @click="confirmLogout">Yes</button>
        <button @click="showLogoutDialog = false">No</button>
      </div>
    </div>
  </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const showLogoutDialog = ref(false)

function confirmLogout() {
  localStorage.removeItem('auth')
  localStorage.removeItem('username')
  router.push('/login')
  showLogoutDialog.value = false
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

.app-navbar {
  display: flex;
  align-items: center; 
  justify-content: space-between;
  padding: 32px 64px 0 64px;
  font-family: 'Jua', sans-serif;
}

.nav-links {
  display: flex;
  align-items: center;
}

.nav-links a {
  margin-left: 20px;
  text-decoration: none;
  font-size: 16px;
  color: rgba(0, 0, 0, 0.46); /* 46% opacity */
  line-height: normal;
  cursor: pointer;
}
/* Blur the navbar and content when modal is active */
.blurred {
  filter: blur(5px);
  pointer-events: none; 
  user-select: none;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.3);
  backdrop-filter: blur(5px); /* Blur background behind overlay */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-content {
  background: white;
  padding: 24px 32px;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
  text-align: center;
  font-family: 'Jua', sans-serif;
  max-width: 320px;
  width: 90%;
}

.modal-buttons {
  margin-top: 20px;
}

.modal-buttons button {
  background-color: #A0C49D;
  border: none;
  color: white;
  font-size: 16px;
  padding: 10px 24px;
  margin: 0 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.modal-buttons button:hover {
  background-color: #87B67A;
}
</style>

