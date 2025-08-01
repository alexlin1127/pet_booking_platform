import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faPlay, faAngleLeft, faAngleRight } from '@fortawesome/free-solid-svg-icons'

// 引入css套件
import './style.css'

import './styles/main.css'

// 通用組件樣式
import './styles/components/common/navbar.css'
import './styles/components/common/footer.css'
import './styles/components/common/sidebar.css'
import './styles/components/common/pagination.css'

// UI組件樣式
import './styles/components/UI/card.css'
import './styles/components/UI/form.css'
import './styles/components/UI/modalbox.css'
import './styles/components/UI/button.css'
import './styles/components/UI/table.css'
import './styles/components/UI/tablecard.css'

// 管理員頁面樣式
import './styles/pages/Admin/index.css'
import './styles/pages/Admin/Accounts/accmanage.css'
import './styles/pages/Admin/Stores/storemanage.css'
import './styles/pages/Admin/Stores/storereview.css'
import './styles/pages/Admin/Posts/postmanage.css'
import './styles/pages/Admin/Posts/postreview.css'

// 商家註冊樣式
import './styles/auth/register/storesregister.css'

// 客戶註冊樣式
import './styles/auth/register/customersregister.css'

library.add(faPlay, faAngleLeft, faAngleRight)

const app = createApp(App)
app.component('FontAwesomeIcon', FontAwesomeIcon)
app.use(router).mount('#app')
