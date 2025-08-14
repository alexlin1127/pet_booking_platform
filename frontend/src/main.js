import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faPlay, faAngleLeft, faAngleRight, faCalendar, faHandshake, faBookmark } from '@fortawesome/free-solid-svg-icons'
import { faLine, faGoogle, faFacebookF } from '@fortawesome/free-brands-svg-icons'

// 引入css套件
import './style.css'
import './styles/main.css'

// 
import './styles/auth/register.css'

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

// 使用者頁面樣式
import './styles/pages/Customers/customersregister.css'

// 商家頁面樣式
import './styles/pages/Stores/dashboard.css'
import './styles/pages/Stores/Booking/addbookings.css'
import './styles/pages/Stores/storesregister.css'
import './styles/pages/Stores/Booking/bookinghistory.css'
import './styles/pages/Stores/Booking/Grooming/grooming.css'
import './styles/pages/Stores/Booking/Boarding/boarding.css'

// 
import './styles/pages/Stores/Info/editinfo.css'
import './styles/pages/Stores/Info/infomanagement.css'
import './styles/pages/Stores/Info/openservices.css'
// 
import './styles/pages/Stores/Services/servicesmanagement.css'
import './styles/pages/Stores/Services/addservices.css'

// 
import './styles/pages/Stores/Posts/postsmanage.css'
import './styles/pages/Stores/Posts/postsprocess.css'
import './styles/pages/Stores/Posts/postsview.css'

// 管理員頁面樣式
import './styles/pages/Admin/admindashboard.css'
import './styles/pages/Admin/Posts/postmanage.css'
import './styles/pages/Admin/Posts/postreview.css'





library.add(faPlay, faAngleLeft, faAngleRight, faCalendar, faHandshake, faBookmark, faLine, faGoogle, faFacebookF)

const app = createApp(App)
app.component('FontAwesomeIcon', FontAwesomeIcon)
app.use(router).mount('#app')
