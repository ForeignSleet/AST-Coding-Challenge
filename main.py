import json
import sys

#removes the unit and converts to an int
def conv_int(input):
    if input[-1:] == "g":
        return int(input[:-1])
    elif input[-2:] == "KG":
        return int(float(input[:-2]))*1000
    else:
        raise ValueError("unrecognised weight unit")

files = sys.argv[1:]

#setting variables
files_processed = 0
total_instructions = 0
equipment = []
materials = []
exp_weight = 0
total_weight_added = 0

for file_name in files:
    try:
        with open(file_name, "r") as current_file:
            parsed_file = json.load(current_file)
            intructions = parsed_file.get("instructions")

            files_processed += 1
            exp_weight += conv_int((parsed_file.get("metadata")).get("expected_weight"))

            for instr in intructions:
                total_instructions += 1
                if "weight_added" in instr:
                    total_weight_added += conv_int(instr.get("weight_added"))

                current_equipment = instr.get("equipment")
                for equip in current_equipment:
                    if equip != None:
                        if equip not in equipment:
                            equipment.append(equip)

                if instr.get("material") != None:
                    if instr.get("material") not in materials:
                        materials.append(instr.get("material"))
            current_file.close()
    
    except FileNotFoundError:
        raise FileNotFoundError(file_name + " not found")

#formatting the output as Summary.txt
with open("Summary.txt", "w") as output:
    output.write("Summary\n")
    output.write("==================\n")
    output.writelines(["Total files processed: ", str(files_processed), "\n"])
    output.writelines(["Total instructions: ", str(total_instructions), "\n"])

    output.writelines(["Equipment: ["])
    for equip in equipment:
        output.write(equip)
        if equipment.index(equip) != len(equipment) - 1:
            output.write(", ")
    output.write("]\n")

    output.writelines(["Materials: ["])
    for mat in materials:
        output.write(mat)
        if materials.index(mat) != len(materials) - 1:
            output.write(", ")
    output.write("]\n")
    
    output.writelines(["Total expected weight: ", str(exp_weight), "\n"])
    output.writelines(["Total weight added in grams: ", str(total_weight_added), "\n"])
    
    output.close()

print("Summary.txt generated successfully")

