import requests
import json
import re
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def fetch_windows_player_version():
    url = "https://setup.roblox.com/DeployHistory.txt"
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        content = response.text

        pattern = r"New Studio64 version-([a-f0-9]+) at (\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2}:\d{2} [AP]M)"
        matches = re.findall(pattern, content)

        if not matches:
            raise ValueError("No WindowsPlayer versions found in DeployHistory.txt")

        versions = [(version, datetime.strptime(date_str, "%m/%d/%Y %I:%M:%S %p")) for version, date_str in matches]

        latest_version, _ = max(versions, key=lambda x: x[1])
        return f'version-{latest_version}'

    except requests.RequestException as e:
        raise RuntimeError(f"Error fetching DeployHistory.txt: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error processing DeployHistory.txt: {str(e)}")

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
    print("Fetching WindowsPlayer version hash...")
    version_hash = fetch_windows_player_version()
    
    print(f"Version hash: {version_hash}")
    
    print("Fetching Roblox API dump...")
    api_dump = fetch_api_dump(version_hash)
    
    print("Extracting data...")
    extracted_data = extract_data(api_dump)
    
    print("Saving to file...")
    save_to_file(extracted_data, f'{version_hash}.json')
    
    print(f"Done! Extracted data for {len(extracted_data['Properties'])} classes.")

if __name__ == "__main__":
    main()
