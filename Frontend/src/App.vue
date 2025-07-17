<template>
  <div id="app">
    <!-- Show AppNavbar only if not on login/signup -->
    <AppNavbar v-if="showNavbar" />
    <router-view />
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import AppNavbar from './components/AppNavbar.vue'

const route = useRoute()

// Hides navbar on login and signup
const showNavbar = computed(() => {
  return !['/', '/signup', '/login'].includes(route.path)
})
</script>

<style>
body {
  font-family: 'Arial', sans-serif;
  background: #fffdf3;
  margin: 0;
}
</style>
