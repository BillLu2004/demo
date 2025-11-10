<script setup lang="ts">
import { RouterView, useRoute, useRouter } from 'vue-router'
import { ref, watch } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const menuRef = ref<any>(null)
let systemMenuAccessed = false;

watch(route, (to) => {
  if (to.path.startsWith('/employees') || to.path.startsWith('/branches')) {
    if (systemMenuAccessed) return;
    
    ElMessageBox.prompt('请输入管理员密码:', '权限验证', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      inputPattern: /.+/,
      inputErrorMessage: '密码不能为空',
    })
    .then(({ value }) => {
      if (value === '1234') {
        systemMenuAccessed = true;
        menuRef.value?.open('system-management');
      } else {
        ElMessage.error('密码错误！')
        router.push('/')
      }
    })
    .catch(() => {
      ElMessage.info('已取消访问')
      router.push('/')
    })
  } else {
    systemMenuAccessed = false;
    if(menuRef.value) menuRef.value.close('system-management');
  }
})
</script>

<template>
  <el-container class="layout-container">
    <el-header class="header">
      <div class="logo-container">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" class="logo-svg">
          <defs>
            <linearGradient id="appleGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" style="stop-color:#4A90E2;stop-opacity:1" />
              <stop offset="100%" style="stop-color:#50E3C2;stop-opacity:1" />
            </linearGradient>
          </defs>
          <rect x="5" y="5" width="90" height="90" rx="22" fill="url(#appleGradient)" />
          <text x="50" y="68" font-family="'Helvetica Neue', 'Arial', sans-serif" font-size="50" fill="white" text-anchor="middle" font-weight="300">SB</text>
        </svg>
        <div class="logo-text">Simple Bank 核心管理系统</div>
      </div>
      <div class="user-info">
        <span>当前员工: Admin</span>
        <el-button type="text">退出登录</el-button>
      </div>
    </el-header>

    <div class="menu-container">
      <el-menu :default-active="route.path" class="main-menu" mode="horizontal" router :ellipsis="false" ref="menuRef">
        <el-menu-item index="/">
          <el-icon><Menu /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/customers">
          <el-icon><User /></el-icon>
          <span>客户管理</span>
        </el-menu-item>
        <el-menu-item index="/accounts">
          <el-icon><Postcard /></el-icon>
          <span>账户管理</span>
        </el-menu-item>
        <el-menu-item index="/transactions">
          <el-icon><Money /></el-icon>
          <span>交易管理</span>
        </el-menu-item>
        <el-menu-item index="/loans">
          <el-icon><Coin /></el-icon>
          <span>贷款管理</span>
        </el-menu-item>
        <div class="flex-grow" />
        <el-sub-menu index="system-management">
          <template #title>
            <el-icon><Setting /></el-icon>
            <span>系统管理</span>
          </template>
          <el-menu-item index="/employees">员工管理</el-menu-item>
          <el-menu-item index="/branches">分行管理</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </div>

    <el-main class="main-content">
      <router-view></router-view>
    </el-main>
  </el-container>
</template>

<style scoped>
.layout-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', Arial, sans-serif;
  background-color: #f0f2f5;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #001529;
  color: white;
  padding: 0 50px;
  flex-shrink: 0;
  height: 60px;
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo-svg {
  width: 40px;
  height: 40px;
  margin-right: 15px;
}

.logo-text {
  font-size: 20px;
  font-weight: bold;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-info span {
  margin-right: 15px;
}

.user-info .el-button {
  color: white;
}

.menu-container {
  background-color: #fff;
  padding: 0 50px;
  border-bottom: solid 1px #e6e6e6;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  flex-shrink: 0;
}

.main-menu.el-menu--horizontal {
  border-bottom: none;
}

.main-content {
  flex-grow: 1;
  padding: 20px 50px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}
.flex-grow {
  flex-grow: 1;
}
</style>
