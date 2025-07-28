<template>
  <div class="contact-page">
    <h1>Login</h1>

    <form class="contact-form" @submit.prevent="login">
      <label for="email">Email</label>
      <input id="email" type="email" v-model="email" required />

      <label for="password">Password</label>
      <input id="password" type="password" v-model="password" required />

      <button type="submit">Log In</button>
    </form>

    <div class="contact-info">
      <p>
        Don’t have an account?
        <span style="color: #87B67A; cursor: pointer;" @click="$router.push('/signup')">
          Sign up here
        </span>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const router = useRouter()

async function login() {
  try {
    const response = await fetch('http://localhost:5050/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: email.value,
        password: password.value,
      }),
    });

    const data = await response.json();
    if (response.ok) {
      localStorage.setItem('auth', 'true');
      localStorage.setItem('username', data.username);
      localStorage.setItem('user_id', data.user_id);
      router.push('/home');
    } else {
      alert(data.message);
    }
  } catch (err) {
    alert('Login failed.');
    console.error(err);
  }
}

</script>

<style scoped>
.contact-page {
  max-width: 700px;
  margin: 0 auto;
  padding: 40px 20px;
  font-family: 'Jua', sans-serif;
  color: rgba(0, 0, 0, 0.7);
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.contact-page h1 {
  font-size: 32px;
  margin-bottom: 20px;
  color: #A0C49D;
}

.contact-page p {
  font-size: 16px;
  margin-bottom: 20px;
  line-height: 1.5;
  max-width: 600px;
}

.contact-form {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 500px;
  text-align: left;
  margin-top: 20px;
}

.contact-form label {
  margin-top: 15px;
  margin-bottom: 5px;
  color: #333;
}

.contact-form input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 15px;
  font-family: inherit;
}

.contact-form button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #A0C49D;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.contact-form button:hover {
  background-color: #87B67A;
}

.contact-info {
  margin-top: 30px;
  text-align: center;
}

@media (max-width: 600px) {
  .contact-page {
    padding: 30px 15px;
  }

  .contact-page h1 {
    font-size: 26px;
  }

  .contact-form input {
    font-size: 14px;
  }

  .contact-form button {
    font-size: 15px;
  }
}
</style>
