import {
  createRouter,
  createWebHistory,
  type RouteLocationNormalized,
  type RouteRecordRaw,
} from 'vue-router'
import { useAuthSession } from '../composables/useAuthSession'

const WelcomePage = () => import('../pages/WelcomePage.vue')
const AuthPage = () => import('../pages/AuthPage.vue')
const InventoryPage = () => import('../pages/InventoryPage.vue')
const RecipesPage = () => import('../pages/RecipesPage.vue')
const RecipeDetailPage = () => import('../pages/RecipeDetailPage.vue')
const ProfilePage = () => import('../pages/ProfilePage.vue')
const NotFoundPage = () => import('../pages/NotFoundPage.vue')

declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean
    guestOnly?: boolean
    title?: string
  }
}

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'welcome',
    component: WelcomePage,
    meta: { title: 'Inicio' },
  },
  {
    path: '/auth',
    name: 'auth',
    component: AuthPage,
    meta: { guestOnly: true, title: 'Acceso' },
  },
  {
    path: '/inventario',
    name: 'inventory',
    component: InventoryPage,
    meta: { requiresAuth: true, title: 'Inventario' },
  },
  {
    path: '/recetas',
    name: 'recipes',
    component: RecipesPage,
    meta: { requiresAuth: true, title: 'Recetas' },
  },
  {
    path: '/recetas/:id',
    name: 'recipe-detail',
    component: RecipeDetailPage,
    meta: { requiresAuth: true, title: 'Detalle de receta' },
    props: true,
  },
  {
    path: '/perfil',
    name: 'profile',
    component: ProfilePage,
    meta: { requiresAuth: true, title: 'Perfil' },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFoundPage,
    meta: { title: 'No encontrado' },
  },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) return savedPosition
    return { top: 0, behavior: 'smooth' }
  },
})

router.beforeEach((to: RouteLocationNormalized) => {
  const { isAuthenticated } = useAuthSession()

  if (to.meta.requiresAuth && !isAuthenticated.value) {
    return { name: 'auth', query: { redirect: to.fullPath } }
  }

  if (to.meta.guestOnly && isAuthenticated.value) {
    return { name: 'inventory' }
  }

  return true
})

router.afterEach((to) => {
  const title = to.meta.title
  document.title = title ? `${title} · Recetas LLM` : 'Recetas LLM'
})
