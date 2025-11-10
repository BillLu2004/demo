<template>
  <div>
    <h1>交易管理 (Transactions)</h1>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>交易流水</span>
          <el-button type="success" @click="openAddDialog">发起转账</el-button>
        </div>
      </template>
      <el-table :data="transactions" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="交易ID" width="100" />
        <el-table-column prop="from_account_id" label="付款账户" width="220" />
        <el-table-column prop="to_account_id" label="收款账户" width="220" />
        <el-table-column prop="amount" label="金额">
          <template #default="scope">
            ¥{{ parseFloat(scope.row.amount).toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="timestamp" label="交易时间">
          <template #default="scope">
            {{ new Date(scope.row.timestamp).toLocaleString() }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Transaction Dialog -->
    <el-dialog v-model="dialogVisible" title="发起转账" width="500" @close="resetForm">
      <el-form :model="form" label-width="100px">
        <el-form-item label="付款账户">
          <el-select v-model="form.from_account" placeholder="请选择付款账户" style="width: 100%;" @change="onFromAccountChange">
            <el-option
              v-for="account in accounts"
              :key="account.id"
              :label="`${account.customer_name} - ${account.account_id}`"
              :value="account.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="收款账户">
          <el-input v-model="form.to_account_number" placeholder="请输入收款账号">
            <template #append>
              <el-button @click="openBeneficiaryDialog" :disabled="!form.from_account">从名册选择</el-button>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="转账金额">
          <el-input v-model.number="form.amount" type="number" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleAddTransaction" :loading="formLoading">确认转账</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- Beneficiary Dialog -->
    <el-dialog v-model="beneficiaryDialogVisible" title="选择常用收款人" width="60%">
      <el-table :data="beneficiaries" @row-click="selectBeneficiary" style="cursor: pointer;">
        <el-table-column prop="name" label="收款人姓名" />
        <el-table-column prop="account_number" label="收款账号" />
        <el-table-column prop="bank_name" label="开户行" />
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';

// Component State
const dialogVisible = ref(false);
const beneficiaryDialogVisible = ref(false);
const loading = ref(true);
const formLoading = ref(false);

// Data
const transactions = ref<any[]>([]);
const accounts = ref<any[]>([]);
const beneficiaries = ref<any[]>([]);
const selectedFromAccount = ref<any>(null);

// API URLs
const TRANSACTIONS_API_URL = 'http://localhost:8000/api/transactions/';
const ACCOUNTS_API_URL = 'http://localhost:8000/api/accounts/';
const BENEFICIARIES_API_URL = 'http://localhost:8000/api/beneficiaries/';

// Form state
const form = ref({
  from_account: null as number | null,
  to_account_number: '',
  amount: 0,
});

// --- Data Fetching ---
const fetchTransactions = async () => {
  loading.value = true;
  try {
    const response = await fetch(TRANSACTIONS_API_URL);
    if (response.ok) {
      transactions.value = await response.json();
    } else {
      ElMessage.error('获取交易列表失败');
    }
  } catch (error) {
    ElMessage.error('网络错误，请稍后重试');
  } finally {
    loading.value = false;
  }
};

const fetchAccounts = async () => {
  try {
    const response = await fetch(ACCOUNTS_API_URL);
    if (response.ok) {
      accounts.value = await response.json();
    } else {
      ElMessage.error('获取账户下拉列表失败');
    }
  } catch (error) {
    ElMessage.error('网络错误，请稍后重试');
  }
};

const fetchBeneficiaries = async (ownerId: number) => {
  try {
    const response = await fetch(`${BENEFICIARIES_API_URL}?owner_id=${ownerId}`);
    if (response.ok) {
      beneficiaries.value = await response.json();
    } else {
      ElMessage.error('获取收款人名册失败');
    }
  } catch (error) {
    ElMessage.error('网络错误');
  }
};

onMounted(() => {
  fetchTransactions();
  fetchAccounts();
});

// --- Dialog and Form Logic ---
const resetForm = () => {
  form.value = { from_account: null, to_account_number: '', amount: 0 };
  selectedFromAccount.value = null;
};

const openAddDialog = () => {
  resetForm();
  dialogVisible.value = true;
};

const onFromAccountChange = (accountId: number) => {
  selectedFromAccount.value = accounts.value.find(acc => acc.id === accountId);
};

const openBeneficiaryDialog = async () => {
  if (!selectedFromAccount.value) {
    ElMessage.warning('请先选择付款账户');
    return;
  }
  beneficiaryDialogVisible.value = true;
  await fetchBeneficiaries(selectedFromAccount.value.customer);
};

const selectBeneficiary = (beneficiary: any) => {
  form.value.to_account_number = beneficiary.account_number;
  beneficiaryDialogVisible.value = false;
};

// --- API Actions ---
const handleAddTransaction = async () => {
  formLoading.value = true;
  try {
    const response = await fetch(TRANSACTIONS_API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value),
    });
    if (response.ok) {
      ElMessage.success('转账成功');
      dialogVisible.value = false;
      await fetchTransactions(); // Refresh list
    } else {
      const errorData = await response.json();
      const errorMessage = Object.values(errorData).flat().join('; ');
      ElMessage.error(`操作失败: ${errorMessage}`);
    }
  } catch (error) {
    ElMessage.error('网络错误，请稍后重试');
  } finally {
    formLoading.value = false;
  }
};
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
