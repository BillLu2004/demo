from django.shortcuts import render
from rest_framework import viewsets
from .models import (
    Customer, Account, Transaction, Loan,
    Branch, Employee, Card, Beneficiary
)
from .serializers import (
    CustomerSerializer, AccountSerializer, TransactionSerializer, LoanSerializer,
    BranchSerializer, EmployeeSerializer, CardSerializer, BeneficiarySerializer
)
from django.db.models import Q

# Create your views here.

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        account_id = self.request.query_params.get('account_id')
        if account_id:
            queryset = queryset.filter(account_id=account_id)
        return queryset

class BeneficiaryViewSet(viewsets.ModelViewSet):
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        owner_id = self.request.query_params.get('owner_id')
        if owner_id:
            queryset = queryset.filter(owner_id=owner_id)
        return queryset

class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows customers to be viewed or edited.
    """
    queryset = Customer.objects.all().order_by('-created_at')
    serializer_class = CustomerSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all().order_by('-created_at')
    serializer_class = AccountSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('-timestamp')
    serializer_class = TransactionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        account_id = self.request.query_params.get('account_id')
        if account_id:
            queryset = queryset.filter(
                Q(from_account_id=account_id) | Q(to_account_id=account_id)
            )
        return queryset

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all().order_by('-request_date')
    serializer_class = LoanSerializer
