from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import (
    CustomerViewSet, AccountViewSet, TransactionViewSet, LoanViewSet,
    BranchViewSet, EmployeeViewSet, CardViewSet, BeneficiaryViewSet
)

router = SimpleRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'loans', LoanViewSet)
router.register(r'branches', BranchViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'cards', CardViewSet)
router.register(r'beneficiaries', BeneficiaryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
