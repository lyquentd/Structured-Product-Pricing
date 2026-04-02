import re

rep_map = {
    # Rates
    "4.548%": "4.502%",
    "0.04548": "0.04502",
    "4.419%": "4.383%",
    "4489.6": "4482.1",
    
    # Values
    "76.118": "76.328",
    "76.12": "76.33",
    "1331.51": "1327.52",
    "657.97": "654.55",
    "2.30": "2.29",
    "21.01": "20.98",
    "21.006": "20.984",
    "97.12": "97.31",
    "97.124": "97.312",
    "2.88": "2.69",
    "2.876": "2.688",
    
    # Greeks/Sens
    "0.808": "0.616",
    "3.116": "2.925",
    "7.071": "6.807",
    "101.161": "101.284",
    "101.16": "101.28",
    "20.985": "20.970" # 101.284 - 80.314 = 20.970 (assuming MTM PV 5Y is roughly 80.314)
}

# Fix 5Y ZC: 100 * exp(-0.043825 * 5) = 80.322
rep_map["80.176"] = "80.322"
rep_map["20.985"] = "20.962" # 101.284 - 80.322

files = ["excel_fill_guide.md", "presentation_speech.md", "README.md"]

for file in files:
    try:
        with open(file, "r") as f:
            t = f.read()
        for k, v in rep_map.items():
            t = t.replace(k, v)
        with open(file, "w") as f:
            f.write(t)
    except:
        pass
