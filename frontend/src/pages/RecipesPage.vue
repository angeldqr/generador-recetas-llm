<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import RecipeHistoryPanel from '../components/RecipeHistoryPanel.vue'
import { useAppData } from '../composables/useAppData'
import { useAuthSession } from '../composables/useAuthSession'
import { useStaggerReveal } from '../composables/useStaggerReveal'
import type { Recipe } from '../types/api'

const { token } = useAuthSession()
const { setRecipes } = useAppData()
const router = useRouter()

const pageRoot = ref<HTMLElement | null>(null)

useStaggerReveal({
  root: pageRoot,
  selector: '.history-card',
  delay: 0.32,
  stagger: 0.06,
  duration: 0.5,
})

function handleOpen(recipe: Recipe) {
  void router.push({ name: 'recipe-detail', params: { id: String(recipe.id) } })
}

function handleLoaded(recipes: Recipe[]) {
  setRecipes(recipes)
}
</script>

<template>
  <article ref="pageRoot" class="page page--recipes" data-route="recipes">
    <RecipeHistoryPanel
      :token="token"
      @open="handleOpen"
      @loaded="handleLoaded"
    />
  </article>
</template>

<style scoped>
.page--recipes {
  width: min(1180px, 100%);
  margin: 0 auto;
}
</style>
