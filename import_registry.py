"""
Imports the HexDebugData pattern registry.
Ensure that the registry is named registry.json, and that the folder import_reg_out exists.
To then load the results into the main program, copy all the files in import_reg_out into the data folder. 
(We have it load into import_reg_out to ensure there's no accidental overwriting of player-defined files.)
"""

import json
import sys
import re

if __name__ == "__main__":
    print("Reading registry.json...")
    with open("registry.json", 'r') as file:
        json_file = file.read()
    json_dict = json.loads(json_file)

    # Keys: Mod names
    # Values: Lists of patterns
    file_outputs = dict()

    # detect mod name
    modname_regex = re.compile(".*:")

    print("Parsing json...")
    for pattern_entry in json_dict['patterns'].values():
        # Get the mod name. We search for the part of the string before the colon, and cut the colon.
        mod_name = re.search(modname_regex, pattern_entry['id']).group(0)[:-1]

        # Add the data for this pattern to the corresponding output.
        if not mod_name in file_outputs:
            file_outputs[mod_name] = ""
        file_outputs[mod_name] += pattern_entry['name'] + ',' + pattern_entry['signature'] + '\n'


    # The data for each mod is written as mod_name.csv into import_reg_out (ex: hexcasting.csv).
    print ("Writing files...")
    for mod_name, data in file_outputs.items():
        with open('import_reg_out/' + mod_name + ".csv", 'w') as file:
            file.write(data)

    print(f"Wrote files for {file_outputs.__len__()} mods.")
