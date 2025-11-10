import { defineStore } from 'pinia'

export const useActionStore = defineStore('actions', {
  state: () => ({
    openAddCustomerDialog: false,
    openAddAccountDialog: false,
    openAddLoanDialog: false,
    openAddTransactionDialog: false,
  }),
  actions: {
    triggerAddCustomer() {
      this.openAddCustomerDialog = true
    },
    resetAddCustomer() {
      this.openAddCustomerDialog = false
    },
    
    // You can add similar actions for other dialogs
  },
})
