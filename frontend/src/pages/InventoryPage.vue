<script setup lang="ts">
import { ref } from 'vue'
import InventoryPanel from '../components/InventoryPanel.vue'
import RecipeGenerator from '../components/RecipeGenerator.vue'
import { useAppData } from '../composables/useAppData'
import { useAuthSession } from '../composables/useAuthSession'
import { useStaggerReveal } from '../composables/useStaggerReveal'

const { token } = useAuthSession()
const { ingredients, setIngredients, prependRecipe } = useAppData()

const pageRoot = ref<HTMLElement | null>(null)

useStaggerReveal({
  root: pageRoot,
  selector: '.ingredient-card, .recipe-card',
  delay: 0.32,
  stagger: 0.05,
  duration: 0.45,
})

function handleIngredientsUpdated(next: Parameters<typeof setIngredients>[0]) {
  setIngredients(next)
}

function handleRecipeGenerated(recipe: Parameters<typeof prependRecipe>[0]) {
  prependRecipe(recipe)
}
</script>

<template>
  <article ref="pageRoot" class="page page--inventory" data-route="inventory">
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
