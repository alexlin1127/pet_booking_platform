import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faPlay, faAngleLeft, faAngleRight } from '@fortawesome/free-solid-svg-icons'

// 引入css套件
import './style.css'

import './styles/main.css'
import './styles/button.css'

import './styles/components/navbar.css'
import './styles/components/footer.css'
import './styles/components/form.css'
import './styles/components/table.css'
import './styles/components/sidebar.css'
import './styles/components/modalbox.css'
import './styles/components/pagination.css'

import './styles/Admin/card.css'
import './styles/Admin/review.css'
import './styles/Admin/postmanage.css'
import './styles/Admin/accmanage.css'
import './styles/Admin/storemanage.css'

import './styles/Users/register.css'

library.add(faPlay, faAngleLeft, faAngleRight)

const app = createApp(App)
app.component('FontAwesomeIcon', FontAwesomeIcon)
app.use(router).mount('#app')
