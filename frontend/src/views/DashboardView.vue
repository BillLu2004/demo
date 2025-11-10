<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">仪表盘概览</h1>
      <span class="date-picker">
        <el-date-picker
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
        />
      </span>
    </div>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="今日活跃客户" :value="125" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="交易总额 (元)" :value="102400" :precision="2" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="新增贷款申请" :value="12" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="系统消息" :value="3">
            <template #suffix>
              <el-icon style="vertical-align: -0.125em"><ChatLineRound /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="quick-access-card" header="常用操作快捷入口">
      <el-button type="primary" size="large" @click="navigateAndAddCustomer">
        <el-icon class="el-icon--left"><User /></el-icon>新增客户
      </el-button>
      <el-button type="success" size="large" @click="router.push('/transactions')">
        <el-icon class="el-icon--left"><Money /></el-icon>发起转账
      </el-button>
      <el-button type="warning" size="large" @click="router.push('/loans')">
        <el-icon class="el-icon--left"><Coin /></el-icon>新建贷款申请
      </el-button>
      <el-button size="large" @click="router.push('/accounts')">
        <el-icon class="el-icon--left"><Postcard /></el-icon>查看账户列表
      </el-button>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useActionStore } from '@/stores/actions'

const router = useRouter()
const actionStore = useActionStore()

const navigateAndAddCustomer = () => {
  actionStore.triggerAddCustomer()
  router.push('/customers')
}
</script>

<style scoped>
.page-container {
  flex-grow: 1;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  color: #303133;
}

.stats-row {
  margin-bottom: 20px;
}

.quick-access-card .el-button {
  margin-right: 10px;
}
</style>
