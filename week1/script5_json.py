import json

with open('week1/menu.json', 'r') as file:
    data = json.load(file)

print(f"Shop: {data['shop']}")
print("Menu items:")
for item in data["items"]:
    print(f"  - {item['name']}| ${item['price']:.2f}")