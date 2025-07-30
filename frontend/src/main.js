import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faPlay, faAngleLeft, faAngleRight } from '@fortawesome/free-solid-svg-icons'

library.add(faPlay, faAngleLeft, faAngleRight)

const app = createApp(App)
app.component('FontAwesomeIcon', FontAwesomeIcon)
app.use(router).mount('#app')
