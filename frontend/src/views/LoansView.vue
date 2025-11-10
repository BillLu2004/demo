<template>
  <div>
    <h1>贷款管理 (Loans)</h1>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>贷款申请列表</span>
           <el-button type="warning" @click="openAddDialog">新建贷款申请</el-button>
        </div>
      </template>
      <el-table :data="loans" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="申请ID" width="100" />
        <el-table-column prop="customer_name" label="客户姓名" width="180" />
        <el-table-column prop="amount" label="贷款金额">
           <template #default="scope">
            ¥{{ parseFloat(scope.row.amount).toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态">
             <template #default="scope">
                <el-tag :type="getStatusTag(scope.row.status)">{{ getStatusText(scope.row.status) }}</el-tag>
            </template>
        </el-table-column>
        <el-table-column prop="request_date" label="申请日期">
             <template #default="scope">
                {{ new Date(scope.row.request_date).toLocaleDateString() }}
            </template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center">
          <template #default="scope">
            <div v-if="scope.row.status === 'pending'">
              <el-button size="small" type="success" @click="handleApproval(scope.row, 'approved')">
                <el-icon class="el-icon--left"><Select /></el-icon>
                批准
              </el-button>
              <el-button size="small" type="danger" @click="handleApproval(scope.row, 'rejected')">
                <el-icon class="el-icon--left"><CloseBold /></el-icon>
                拒绝
              </el-button>
            </div>
            <span v-else>已处理</span>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" title="新建贷款申请" width="500" @close="resetForm">
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
        <el-form-item label="贷款金额">
          <el-input v-model.number="form.amount" type="number" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleAddLoan" :loading="formLoading">提交申请</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const dialogVisible = ref(false)
const loading = ref(true)
const formLoading = ref(false)
const loans = ref([])
const customers = ref<{id: number, name: string}[]>([])

const LOANS_API_URL = 'http://localhost:8000/api/loans/'
const CUSTOMERS_API_URL = 'http://localhost:8000/api/customers/'

const fetchLoans = async () => {
  loading.value = true
  try {
    const response = await fetch(LOANS_API_URL)
    if (response.ok) {
      loans.value = await response.json()
    } else {
      ElMessage.error('获取贷款列表失败')
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

const getStatusText = (status: string) => {
    const map: { [key: string]: string } = {
        pending: '待审批',
        approved: '已批准',
        rejected: '已拒绝',
        paid: '已还清',
    }
    return map[status] || '未知'
}

const getStatusTag = (status: string) => {
    const map: { [key: string]: string } = {
        pending: 'warning',
        approved: 'success',
        rejected: 'danger',
        paid: 'info',
    }
    return map[status] || ''
}

onMounted(() => {
  fetchLoans()
  fetchCustomers()
})

const form = ref({
  customer: null,
  amount: 0,
})

const resetForm = () => {
  form.value = { customer: null, amount: 0 }
}

const openAddDialog = () => {
  resetForm()
  dialogVisible.value = true
}

const handleAddLoan = async () => {
  formLoading.value = true
  try {
    const response = await fetch(LOANS_API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value),
    })
    if (response.ok) {
      ElMessage.success('贷款申请提交成功')
      dialogVisible.value = false
      await fetchLoans()
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

const handleApproval = async (loan: any, newStatus: 'approved' | 'rejected') => {
  const actionText = newStatus === 'approved' ? '批准' : '拒绝'
  await ElMessageBox.confirm(`您确定要${actionText}这笔贷款申请吗？`, '确认操作', {
    confirmButtonText: `确定${actionText}`,
    cancelButtonText: '取消',
    type: 'warning',
  })

  try {
    const response = await fetch(`${LOANS_API_URL}${loan.id}/`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus }),
    })
    if (response.ok) {
      ElMessage.success(`操作成功，贷款已${actionText}`)
      await fetchLoans()
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
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
