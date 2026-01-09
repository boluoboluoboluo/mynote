// import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import elementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import './assets/common.css'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(elementPlus)
app.use(router)

app.mount('#app')
