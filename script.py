import requests
import json

def fetch_api_version_hash():
    url = "https://setup.rbxcdn.com/versionQTStudio"
    response = requests.get(url)
    response.raise_for_status()
    return response.text.strip()

def fetch_api_dump(version_hash):
    url = f"https://setup.rbxcdn.com/{version_hash}-API-Dump.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def extract_data(api_dump):
    result = {
        "Properties": {},
        "DataTypes": {},
        "Enums": {},
        "ClassHierarchy": {}
    }

    for class_info in api_dump['Classes']:
        class_name = class_info['Name']
        result["Properties"][class_name] = {}
        result["ClassHierarchy"][class_name] = class_info.get('Superclass')

        current_class = class_info
        while current_class:
            for member in current_class['Members']:
                if member['MemberType'] == 'Property':
                    if member['Security']['Read'] == 'None' and 'Deprecated' not in member.get('Tags', []):
                        prop_name = member['Name']
                        prop_type = member['ValueType']['Name']
                        result["Properties"][class_name][prop_name] = prop_type
                        
                        if prop_type not in result["DataTypes"]:
                            result["DataTypes"][prop_type] = {
                                "Category": member['ValueType']['Category']
                            }
            
            superclass = current_class.get('Superclass')
            current_class = next((c for c in api_dump['Classes'] if c['Name'] == superclass), None)
            
    for enum in api_dump['Enums']:
        enum_name = enum['Name']
        result["Enums"][enum_name] = {item['Name']: item['Value'] for item in enum['Items']}

    return result

def save_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    print("Fetching Roblox API version hash...")
    version_hash = fetch_api_version_hash()
    
    print("Fetching Roblox API dump...")
    api_dump = fetch_api_dump(version_hash)
    
    print("Extracting data...")
    extracted_data = extract_data(api_dump)
    
    print("Saving to file...")
    save_to_file(extracted_data, f'${version_hash}.json')
    
    print(f"Done! Extracted data for {len(extracted_data['Properties'])} classes.")

if __name__ == "__main__":
    main()
