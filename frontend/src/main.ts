import { createApp } from 'vue'
import App from './App.vue'
import { router } from './router'
import './styles/main.css'
import './styles/shell.css'
import './styles/auth.css'
import './styles/inventory.css'
import './styles/modal.css'
import './styles/recipe.css'

const app = createApp(App)
app.use(router)
app.mount('#app')
