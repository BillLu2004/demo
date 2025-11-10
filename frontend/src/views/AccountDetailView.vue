<template>
  <div class="page-container" v-if="account">
    <el-page-header @back="goBack" :content="`账户详情: ${account.account_id}`" />

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="8">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span><el-icon><Postcard /></el-icon> 账户信息</span>
            </div>
          </template>
          <div class="text item"><strong>客户姓名:</strong> {{ account.customer_name }}</div>
          <div class="text item"><strong>账户余额:</strong> ¥{{ parseFloat(account.balance).toFixed(2) }}</div>
          <div class="text item"><strong>账户状态:</strong> 
            <el-tag :type="account.status === 'active' ? 'success' : 'danger'">
              {{ account.status === 'active' ? '正常' : '冻结' }}
            </el-tag>
          </div>
          <div class="text item"><strong>开户日期:</strong> {{ new Date(account.created_at).toLocaleDateString() }}</div>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span><el-icon><CreditCard /></el-icon> 绑定的银行卡</span>
            </div>
          </template>
          <el-table :data="cards" height="150">
            <el-table-column prop="card_number" label="卡号" />
            <el-table-column prop="card_type" label="类型" />
            <el-table-column prop="expiry_date" label="有效期" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="box-card" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span><el-icon><Money /></el-icon> 交易记录</span>
        </div>
      </template>
       <el-table :data="transactions" height="250">
        <el-table-column prop="id" label="ID" width="60"/>
        <el-table-column label="类型" width="80">
          <template #default="scope">
            <el-tag :type="scope.row.from_account === account.id ? 'danger' : 'success'">
              {{ scope.row.from_account === account.id ? '转出' : '转入' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="对方账户" width="220">
            <template #default="scope">
                {{ scope.row.from_account === account.id ? scope.row.to_account_id : scope.row.from_account_id }}
            </template>
        </el-table-column>
        <el-table-column prop="amount" label="金额" />
        <el-table-column prop="timestamp" label="交易时间" />
      </el-table>
    </el-card>
  </div>
  <div v-else-if="loading">
      <p>加载中...</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const accountId = route.params.id

const account = ref<any>(null)
const cards = ref<any[]>([])
const transactions = ref<any[]>([])
const loading = ref(true)

const goBack = () => {
  router.push('/accounts')
}

onMounted(async () => {
  try {
    // Fetch account details
    const accResponse = await fetch(`http://localhost:8000/api/accounts/${accountId}/`)
    if(!accResponse.ok) throw new Error('账户信息加载失败')
    account.value = await accResponse.json()

    // Fetch associated cards
    const cardsResponse = await fetch(`http://localhost:8000/api/cards/?account_id=${accountId}`)
    if(cardsResponse.ok) cards.value = await cardsResponse.json()
    
    // Fetch associated transactions efficiently
    const transResponse = await fetch(`http://localhost:8000/api/transactions/?account_id=${accountId}`)
    if(transResponse.ok) {
        transactions.value = await transResponse.json();
    }

  } catch (error: any) {
    ElMessage.error(error.message || '数据加载失败')
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.page-container {
  padding: 20px;
}
.card-header {
  display: flex;
  align-items: center;
  font-weight: bold;
}
.card-header .el-icon {
  margin-right: 8px;
}
.text.item {
  padding: 8px 0;
}
</style>
