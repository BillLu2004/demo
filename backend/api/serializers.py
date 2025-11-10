from rest_framework import serializers
from .models import (
    Customer, Account, Transaction, Loan,
    Branch, Employee, Card, Beneficiary
)

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    class Meta:
        model = Employee
        fields = ['id', 'employee_id', 'name', 'position', 'branch', 'branch_name']
        extra_kwargs = {'branch': {'write_only': True}}

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'

class BeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiary
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone', 'created_at']

class AccountSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'account_id', 'customer', 'customer_name', 'balance', 'status', 'created_at']
        extra_kwargs = {'customer': {'write_only': True}}


class TransactionSerializer(serializers.ModelSerializer):
    to_account_number = serializers.CharField(write_only=True, required=False)
    from_account_id = serializers.CharField(source='from_account.account_id', read_only=True)
    to_account_id = serializers.CharField(source='to_account.account_id', read_only=True)


    class Meta:
        model = Transaction
        fields = [
            'id', 'from_account', 'to_account', 'to_account_number', 'amount', 'timestamp',
            'from_account_id', 'to_account_id'
        ]
        read_only_fields = ['to_account']
        extra_kwargs = {'from_account': {'write_only': True}}


    def create(self, validated_data):
        to_account_number = validated_data.pop('to_account_number', None)
        
        if not to_account_number:
            raise serializers.ValidationError("收款账号 (to_account_number) 不能为空。")

        try:
            to_account = Account.objects.get(account_id=to_account_number)
            validated_data['to_account'] = to_account
        except Account.DoesNotExist:
            raise serializers.ValidationError(f"账号为 {to_account_number} 的收款账户不存在。")

        from_account = validated_data['from_account']

        # --- NEW VALIDATION LOGIC ---
        if from_account.status != 'active':
            raise serializers.ValidationError("付款账户已被冻结，无法转出。")
        
        if to_account.status != 'active':
            raise serializers.ValidationError("收款账户已被冻结，无法接收款项。")
        # --- END NEW VALIDATION ---

        if from_account == to_account:
            raise serializers.ValidationError("不能给自己转账。")

        # In a real system, you'd also check for sufficient balance and update balances
        # within a database transaction.

        return super().create(validated_data)


class LoanSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Loan
        fields = ['id', 'customer', 'customer_name', 'amount', 'status', 'request_date', 'approval_date']
        extra_kwargs = {'customer': {'write_only': True}}
