import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

axios.defaults.baseURL = 'http://127.0.0.1:8000'
axios.defaults.withCredentials = true
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

axios.get('/sanctum/csrf-cookie').catch(() => {})

const app = createApp(App);
app.config.globalProperties.$http = axios;

app.use(store).use(router).mount('#app')

