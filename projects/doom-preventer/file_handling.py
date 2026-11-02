import json

file_path = "detail.json"

file_data = {
    "name": "Rishit Katiyar",
    "age": 18,
    "fav_color": "green",
    "hobby": "reading",
}
try:
    with open(file_path, "w") as file:
        json.dump(file_data, file, indent=4)

    with open(file_path, "r") as file:
        r = json.load(file)

except FileNotFoundError:
    print(f"file not found at {file_path}.")
except json.JSONDecodeError:
    print(f"could not decode file.")


print(r)
