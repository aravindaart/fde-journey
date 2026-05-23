import requests

response = requests.get("https://wttr.in/Singapore?format=j1")
data = response.json()

current = data["current_condition"][0]
temp = current["temp_C"]
weather= current["weatherDesc"][0]["value"]

print(f"Singapore weather right now")
print(f"  Temperature: {temp}°C")
print(f"  Condition: {weather}")