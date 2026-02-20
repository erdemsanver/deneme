#exercise 1, factory
from abc import ABC, abstractmethod

# 1. ABC — Superclass
class PaymentProcessor(ABC):
    @abstractmethod
    def validate(self, details: dict) -> bool:
        pass
    
    @abstractmethod
    def process(self, amount: float, details: dict) -> dict:
        pass

# 2. Concrete Classes
class CreditCardProcessor(PaymentProcessor):
    def validate(self, details: dict) -> bool:
        card_number = details.get("card_number")
        cvv = details.get("cvv")
        if not card_number or len(card_number) != 16:
            return False
        if not cvv or len(cvv) != 3:
            return False
        return True
    
    def process(self, amount: float, details: dict) -> dict:
        if not self.validate(details):
            return {"success": False, "error": "Invalid card details"}
        fee = amount * 0.029
        total = amount + fee
        return {"success": True, "method": "credit_card", "amount": total, "fee": fee}

class BankTransferProcessor(PaymentProcessor):
    def validate(self, details: dict) -> bool:
        iban = details.get("iban")
        if not iban or len(iban) < 15:
            return False
        return True
    
    def process(self, amount: float, details: dict) -> dict:
        if not self.validate(details):
            return {"success": False, "error": "Invalid IBAN"}
        fee = 1.50
        total = amount + fee
        return {"success": True, "method": "bank_transfer", "amount": total, "fee": fee}

class PayPalProcessor(PaymentProcessor):
    def validate(self, details: dict) -> bool:
        email = details.get("email")
        if not email or "@" not in email:
            return False
        return True
    
    def process(self, amount: float, details: dict) -> dict:
        if not self.validate(details):
            return {"success": False, "error": "Invalid PayPal email"}
        fee = amount * 0.034 + 0.30
        total = amount + fee
        return {"success": True, "method": "paypal", "amount": total, "fee": fee}

# 3. Factory
class PaymentFactory:
    def __init__(self):
        self._processors = {
            "credit_card": CreditCardProcessor,
            "bank_transfer": BankTransferProcessor,
            "paypal": PayPalProcessor
        }
    
    def get_processor(self, payment_type: str) -> PaymentProcessor:
        processor = self._processors.get(payment_type)
        if not processor:
            raise ValueError(f"Unknown payment type: {payment_type}")
        return processor()

#how to use the code
factory = PaymentFactory()
processor = factory.get_processor("credit_card")
result = processor.process(100.0, {"card_number": "1234567890123456", "cvv": "123", "expiry": "12/25"})
print(result)


#Exercise 2 Builder

# 1. Product 
class Employee:
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.email = None
        self.department = None
        self.position = None
        self.salary = None
        self.has_laptop = False
        self.has_parking = False
        self.has_vpn = False
        self.has_admin = False

# 2. Builder
class EmployeeBuilder:
    def __init__(self):
        self._employee = Employee()  

    def with_name(self, first, last):
        self._employee.first_name = first
        self._employee.last_name = last
        return self  

    def with_email(self, email):
        self._employee.email = email
        return self

    def with_job(self, department, position, salary):
        self._employee.department = department
        self._employee.position = position
        self._employee.salary = salary
        return self

    def with_equipment(self, laptop=False, parking=False):
        self._employee.has_laptop = laptop
        self._employee.has_parking = parking
        return self

    def with_access(self, vpn=False, admin=False):
        self._employee.has_vpn = vpn
        self._employee.has_admin = admin
        return self

    def build(self):
        # validation
        if not self._employee.first_name:
            raise ValueError("name is required!")
        if not self._employee.email or "@" not in self._employee.email:
            raise ValueError("email is required!")
        return self._employee  

# 3. Preset Builder 
class DeveloperBuilder(EmployeeBuilder):
    def __init__(self, first, last, email):
        super().__init__()
        self.with_name(first, last)
        self.with_email(email)
        self.with_job("Engineering", "Developer", 75000)
        self.with_equipment(laptop=True)
        self.with_access(vpn=True, admin=True)

# how to use:
employee = (
    EmployeeBuilder()
    .with_name("John", "Doe")
    .with_email("john.doe@company.com")
    .with_job("Engineering", "Senior Developer", 75000)
    .with_equipment(laptop=True, parking=False)
    .with_access(vpn=True, admin=True)
    .build()
)

print(employee.first_name)   # John
print(employee.department)   # Engineering
print(employee.has_admin)    # True

