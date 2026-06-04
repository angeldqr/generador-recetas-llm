<script setup lang="ts">
import { useRouter } from 'vue-router'
import RecipeHistoryPanel from '../components/RecipeHistoryPanel.vue'
import type { Recipe } from '../types/api'

const props = defineProps<{
  token: string
}>()

const emit = defineEmits<{
  loaded: [recipes: Recipe[]]
}>()

const router = useRouter()

function handleOpen(recipe: Recipe) {
  void router.push({ name: 'recipe-detail', params: { id: String(recipe.id) } })
}

function handleLoaded(recipes: Recipe[]) {
  emit('loaded', recipes)
}
</script>

<template>
  <article class="page page--recipes" data-route="recipes">
    <RecipeHistoryPanel
      :token="props.token"
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
