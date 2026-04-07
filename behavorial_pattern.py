import json
import time
from abc import ABC, abstractmethod


# ================================
# STRATEGY PATTERN (REPORT FORMATS)
# ================================

class ReportFormatStrategy(ABC):
    # We define a common contract for all formats
    # So no matter what format we use, system behaves the same
    @abstractmethod
    def generate(self, data: list[dict]) -> str:
        pass

    @abstractmethod
    def get_file_extension(self) -> str:
        pass


class PDFFormatStrategy(ReportFormatStrategy):
    # Here we generate a PDF-like text report
    def generate(self, data: list[dict]) -> str:
        report = "PDF REPORT\n"
        report += "=" * 50 + "\n"
        for item in data:
            # We format each row nicely like a table
            report += f"| {item['name']:20} | {item['value']:10} |\n"
        report += "=" * 50 + "\n"
        report += "End of PDF Report"
        return report

    def get_file_extension(self) -> str:
        return "pdf"


class CSVFormatStrategy(ReportFormatStrategy):
    # Here we generate a CSV format (simple comma separated)
    def generate(self, data: list[dict]) -> str:
        report = "name,value\n"
        for item in data:
            report += f"{item['name']},{item['value']}\n"
        return report

    def get_file_extension(self) -> str:
        return "csv"


class JSONFormatStrategy(ReportFormatStrategy):
    # We convert Python data directly into JSON
    def generate(self, data: list[dict]) -> str:
        return json.dumps(data, indent=2)

    def get_file_extension(self) -> str:
        return "json"


class HTMLFormatStrategy(ReportFormatStrategy):
    # We generate an HTML table (for web display)
    def generate(self, data: list[dict]) -> str:
        report = "<html>\n<body>\n"
        report += "<h1>HTML REPORT</h1>\n"
        report += "<table border='1'>\n"
        report += "  <tr><th>Name</th><th>Value</th></tr>\n"
        for item in data:
            report += f"  <tr><td>{item['name']}</td><td>{item['value']}</td></tr>\n"
        report += "</table>\n</body>\n</html>"
        return report

    def get_file_extension(self) -> str:
        return "html"


class ReportGenerator:
    def __init__(self, data: list[dict], strategy: ReportFormatStrategy = None):
        self.data = data
        self.strategy = strategy

    def set_strategy(self, strategy: ReportFormatStrategy):
        # Here we dynamically change behavior at runtime
        # We can switch from JSON → CSV → HTML anytime
        self.strategy = strategy

    def generate_report(self) -> str:
        if not self.strategy:
            raise ValueError("No strategy set")
        # We delegate the work to the selected strategy
        return self.strategy.generate(self.data)

    def save_report(self, filename: str):
        # We generate the content first
        content = self.generate_report()
        # Then we get correct file extension from strategy
        ext = self.strategy.get_file_extension()

        # We save the file using the selected format
        with open(f"{filename}.{ext}", "w") as f:
            f.write(content)


# ================================
# TEMPLATE METHOD PATTERN (PIPELINES)
# ================================

class DataPipeline(ABC):
    def __init__(self, source: str):
        self.source = source
        self.data = None

    def run(self):
        # This is the TEMPLATE METHOD
        # We define the full pipeline flow once
        # And all subclasses must follow this order
        self.connect()
        self.extract()
        self.transform()
        self.validate()
        self.load()
        self.cleanup()
        return f"{self.get_pipeline_name()} pipeline finished"

    @abstractmethod
    def connect(self): pass

    @abstractmethod
    def extract(self): pass

    @abstractmethod
    def transform(self): pass

    @abstractmethod
    def validate(self): pass

    def load(self):
        # Shared logic (same for all pipelines)
        print("Loading data...")
        time.sleep(0.3)
        print(f"Loaded {len(self.data)} records")

    def cleanup(self):
        # Shared cleanup step
        print("Cleaning up...")
        self.data = None

    @abstractmethod
    def get_pipeline_name(self): pass


class CSVPipeline(DataPipeline):
    def connect(self):
        print(f"Connecting CSV: {self.source}")

    def extract(self):
        # We simulate reading CSV
        self.data = [
            {"id": 1, "name": "Alice", "age": 30},
            {"id": 2, "name": "Bob", "age": 25}
        ]

    def transform(self):
        # We modify data (business logic)
        for r in self.data:
            r["name"] = r["name"].upper()

    def validate(self):
        print("CSV validated")

    def get_pipeline_name(self):
        return "CSV"


class APIPipeline(DataPipeline):
    def connect(self):
        print(f"Connecting API: {self.source}")

    def extract(self):
        # Simulating API response
        self.data = [
            {"user": "john", "score": 90},
            {"user": "emma", "score": 80}
        ]

    def transform(self):
        # We enrich data (add new field)
        for r in self.data:
            r["grade"] = "A" if r["score"] > 85 else "B"

    def validate(self):
        print("API validated")

    def get_pipeline_name(self):
        return "API"


# ================================
# MAIN
# ================================

if __name__ == "__main__":
    # Sample data
    data = [
        {"name": "Q1", "value": 100},
        {"name": "Q2", "value": 200}
    ]

    generator = ReportGenerator(data)

    print("=== JSON ===")
    # We choose JSON strategy here
    generator.set_strategy(JSONFormatStrategy())
    print(generator.generate_report())

    print("\n=== HTML ===")
    # Now we switch behavior without changing core logic
    generator.set_strategy(HTMLFormatStrategy())
    print(generator.generate_report())

    # We save file using current strategy (HTML)
    generator.save_report("report")

    print("\n--- PIPELINES ---\n")

    # Running CSV pipeline
    csv = CSVPipeline("users.csv")
    print(csv.run())

    # Running API pipeline
    api = APIPipeline("api/url")
    print(api.run())
