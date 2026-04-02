import re

# Update presentation_speech.md
with open("presentation_speech.md", "r") as f:
    text = f.read()

text = text.replace("Short 160% Cap Call", "Short 150% Cap Call and a Long 10% Digital Call")
text = text.replace("23.5% at the Cap", "24.0% at the Cap")
text = text.replace("€21.30", "€21.01")
text = text.replace("€97.42", "€97.12")
text = text.replace("2.58%", "2.88%")
text = text.replace("5,760", "5,400")
text = text.replace("160%", "150%")
text = text.replace("€0.51", "€0.81")
text = text.replace("€6.74", "€7.07")
text = text.replace("€101.40", "€101.16")
text = text.replace("three exact Lego blocks", "four exact Lego blocks")
text = text.replace("and a Short 160% Cap Call", "a Short 150% Cap Call, and a Digital Call jumping 10%")

with open("presentation_speech.md", "w") as f:
    f.write(text)

# Update excel_fill_guide.md
with open("excel_fill_guide.md", "r") as f:
    guide = f.read()

guide = guide.replace("three", "four")
guide = guide.replace("Lego 3:", "Lego 3 (Sell Cap) and Lego 4 (Digital) :")
guide = guide.replace("5760", "5400").replace("160%", "150%")
guide = guide.replace("23.55%", "24.00%")
guide = guide.replace("564.68", "657.97")
guide = guide.replace("21.30", "21.01")
guide = guide.replace("97.42", "97.12")
guide = guide.replace("2.58", "2.88")
guide = guide.replace("0.515", "0.808")
guide = guide.replace("2.815", "3.116")
guide = guide.replace("6.744", "7.071")
guide = guide.replace("101.404", "101.161")
guide = guide.replace("21.229", "20.985") # 101.161 - 80.176
# Add digital line context
c_line = guide.find("Price: **657.97**")
if c_line != -1:
    guide = guide[:c_line+17] + " \n  - **Lego 4 (Digital Buy) :** Strike: 5400 | Payout: 10 | Vol: 24.00% | Price: **2.30**" + guide[c_line+17:]

with open("excel_fill_guide.md", "w") as f:
    f.write(guide)
