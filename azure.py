from azure.ai.formrecognizer import DocumentModelAdministrationClient, DocumentAnalysisClient
from openpyxl import Workbook

# Replace with your endpoint and key
endpoint = "YOUR_ENDPOINT"
key = "YOUR_KEY"

# Instantiate clients
model_admin_client = DocumentModelAdministrationClient(endpoint, key)
client = DocumentAnalysisClient(endpoint, key)

# Specify pre-built layout model
model_id = "prebuilt-layout"

# Analyze your image (replace with your image path)
with open("path/to/your/image.jpg", "rb") as f:
    poller = client.analyze_document(model_id, f)
    result = poller.result()

# Create workbook and worksheet
wb = Workbook()
ws = wb.active

# Process and save extracted tables
row_index = 1
for page in result.pages:
    for table in page.tables:
        # Iterate through rows and columns
        for row in range(table.row_count):
            for col in range(table.column_count):
                # Get cell text and write to spreadsheet
                cell = table.cells[row*table.column_count + col]
                ws.cell(row=row_index, column=col+1).value = cell.text
            row_index += 1

# Save workbook
wb.save("extracted_tables.xlsx")

print("Tables extracted and saved to extracted_tables.xlsx!")
