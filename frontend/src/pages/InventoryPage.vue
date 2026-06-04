<script setup lang="ts">
import InventoryPanel from '../components/InventoryPanel.vue'
import RecipeGenerator from '../components/RecipeGenerator.vue'
import type { Ingredient, Recipe } from '../types/api'

const props = defineProps<{
  token: string
  ingredients: Ingredient[]
}>()

const emit = defineEmits<{
  'ingredients-updated': [ingredients: Ingredient[]]
  'recipe-generated': [recipe: Recipe]
}>()

function handleIngredientsUpdated(next: Ingredient[]) {
  emit('ingredients-updated', next)
}

function handleRecipeGenerated(recipe: Recipe) {
  emit('recipe-generated', recipe)
}
</script>

<template>
  <article class="page page--inventory" data-route="inventory">
    <div class="inventory-stack">
      <RecipeGenerator
        :token="props.token"
        :ingredient-count="props.ingredients.length"
        @generated="handleRecipeGenerated"
      />
      <InventoryPanel :token="props.token" @updated="handleIngredientsUpdated" />
    </div>
  </article>
</template>

<style scoped>
.page--inventory {
  width: min(1180px, 100%);
  margin: 0 auto;
}
</style>
