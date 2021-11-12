from src.internal import BarcodeService
from dotenv import dotenv_values

config = dotenv_values(".env.dev")

b = BarcodeService("barcode", config["PATH"])
# print(b.barcode)
print(b.mapBarcode("1001"))

