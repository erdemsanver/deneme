import json
from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET

# Contract — whoever implements this must write generate()
class ReportGeneratorInterface(ABC):
    @abstractmethod
    def generate(self, data: dict) -> str:
        pass

# Legacy system — cannot modify, comes from external library
class LegacyReportGenerator:
    def generate_report(self, data: dict) -> str:
        xml = "<report>\n"
        for key, value in data.items():
            xml += f"  <{key}>{value}</{key}>\n"
        xml += "</report>"
        return xml

# Adapter — wraps Legacy, converts XML to JSON
class LegacyReportAdapter(ReportGeneratorInterface):
    def __init__(self, legacy: LegacyReportGenerator):
        self._legacy = legacy  # save legacy to use later

    def generate(self, data: dict) -> str:
        # Step 1: Get XML from legacy
        xml_report = self._legacy.generate_report(data)
        # Step 2: Parse XML into Python object
        root = ET.fromstring(xml_report)
        result = {}
        for child in root:
            result[child.tag] = child.text
        # Step 3: Convert to JSON string and return
        return json.dumps(result)

# Dashboard — cannot modify, expects JSON
class AnalyticsDashboard:
    def display(self, json_data: str):
        data = json.loads(json_data)
        print("=== Analytics Dashboard ===")
        for key, value in data.items():
            print(f"  {key}: {value}")

# Clean usage
def show_sales_report():
    adapter = LegacyReportAdapter(LegacyReportGenerator())
    dashboard = AnalyticsDashboard()
    json_report = adapter.generate({"total_sales": 150000, "orders": 1234})
    dashboard.display(json_report)

def show_inventory_report():
    adapter = LegacyReportAdapter(LegacyReportGenerator())
    dashboard = AnalyticsDashboard()
    json_report = adapter.generate({"total_items": 5000, "low_stock": 45})
    dashboard.display(json_report)

if __name__ == "__main__":
    show_sales_report()
    show_inventory_report()

#Exo 2


from abc import ABC, abstractmethod

# Interface — sözleşme
class OrderComponent(ABC):
    @abstractmethod
    def get_cost(self) -> float:
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        pass

# Base order — temel sipariş
class BaseOrder(OrderComponent):
    def __init__(self, base_price: float):
        self._price = base_price
    
    def get_cost(self) -> float:
        return self._price
    
    def get_description(self) -> str:
        return f"Base price: {self._price}€"

# Decorator base class — tüm decorator'ların parent'ı
class OrderDecorator(OrderComponent):
    def __init__(self, order: OrderComponent):
        self._order = order  # sarılan nesne

# Express Shipping
class ExpressShippingDecorator(OrderDecorator):
    def get_cost(self) -> float:
        return self._order.get_cost() + 15.00
    
    def get_description(self) -> str:
        return self._order.get_description() + "\nExpress shipping: +15€"

# Insurance
class InsuranceDecorator(OrderDecorator):
    def get_cost(self) -> float:
        return self._order.get_cost() + self._order.get_cost() * 0.05
    
    def get_description(self) -> str:
        return self._order.get_description() + f"\nInsurance (5%): +{self._order.get_cost() * 0.05}€"

# Gift Wrap
class GiftWrapDecorator(OrderDecorator):
    def get_cost(self) -> float:
        return self._order.get_cost() + 5.00
    
    def get_description(self) -> str:
        return self._order.get_description() + "\nGift wrap: +5€"

# Discount
class DiscountDecorator(OrderDecorator):
    def __init__(self, order: OrderComponent, percent: float):
        super().__init__(order)
        self._percent = percent
    
    def get_cost(self) -> float:
        discount = self._order.get_cost() * (self._percent / 100)
        return self._order.get_cost() - discount
    
    def get_description(self) -> str:
        discount = self._order.get_cost() * (self._percent / 100)
        return self._order.get_description() + f"\nDiscount ({self._percent}%): -{discount}€"

# Premium Member
class PremiumMemberDecorator(OrderDecorator):
    def get_cost(self) -> float:
        return self._order.get_cost() * 0.90
    
    def get_description(self) -> str:
        discount = self._order.get_cost() * 0.10
        return self._order.get_description() + f"\nPremium member (10%): -{discount}€"

# Wrapping
if __name__ == "__main__":
    order = BaseOrder(100.00)
    order = ExpressShippingDecorator(order)
    order = InsuranceDecorator(order)
    order = GiftWrapDecorator(order)
    order = DiscountDecorator(order, percent=15)
    order = PremiumMemberDecorator(order)

    print(order.get_description())
    print(f"Total: {order.get_cost()}€")
```

---

## Output:
```
Base price: 100.0€
Express shipping: +15€
Insurance (5%): +5.75€
Gift wrap: +5€
Discount (15%): +18.11€
Premium member (10%): -10.88€
Total: 98.33€
