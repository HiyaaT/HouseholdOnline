import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import CreateServiceView from '@/views/CreateServiceView.vue'
import AdminView from '@/views/AdminView.vue'
import SearchBarView from '@/views/SearchBarView.vue'
import CustomerDash from '@/views/CustomerDash.vue'
import SearchCustomer from '@/views/SearchCustomer.vue'
import ProfessionalDash from '@/views/ProfessionalDash.vue'
import ProfessionalProfile from '@/views/Profile.vue'
import AdminSummary from '@/views/AdminSummary.vue'
import ProfessionalSummary from '@/views/ProfessionalSummary.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/homepage',
      name: 'homePage',
      //component:
    },
    
    {
      path: '/search_admin',
      name: 'SearchAdmin',
      component: SearchBarView
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfessionalProfile
    },
    {
      path: '/admin_summary',
      name: 'admin_summary',
      component: AdminSummary
    },
    
    {
      path: '/professional_summary',
      name: 'professional_summary',
      component: ProfessionalSummary
    },
    {
      path: '/professional-dash',
      name: 'ProfessionalDash',
      component: ProfessionalDash
    },
    {
      path: '/admin-dash',
      name: 'admin-dash',
      component: AdminView
    },
    {
      path: '/customer-dash',
      name: 'customer-dash',
      component: CustomerDash
    },
    {
      path: '/search_customer',
      name: 'SearchCustomer',
      component: SearchCustomer
    },

    {
      path: '/createservice',
      name: 'createService',
      component:CreateServiceView
    },
    {
      path: '/',
      name: 'login',
      component: LoginView
    },

    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router
