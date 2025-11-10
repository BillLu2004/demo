<template>
  <div class="page-container">
    <el-card class="fill-card">
      <template #header>
        <div class="card-header">
          <span>员工管理</span>
          <el-button type="primary" @click="openDialog()">
            <el-icon class="el-icon--left"><Plus /></el-icon>
            新增员工
          </el-button>
        </div>
      </template>
      <el-table :data="employees" style="width: 100%" stripe v-loading="loading">
        <el-table-column prop="employee_id" label="员工号" width="120" />
        <el-table-column prop="name" label="姓名" width="150" />
        <el-table-column prop="position" label="职位" width="150" />
        <el-table-column prop="branch_name" label="所属分行" />
        <el-table-column label="操作" width="200" align="center">
          <template #default="scope">
            <el-button size="small" type="primary" plain @click="openDialog(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" plain @click="handleDelete(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEditMode ? '编辑员工' : '新增员工'" width="500" @close="resetForm">
      <el-form :model="form" label-width="80px">
        <el-form-item label="员工号">
          <el-input v-model="form.employee_id" />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="职位">
           <el-select v-model="form.position" placeholder="请选择职位">
            <el-option label="柜员" value="teller"></el-option>
            <el-option label="经理" value="manager"></el-option>
            <el-option label="系统管理员" value="admin"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="所属分行">
          <el-select v-model="form.branch" placeholder="请选择分行">
            <el-option v-for="branch in branches" :key="branch.id" :label="branch.name" :value="branch.id"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="formLoading">提交</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const employees = ref([])
const branches = ref<{id: number, name: string}[]>([])
const loading = ref(true)
const dialogVisible = ref(false)
const formLoading = ref(false)
const editingEmployee = ref<any>(null)

const isEditMode = computed(() => !!editingEmployee.value)
const EMPLOYEES_API_URL = 'http://localhost:8000/api/employees/'
const BRANCHES_API_URL = 'http://localhost:8000/api/branches/'

const form = ref({
  employee_id: '',
  name: '',
  position: '',
  branch: null,
})

const fetchEmployees = async () => {
  loading.value = true
  try {
    const response = await fetch(EMPLOYEES_API_URL)
    if (response.ok) {
      employees.value = await response.json()
    } else {
      ElMessage.error('获取员工列表失败')
    }
  } catch (error) {
    ElMessage.error('网络错误，请稍后重试')
  } finally {
    loading.value = false
  }
}

const fetchBranches = async () => {
  try {
    const response = await fetch(BRANCHES_API_URL)
    if (response.ok) {
      branches.value = await response.json()
    } else {
      ElMessage.error('获取分行列表失败')
    }
  } catch (error) {
    ElMessage.error('网络错误，请稍后重试')
  }
}

onMounted(() => {
  fetchEmployees()
  fetchBranches()
})

const resetForm = () => {
  form.value = { employee_id: '', name: '', position: '', branch: null }
  editingEmployee.value = null
}

const openDialog = (employee: any = null) => {
  resetForm()
  if (employee) {
    editingEmployee.value = employee
    form.value = { ...employee }
  }
  dialogVisible.value = true
}

const handleSubmit = () => {
  isEditMode.value ? handleUpdate() : handleAdd()
}

const handleAdd = async () => {
  formLoading.value = true
  try {
    const response = await fetch(EMPLOYEES_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(form.value),
    })
    if (response.ok) {
      ElMessage.success('员工添加成功')
      fetchEmployees()
      dialogVisible.value = false
    } else {
      const errorData = await response.json()
      ElMessage.error(errorData.detail || '添加员工失败')
    }
  } catch (error) {
    ElMessage.error('网络错误，请稍后重试')
  } finally {
    formLoading.value = false
  }
}

const handleUpdate = async () => {
  formLoading.value = true
  try {
    const response = await fetch(`${EMPLOYEES_API_URL}${editingEmployee.value.id}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(form.value),
    })
    if (response.ok) {
      ElMessage.success('员工更新成功')
      fetchEmployees()
      dialogVisible.value = false
    } else {
      const errorData = await response.json()
      ElMessage.error(errorData.detail || '更新员工失败')
    }
  } catch (error) {
    ElMessage.error('网络错误，请稍后重试')
  } finally {
    formLoading.value = false
  }
}

const handleDelete = async (employeeId: number) => {
  ElMessageBox.confirm('确定要删除此员工吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  })
    .then(async () => {
      try {
        const response = await fetch(`${EMPLOYEES_API_URL}${employeeId}/`, {
          method: 'DELETE',
        })
        if (response.ok) {
          ElMessage.success('员工删除成功')
          fetchEmployees()
        } else {
          const errorData = await response.json()
          ElMessage.error(errorData.detail || '删除员工失败')
        }
      } catch (error) {
        ElMessage.error('网络错误，请稍后重试')
      }
    })
    .catch(() => {
      // User cancelled
    })
}
</script>

<style scoped>
.page-container, .fill-card, :deep(.el-card__body), :deep(.el-table) {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}
:deep(.el-card__body) {
  padding: 0;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
