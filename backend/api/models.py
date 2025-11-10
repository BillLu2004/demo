from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

# Create your models here.

class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    POSITION_CHOICES = [
        ('teller', '柜员'),
        ('manager', '经理'),
        ('admin', '系统管理员'),
    ]
    employee_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    
    def __str__(self):
        return f"{self.name} ({self.employee_id})"

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Beneficiary(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='beneficiaries')
    name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    bank_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.owner.name}'s beneficiary: {self.name}"

class Account(models.Model):
    ACCOUNT_STATUS_CHOICES = [
        ('active', '正常'),
        ('frozen', '冻结'),
        ('closed', '已关闭'),
    ]
    
    account_id = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='accounts')
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=ACCOUNT_STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.account_id}"

class Card(models.Model):
    CARD_TYPE_CHOICES = [
        ('debit', '借记卡'),
        ('credit', '信用卡'),
    ]
    card_number = models.CharField(max_length=19, unique=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='cards')
    card_type = models.CharField(max_length=10, choices=CARD_TYPE_CHOICES)
    expiry_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.card_number} ({self.get_card_type_display()})"

class Transaction(models.Model):
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='outgoing_transactions')
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='incoming_transactions')
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.from_account.account_id} to {self.to_account.account_id} - {self.amount}"

class Loan(models.Model):
    LOAN_STATUS_CHOICES = [
        ('pending', '待审批'),
        ('approved', '已批准'),
        ('rejected', '已拒绝'),
        ('paid', '已还清'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=10, choices=LOAN_STATUS_CHOICES, default='pending')
    request_date = models.DateTimeField(auto_now_add=True)
    approval_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.customer.name} - {self.amount} - {self.status}"