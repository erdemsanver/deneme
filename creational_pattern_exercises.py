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


