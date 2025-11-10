import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path: '/customers',
      name: 'customers',
      component: () => import('../views/CustomersView.vue')
    },
    {
      path: '/accounts',
      name: 'accounts',
      component: () => import('../views/AccountsView.vue')
    },
    {
      path: '/accounts/:id',
      name: 'account-detail',
      component: () => import('../views/AccountDetailView.vue')
    },
    {
      path: '/transactions',
      name: 'transactions',
      component: () => import('../views/TransactionsView.vue')
    },
    {
      path: '/loans',
      name: 'loans',
      component: () => import('../views/LoansView.vue')
    },
    {
      path: '/employees',
      name: 'employees',
      component: () => import('../views/EmployeesView.vue')
    },
    {
      path: '/branches',
      name: 'branches',
      component: () => import('../views/BranchesView.vue')
    }
  ]
})

export default router
