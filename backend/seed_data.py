import os
import django
import random
from decimal import Decimal
from datetime import date, timedelta
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank_project.settings')
django.setup()

from api.models import Branch, Employee, Customer, Beneficiary, Account, Card, Loan, Transaction

fake = Faker('zh_CN') # Use Chinese data provider

def seed_all_data():
    print("Deleting old data...")
    # Clean up in reverse order of dependency
    Transaction.objects.all().delete()
    Loan.objects.all().delete()
    Card.objects.all().delete()
    Beneficiary.objects.all().delete()
    Account.objects.all().delete()
    Customer.objects.all().delete()
    Employee.objects.all().delete()
    Branch.objects.all().delete()

    # --- Seed Branches ---
    print("Seeding Branches...")
    branches = [Branch.objects.create(name=name, address=fake.address()) for name in ["总行营业部", "城东支行", "西城科技园支行"]]

    # --- Seed Employees ---
    print("Seeding Employees...")
    for i in range(5):
        Employee.objects.create(
            employee_id=f'E{i+1:03}',
            name=fake.name(),
            position=random.choice(['teller', 'manager']),
            branch=random.choice(branches)
        )

    # --- Seed Customers ---
    print("Seeding 20 Customers...")
    customers = [Customer.objects.create(name=fake.name(), email=fake.email()) for _ in range(20)]

    # --- Seed Accounts & Cards ---
    print("Seeding Accounts and Cards for each customer...")
    all_accounts = []
    for customer in customers:
        num_accounts = random.randint(1, 2)
        for _ in range(num_accounts):
            account = Account.objects.create(
                account_id=fake.credit_card_number(),
                customer=customer,
                balance=Decimal(random.uniform(100, 50000))
            )
            # Create one card for each account
            Card.objects.create(
                card_number=fake.credit_card_number(),
                account=account,
                card_type=random.choice(['debit', 'credit']),
                expiry_date=date.today() + timedelta(days=365*3)
            )
            all_accounts.append(account)
    
    # --- Seed Beneficiaries for first 5 customers ---
    print("Seeding Beneficiaries...")
    for customer in customers[:5]:
        beneficiary_customer = random.choice(customers)
        if beneficiary_customer != customer:
            beneficiary_account = random.choice(beneficiary_customer.accounts.all())
            Beneficiary.objects.create(
                owner=customer,
                name=beneficiary_customer.name,
                account_number=beneficiary_account.account_id,
                bank_name="本行"
            )

    # --- Seed Transactions ---
    print("Seeding 30 Transactions...")
    for _ in range(30):
        from_acc, to_acc = random.sample(all_accounts, 2)
        Transaction.objects.create(
            from_account=from_acc,
            to_account=to_acc,
            amount=Decimal(random.uniform(10, 5000))
        )

    # --- Seed Loans for first 10 customers ---
    print("Seeding Loans...")
    for customer in customers[:10]:
        Loan.objects.create(
            customer=customer,
            amount=Decimal(random.uniform(5000, 200000)),
            status=random.choice(['pending', 'approved', 'rejected'])
        )

    print("All new data seeded successfully!")

if __name__ == '__main__':
    seed_all_data()
