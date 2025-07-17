<template>
  <div class="contact-page">
    <h1>Contact Us</h1>
    <p>
      We'd love to hear from you — whether it's feedback, suggestions, or just saying hi!
      Use the form below or reach out via email.
    </p>

    <form class="contact-form" @submit.prevent="handleSubmit">
      <label for="name">Name</label>
      <input id="name" type="text" v-model="name" required />

      <label for="email">Email</label>
      <input id="email" type="email" v-model="email" required />

      <label for="message">Message</label>
      <textarea id="message" rows="5" v-model="message" required></textarea>

      <button type="submit">Send Message</button>
    </form>

    <div class="contact-info">
      <h2>Or reach us at:</h2>
      <p>Email: <a href="mailto:nutriquery@support.com">nutriquery@support.com</a></p>
      <p>University of Stuttgart, Autonomous Systems</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const name = ref('')
const email = ref('')
const message = ref('')

function handleSubmit() {
  // For now, we'll just log the data
  console.log('Submitted:', { name: name.value, email: email.value, message: message.value })
  alert('Message sent! (This is just a demo — no backend yet.)')

  // Clear form
  name.value = ''
  email.value = ''
  message.value = ''
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

.contact-page h2 {
  font-size: 24px;
  margin-top: 30px;
  color: #87B67A;
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

.contact-form input,
.contact-form textarea {
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
  margin-top: 40px;
  text-align: center;
}

.contact-info a {
  color: #87B67A;
  text-decoration: none;
}

@media (max-width: 600px) {
  .contact-page {
    padding: 30px 15px;
  }

  .contact-page h1 {
    font-size: 26px;
  }

  .contact-form input,
  .contact-form textarea {
    font-size: 14px;
  }

  .contact-form button {
    font-size: 15px;
  }
}
</style>
