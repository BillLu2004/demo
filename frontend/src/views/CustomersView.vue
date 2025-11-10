<template>
  <div class="page-container">
    <el-card class="fill-card">
      <template #header>
        <div class="card-header">
          <span>客户列表</span>
          <el-button type="primary" @click="openDialog()">
            <el-icon class="el-icon--left"><Plus /></el-icon>
            新增客户
          </el-button>
        </div>
      </template>
      <el-table :data="customers" style="width: 100%" stripe v-loading="loading">
        <el-table-column prop="id" label="客户ID" width="100" />
        <el-table-column prop="name" label="姓名" width="180" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="phone" label="电话" />
        <el-table-column label="操作" width="200" align="center">
          <template #default="scope">
            <el-button size="small" type="primary" plain @click="openDialog(scope.row)">
              <el-icon class="el-icon--left"><Edit /></el-icon>
              编辑
            </el-button>
            <el-button size="small" type="danger" plain @click="handleDelete(scope.row.id)">
              <el-icon class="el-icon--left"><Delete /></el-icon>
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEditMode ? '编辑客户' : '新增客户'" width="500" @close="resetForm">
      <el-form :model="form">
        <el-form-item label="姓名">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="form.phone" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="formLoading">
            提交
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useActionStore } from '@/stores/actions'

const dialogVisible = ref(false)
const loading = ref(true)
const formLoading = ref(false)
const customers = ref([])
const editingCustomer = ref<any>(null)

const isEditMode = computed(() => !!editingCustomer.value)

const API_URL = 'http://localhost:8000/api/customers/'

const actionStore = useActionStore()

const fetchCustomers = async () => {
  loading.value = true
  try {
    const response = await fetch(API_URL)
    if (response.ok) {
      customers.value = await response.json()
    } else {
      ElMessage.error('获取客户列表失败')
    }
  } catch (error) {
    ElMessage.error('网络错误，请稍后重试')
    console.error('An error occurred:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCustomers()
  if (actionStore.openAddCustomerDialog) {
    openDialog()
    actionStore.resetAddCustomer()
  }
})

const form = ref({
  name: '',
  email: '',
  phone: '',
})

const resetForm = () => {
  form.value = { name: '', email: '', phone: '' }
  editingCustomer.value = null
}

const openDialog = (customer: any = null) => {
  resetForm()
  if (customer) {
    editingCustomer.value = customer
    form.value = { ...customer }
  }
  dialogVisible.value = true
}

const handleSubmit = () => {
  if (isEditMode.value) {
    handleUpdateCustomer()
  } else {
    handleAddCustomer()
  }
}

const handleAddCustomer = async () => {
  formLoading.value = true
  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value),
    })
    if (response.ok) {
      ElMessage.success('新增客户成功')
      dialogVisible.value = false
      await fetchCustomers()
    } else {
      const errorData = await response.json()
      ElMessage.error(`新增失败: ${JSON.stringify(errorData)}`)
    }
  } catch (error) {
    ElMessage.error('网络错误，请稍后重试')
  } finally {
    formLoading.value = false
  }
}

const handleUpdateCustomer = async () => {
  formLoading.value = true
  try {
    const response = await fetch(`${API_URL}${editingCustomer.value.id}/`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value),
    })
    if (response.ok) {
      ElMessage.success('更新客户成功')
      dialogVisible.value = false
      await fetchCustomers()
    } else {
      const errorData = await response.json()
      ElMessage.error(`更新失败: ${JSON.stringify(errorData)}`)
    }
  } catch (error) {
    ElMessage.error('网络错误，请稍后重试')
  } finally {
    formLoading.value = false
  }
}

const handleDelete = async (customerId: number) => {
  await ElMessageBox.confirm('您确定要删除该客户吗？此操作不可撤销。', '警告', {
    confirmButtonText: '确定删除',
    cancelButtonText: '取消',
    type: 'warning',
  })
  try {
    const response = await fetch(`${API_URL}${customerId}/`, {
      method: 'DELETE',
    })
    if (response.ok) {
      ElMessage.success('删除客户成功')
      await fetchCustomers()
    } else {
      const errorData = await response.json()
      ElMessage.error(`删除失败: ${JSON.stringify(errorData)}`)
    }
  } catch (error) {
    if (error !== 'cancel') {
        ElMessage.error('网络错误，请稍后重试')
    }
  }
}
</script>

<style scoped>
.page-container {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.fill-card {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

:deep(.el-card__body) {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

:deep(.el-table) {
  flex-grow: 1;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
