<template>
  <div class="about-page">
    <h1>About NutriQuery</h1>
    <p>
      NutriQuery is your smart meal filtering assistant. Whether you're watching calories,
      looking for quick meals, or following a specific diet like vegan or high-protein — we’ve got you covered.
    </p>

    <h2>What We Offer</h2>
    <ul>
      <li>Smart filtering based on nutrition goals</li>
      <li>Ingredient-based recipe suggestions</li>
      <li>Custom dietary options: Vegan, Vegetarian, Meat, Seafood</li>
      <li>Surprise meal generator for the adventurous!</li>
      <li>Clear nutrition facts: calories, protein, fats, and more</li>
    </ul>

    <h2>Our Mission</h2>
    <p>
      Our goal is to make healthy eating simple, personalized, and fun.
      Whether you're meal prepping, counting macros, or just exploring — NutriQuery helps you discover the perfect recipe for your needs.
    </p>

    <h2>How It Works</h2>
    <ol>
      <li>Select your dietary preferences (e.g., Vegan, High Protein)</li>
      <li>Adjust calorie or ingredient filters</li>
      <li>Browse matching recipes instantly</li>
      <li>Save your favorites for later</li>
    </ol>

    <h2>Built By</h2>
    <p>
      NutriQuery is a student project from the University of Stuttgart, created with love by aspiring computer scientists.
    </p>

    <h2>Contact Us</h2>
    <p>
      Have questions or suggestions? We’d love to hear from you.<br />
      Email us at: <a href="mailto:nutriquery@support.com">nutriquery@support.com</a>
    </p>
  </div>
</template>

<script setup>
// No additional logic needed
</script>

<style scoped>
.about-page {
  max-width: 700px;
  margin: 0 auto;
  padding: 40px 20px;
  font-family: 'Jua', sans-serif;
  color: rgba(0, 0, 0, 0.7);
}

.about-page h1 {
  font-size: 32px;
  margin-bottom: 20px;
  color: #A0C49D;
}

.about-page h2 {
  font-size: 24px;
  margin-top: 30px;
  color: #87B67A;
}

.about-page p {
  font-size: 16px;
  line-height: 1.6;
}

.about-page ul,
.about-page ol {
  padding-left: 20px;
  font-size: 16px;
  margin-top: 10px;
}

.about-page li {
  margin-bottom: 8px;
}

.about-page a {
  color: #5E8B7E;
  text-decoration: underline;
}
</style>
