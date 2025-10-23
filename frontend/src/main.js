import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import components from '@/components/UI'

const app = createApp(App)
const pinia = createPinia()

components.forEach((component) => {
    app.component(component.name, component)
})

app.use(router)
    .use(pinia)
    .mount('#app')
