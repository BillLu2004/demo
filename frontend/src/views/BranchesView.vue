<template>
  <div class="page-container">
    <el-card class="fill-card">
      <template #header>
        <div class="card-header">
          <span>分行管理</span>
          <el-button type="primary" @click="openDialog()">
            <el-icon class="el-icon--left"><Plus /></el-icon>
            新增分行
          </el-button>
        </div>
      </template>
      <el-table :data="branches" style="width: 100%" stripe v-loading="loading">
        <el-table-column prop="name" label="分行名称" width="200" />
        <el-table-column prop="address" label="地址" />
        <el-table-column prop="phone_number" label="联系电话" width="200" />
        <el-table-column label="操作" width="200" align="center">
          <template #default="scope">
            <el-button size="small" type="primary" plain @click="openDialog(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" plain @click="handleDelete(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEditMode ? '编辑分行' : '新增分行'" width="500" @close="resetForm">
      <el-form :model="form" label-width="80px">
        <el-form-item label="分行名称">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="form.address" />
        </el-form-item>
        <el-form-item label="联系电话">
          <el-input v-model="form.phone_number" />
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

const branches = ref([])
const loading = ref(true)
const dialogVisible = ref(false)
const formLoading = ref(false)
const editingBranch = ref<any>(null)

const isEditMode = computed(() => !!editingBranch.value)
const API_URL = 'http://localhost:8000/api/branches/'

const form = ref({
  name: '',
  address: '',
  phone_number: '',
})

const fetchBranches = async () => {
  loading.value = true
  try {
    const response = await fetch(API_URL)
    if (response.ok) {
      branches.value = await response.json()
    } else {
      ElMessage.error('获取分行列表失败')
    }
  } catch (error) {
    ElMessage.error('网络错误，请稍后重试')
  } finally {
    loading.value = false
  }
}

onMounted(() => { fetchBranches() })

const resetForm = () => {
  form.value = { name: '', address: '', phone_number: '' }
  editingBranch.value = null
}

const openDialog = (branch: any = null) => {
  resetForm()
  if (branch) {
    editingBranch.value = branch
    form.value = { ...branch }
  }
  dialogVisible.value = true
}

const handleSubmit = () => {
  isEditMode.value ? handleUpdate() : handleAdd()
}

const handleAdd = async () => {
  formLoading.value = true
  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value),
    })
    if (response.ok) {
      ElMessage.success('新增分行成功')
      dialogVisible.value = false
      await fetchBranches()
    } else {
      const errorData = await response.json()
      ElMessage.error(`新增失败: ${JSON.stringify(errorData)}`)
    }
  } catch (error) {
    ElMessage.error('网络错误')
  } finally {
    formLoading.value = false
  }
}

const handleUpdate = async () => {
  formLoading.value = true
  try {
    const response = await fetch(`${API_URL}${editingBranch.value.id}/`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value),
    })
    if (response.ok) {
      ElMessage.success('更新分行成功')
      dialogVisible.value = false
      await fetchBranches()
    } else {
      const errorData = await response.json()
      ElMessage.error(`更新失败: ${JSON.stringify(errorData)}`)
    }
  } catch (error) {
    ElMessage.error('网络错误')
  } finally {
    formLoading.value = false
  }
}

const handleDelete = async (branchId: number) => {
  await ElMessageBox.confirm('您确定要删除该分行吗？', '警告', {
    confirmButtonText: '确定删除',
    cancelButtonText: '取消',
    type: 'warning',
  })
  try {
    const response = await fetch(`${API_URL}${branchId}/`, { method: 'DELETE' })
    if (response.ok) {
      ElMessage.success('删除分行成功')
      await fetchBranches()
    } else {
      ElMessage.error('删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') ElMessage.error('网络错误')
  }
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
