<script setup lang="ts">
import InventoryPanel from '../components/InventoryPanel.vue'
import RecipeGenerator from '../components/RecipeGenerator.vue'
import { useAppData } from '../composables/useAppData'
import { useAuthSession } from '../composables/useAuthSession'

const { token } = useAuthSession()
const { ingredients, setIngredients, prependRecipe } = useAppData()

function handleIngredientsUpdated(next: Parameters<typeof setIngredients>[0]) {
  setIngredients(next)
}

function handleRecipeGenerated(recipe: Parameters<typeof prependRecipe>[0]) {
  prependRecipe(recipe)
}
</script>

<template>
  <article class="page page--inventory" data-route="inventory">
    <div class="inventory-stack">
      <RecipeGenerator
        :token="token"
        :ingredient-count="ingredients.length"
        @generated="handleRecipeGenerated"
      />
      <InventoryPanel
        :token="token"
        @updated="handleIngredientsUpdated"
      />
    </div>
  </article>
</template>

<style scoped>
.page--inventory {
  width: min(1180px, 100%);
  margin: 0 auto;
}
</style>
