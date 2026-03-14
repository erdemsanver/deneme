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
