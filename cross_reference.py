# Helper script for creating the image filename to UUID mapping
# This is not actually executed.
 
import csv
import json
import os

# Define the path to the directory containing the JSON files
json_directory = "../pf2e/packs/pathfinder-monster-core"

# Function to process the monster name
def process_name(name):
    return name.lower().replace(" ", "-").replace("(","").replace(")","").replace("’","")

# Open and read the CSV file
with open("MonsterCore.csv", newline="") as csvfile:
    reader = csv.reader(csvfile)
    print("\"pathfinder-monster-core\": {");
    for row in reader:
        if row:
            monster_name = row[1]  # Assuming the monster name is in the second column
            if monster_name != '':
               processed_name = process_name(monster_name)
               json_file_path = os.path.join(json_directory, f"{processed_name}.json")

               # Check if the JSON file exists and read it
               if os.path.exists(json_file_path):
                   with open(json_file_path, "r") as jsonfile:
                       data = json.load(jsonfile)
                       if "_id" in data:
                           print("\t\"" + data['_id'] + "\": {")
                           print("\t\t\"actor\": \"modules/pf2e-monster-core-pdf-mapping/MonsterCoreImages/" +  monster_name + ".png\",")
                           print("\t\t\"token\": \"modules/pf2e-monster-core-pdf-mapping/MonsterCoreImages/" +  monster_name + ".png\"},")
                       else:
                           print(f"Data for monster {monster_name} does not contain an '_id'.")
               else:
                   print(f"JSON file for {monster_name} ({processed_name}.json) not found.")
    print("}")

