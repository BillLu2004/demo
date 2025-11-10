<template>
  <div>
    <h1>账户管理 (Accounts)</h1>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>账户列表</span>
          <el-button type="primary" @click="openAddDialog">开设新账户</el-button>
        </div>
      </template>
      <el-table :data="accounts" style="width: 100%" v-loading="loading">
        <el-table-column prop="account_id" label="账户ID" width="220" />
        <el-table-column prop="customer_name" label="客户姓名" width="180" />
        <el-table-column prop="balance" label="余额">
          <template #default="scope">
            ¥{{ parseFloat(scope.row.balance).toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态">
            <template #default="scope">
                <el-tag :type="scope.row.status === 'active' ? 'success' : 'danger'">{{ scope.row.status === 'active' ? '正常' : '冻结' }}</el-tag>
            </template>
        </el-table-column>
        <el-table-column label="操作" width="280" align="center">
          <template #default="scope">
            <el-button size="small" type="primary" plain @click="viewDetails(scope.row.id)">详情</el-button>
            <el-button size="small" type="info" plain @click="openCardDialog(scope.row)">银行卡管理</el-button>
            <el-button 
              v-if="scope.row.status === 'active'"
              size="small" 
              type="danger" 
              plain
              @click="handleStatusChange(scope.row, 'frozen')">
              冻结
            </el-button>
            <el-button 
              v-if="scope.row.status === 'frozen'"
              size="small" 
              type="success" 
              plain
              @click="handleStatusChange(scope.row, 'active')">
              解冻
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

     <el-dialog v-model="dialogVisible" title="开设新账户" width="500" @close="resetForm">
      <el-form :model="form" label-width="100px">
        <el-form-item label="选择客户">
          <el-select v-model="form.customer" placeholder="请选择客户" style="width: 100%;">
            <el-option
              v-for="customer in customers"
              :key="customer.id"
              :label="customer.name"
              :value="customer.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="账户ID">
          <el-input v-model="form.account_id" placeholder="请输入16-20位账户ID" />
        </el-form-item>
        <el-form-item label="初始余额">
          <el-input v-model.number="form.balance" type="number" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleAddAccount" :loading="formLoading">提交</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- Card Management Dialog -->
    <el-dialog v-model="cardDialogVisible" title="银行卡管理" width="70%">
      <div v-if="selectedAccount">
        <p><strong>当前账户:</strong> {{ selectedAccount.account_id }} ({{ selectedAccount.customer_name }})</p>
        <el-button type="primary" @click="showAddCardForm = !showAddCardForm" style="margin-bottom: 15px;">
          {{ showAddCardForm ? '取消新增' : '绑定新卡' }}
        </el-button>

        <el-form v-if="showAddCardForm" :model="cardForm" label-width="80px" style="margin-bottom: 20px;">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="卡号">
                <el-input v-model="cardForm.card_number" placeholder="请输入银行卡号"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="12">
               <el-form-item label="卡类型">
                <el-select v-model="cardForm.card_type" placeholder="请选择">
                  <el-option label="借记卡" value="debit"></el-option>
                  <el-option label="信用卡" value="credit"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="有效期">
                <el-date-picker v-model="cardForm.expiry_date" type="date" placeholder="选择日期" format="YYYY-MM-DD" value-format="YYYY-MM-DD"></el-date-picker>
              </el-form-item>
            </el-col>
            <el-col :span="12">
               <el-button type="success" @click="handleAddCard">确认绑定</el-button>
            </el-col>
          </el-row>
        </el-form>
        
        <el-table :data="cards" v-loading="cardLoading">
          <el-table-column prop="card_number" label="卡号"></el-table-column>
          <el-table-column prop="card_type" label="卡类型">
            <template #default="scope">{{ scope.row.card_type === 'debit' ? '借记卡' : '信用卡' }}</template>
          </el-table-column>
          <el-table-column prop="expiry_date" label="有效期"></el-table-column>
          <el-table-column prop="is_active" label="状态">
            <template #default="scope">
              <el-tag :type="scope.row.is_active ? 'success' : 'danger'">{{ scope.row.is_active ? '已激活' : '未激活' }}</el-tag>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()

const dialogVisible = ref(false)
const loading = ref(true)
const formLoading = ref(false)
const accounts = ref([])
const customers = ref<{id: number, name: string}[]>([])

const ACCOUNTS_API_URL = 'http://localhost:8000/api/accounts/'
const CUSTOMERS_API_URL = 'http://localhost:8000/api/customers/'

const fetchAccounts = async () => {
  loading.value = true
  try {
    const response = await fetch(ACCOUNTS_API_URL)
    if (response.ok) {
      accounts.value = await response.json()
    } else {
      ElMessage.error('获取账户列表失败')
    }
  } catch (error) {
    ElMessage.error('网络错误，请稍后重试')
  } finally {
    loading.value = false
  }
}

const fetchCustomers = async () => {
  try {
    const response = await fetch(CUSTOMERS_API_URL)
    if (response.ok) {
      customers.value = await response.json()
    } else {
      ElMessage.error('获取客户下拉列表失败')
    }
  } catch (error) {
    ElMessage.error('网络错误，请稍后重试')
  }
}

onMounted(() => {
  fetchAccounts()
  fetchCustomers()
})

const form = ref({
  customer: null,
  account_id: '',
  balance: 0,
})

const resetForm = () => {
  form.value = { customer: null, account_id: '', balance: 0 }
}

const openAddDialog = () => {
  resetForm()
  dialogVisible.value = true
}

const handleAddAccount = async () => {
  formLoading.value = true
  try {
    const response = await fetch(ACCOUNTS_API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value),
    })
    if (response.ok) {
      ElMessage.success('开设账户成功')
      dialogVisible.value = false
      await fetchAccounts()
    } else {
      const errorData = await response.json()
      ElMessage.error(`操作失败: ${JSON.stringify(errorData)}`)
    }
  } catch (error) {
    ElMessage.error('网络错误，请稍后重试')
  } finally {
    formLoading.value = false
  }
}

const handleStatusChange = async (account: any, newStatus: 'active' | 'frozen') => {
  const actionText = newStatus === 'frozen' ? '冻结' : '解冻'
  await ElMessageBox.confirm(`您确定要${actionText}该账户吗？`, '确认操作', {
    confirmButtonText: `确定${actionText}`,
    cancelButtonText: '取消',
    type: 'warning',
  })

  try {
    const response = await fetch(`${ACCOUNTS_API_URL}${account.id}/`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus }),
    })
    if (response.ok) {
      ElMessage.success(`账户已${actionText}`)
      await fetchAccounts()
    } else {
      const errorData = await response.json()
      ElMessage.error(`操作失败: ${JSON.stringify(errorData)}`)
    }
  } catch (error) {
     if (error !== 'cancel') {
        ElMessage.error('网络错误，请稍后重试')
    }
  }
}

// --- New state for Card Management ---
const cardDialogVisible = ref(false)
const cardLoading = ref(false)
const showAddCardForm = ref(false)
const selectedAccount = ref<any>(null)
const cards = ref([])

const cardForm = ref({
  card_number: '',
  card_type: 'debit',
  expiry_date: '',
  is_active: true,
  account: null,
})

const CARDS_API_URL = 'http://localhost:8000/api/cards/'

const openCardDialog = async (account: any) => {
  selectedAccount.value = account
  cardDialogVisible.value = true
  showAddCardForm.value = false
  cardForm.value.account = account.id
  await fetchCards(account.id)
}

const fetchCards = async (accountId: number) => {
  cardLoading.value = true
  try {
    const response = await fetch(`${CARDS_API_URL}?account_id=${accountId}`)
    if (response.ok) {
      cards.value = await response.json()
    } else {
      ElMessage.error('获取银行卡列表失败')
    }
  } catch (error) {
    ElMessage.error('网络错误')
  } finally {
    cardLoading.value = false
  }
}

const handleAddCard = async () => {
  try {
    const response = await fetch(CARDS_API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(cardForm.value),
    })
    if (response.ok) {
      ElMessage.success('绑定新卡成功')
      showAddCardForm.value = false
      await fetchCards(selectedAccount.value.id)
    } else {
      const errorData = await response.json()
      ElMessage.error(`绑定失败: ${JSON.stringify(errorData)}`)
    }
  } catch (error) {
    ElMessage.error('网络错误')
  }
}

const viewDetails = (accountId: number) => {
  router.push(`/accounts/${accountId}`)
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
