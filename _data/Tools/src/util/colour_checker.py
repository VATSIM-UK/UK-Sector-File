import csv, glob,os,re,subprocess,sys
from PIL import Image, ImageDraw, ImageFont
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
main_dir = os.path.join(current_dir, os.pardir, os.pardir, os.pardir, os.pardir)
os.chdir(main_dir)
print(main_dir)
def conv_rgb(colour : int) -> tuple[int,int,int]:
    red = int(colour) & 0xff
    green = (int(colour) >> 8) & 0xff
    blue = (int(colour) >> 16) & 0xff
    return red,green,blue

to_compress = {
    ("smrBuilding", "smrDisused", "smrRunway", "smrTaxiway", "blackBackground") : "black",
    ("smrHHcompass",) : "smrCompassbase",
    ("smrGDtaxiway", "smrJJtaxiway", "smrSCOTaxiway", "smrMilTaxiway") : "smrTaxiwayDarker",
    ("smrGDrunway", "smrSCORunway") : "smrGrey",
    ("smrMilRoad",) : "smrRoad",
    ("smrBlue", "blueBackground") : "smrBlue",
    ("smrSCOGrass",) : "smrGreen",
    ("smrPFApron", "smrPFHoldLabels") : "smrPFGreyDark",
    ("smrPFRwyOuter","smrPFStandLabels") : "smrPFGreyLight",
    ("smrMDapron","smrMDrunway") : "smrMDGreyLight",
    ("smrFISGrass",) : "smrGrass3",

    ("smrNTapron",) : "smrApron",
    ("apron",) : "smrApron2",
    ("arrester",) : "smrArrester",
    ("building",) : "smrBuilding",
    ("Edge",) : "smrEdge",
    ("grass",) : "smrGrass3",
    ("grey",) : "smrGrey2",
    ("runway",) : "smrRunway",
    ("standHold",) : "smrStandHold",
    ("taxiway",) : "smrTaxiway",
    ("terminal",) : "smrTerminal",
    ("water",) : "smrWater",
}


flattened_map = {name.lower(): value for keys, value in to_compress.items() for name in keys}


def check() -> None:
    print("Scanning...")
    with open("Colours.txt", "r")as f:
        data = f.read().splitlines()
    colours = {}
    defs = {}

    for d in data:
        if d.startswith("#define"): # is colour
            d = d.split()
            colours[d[1]] = -1
            if d[2] not in defs:
                defs[d[2]] = [d[1]]
            else:
                defs[d[2]].append(d[1])

    with open(".bin/UK.sct","r")as sct:
        data = sct.read().splitlines()
    data = [item for sublist in [d.split(" ") for d in data] for item in sublist]

    for d in data:
        if d in colours:
            colours[d] += 1

    sorted_colours = {k: v for k, v in sorted(colours.items(), key=lambda item: item[1])}
    sorted_defs = {k: v for k, v in sorted(defs.items(), key=lambda item: len(item[1]),reverse=True)}

    with open('colours.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Colour', 'Value'])
        for key, value in sorted_colours.items():
            writer.writerow([key, value])

    with open("defs.csv","w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Colour', 'Names'])
        for key, value in sorted_defs.items():
            writer.writerow([key, value])

    print("Done")

def sort_colours() -> None:                 
    with open("Colours.txt","r")as in_file:
        data = in_file.readlines()

    original_defs = {}
    

    


    data.insert(0, ";Misc\n")
    replaced_lines = []
    for line in data:
        if line.startswith("#define"):
            _, col, def_ =  line.split(" ")
            original_defs[col] = def_
            if col.lower() in flattened_map:
                col = flattened_map[col.lower()]
            line = line = " ".join(("#define",col,def_))
        replaced_lines.append(line)

    
    
    section_pattern = re.compile(r'^;(\S.*$)')
    sections = {}
    current_section = ""
    comments = {}
    for line in replaced_lines:
        match = section_pattern.match(line)
        if match:
            current_section = match.group(0)
            sections[current_section] = []
        else:
            if line.strip().startswith('; @preserveComment'):
                if sections[current_section]:
                    last_line = sections[current_section][-1]
                    comments.setdefault(last_line, []).append(line.strip())
            else:
                sections[current_section].append(line.strip())

    fixed_sections = {
        ";Misc" :set(),
        ";SMR Colours" : set(),
    }
    for col_defs in sections.values():
        for col in col_defs:
            if col:
                _, name, def_ =  col.split(" ")
                if name.startswith("smr"):
                    fixed_sections[";SMR Colours"].add(" ".join(("#define",name,def_)))
                else:
                    fixed_sections[";Misc"].add(" ".join(("#define",name,def_)))
    

    sorted_sections = {}
    for section, lines in fixed_sections.items():
        sorted_lines = sorted(lines, key=lambda x: x.lower())
        sorted_sections[section] = []
        for line in sorted_lines:
            sorted_sections[section].append(line)
            if line in comments:
                sorted_sections[section].extend(comments[line])

        
    lines = []
    prev_line ="a b c"
    for i,section in enumerate(sorted_sections):
        if i != 0:
            lines.append(f"\n{section}\n")
        for line in sorted_sections[section]:
            if line != "":
                
                if prev_line.split(" ")[1] == line.split(" ")[1]:
                    if prev_line.split(" ")[1] in original_defs:
                        lines.pop()
                        lines.append(f"#define {prev_line.split(' ')[1]} {original_defs[prev_line.split(' ')[1]]}")
                else:
                    lines.append(f"{line}\n")
            prev_line = line
            


    
    with open("Colours.txt", "w") as file:
        file.writelines(lines)
        
def remove_unused() -> None:
    check()
    to_remove = set() # not used colours
    with open("colours.csv","r")as file:
        csv_reader = csv.reader(file)
        _ = next(csv_reader)
        for row in csv_reader:
            if int(row[1]) == 0:
                to_remove.add(row[0])

    with open("Colours.txt", "r")as f:
        data = f.read().splitlines()

    with open("Colours.txt","w")as out_file:
        for line in data:
            if line.startswith("#define"): # colour
                line_split = line.split(" ")
                if line_split[1] not in to_remove:
                    out_file.write(f"{line}\n")
            else:
                out_file.write(f"{line}\n")

def compress_colours() -> None:
    prev_line = ""

    print("Processing Airports")
    for root,dirs,_ in os.walk("Airports"):
        if "SMR" in dirs:
            path = os.path.join(root,"SMR")
            for smr_file in os.listdir(path):
                file_path = os.path.join(path, smr_file)
                if os.path.isfile(file_path):
                    type_ = file_path.split("\\")[-1].split(".")[0]
                    with open(file_path,"r")as in_file:
                        data = in_file.read().splitlines()
                    with open(file_path,"w")as out_file:
                        for line in data:
                            if type_ == "Geo" or type_ == "Labels":
                               if not line.startswith(";") and line != "":
                                content ,_ ,_ = line.partition(";")
                                colour = content.split()[-1]
                                if colour.lower() in flattened_map:
                                    line = line.replace(colour,flattened_map[colour.lower()])
                            elif type_ == "Regions":
                                if prev_line.startswith("REGIONNAME"):
                                    colour = line.split(" ")[0]
                                    if colour.lower() in flattened_map:
                                        line = line.replace(colour, flattened_map[colour.lower()])
                                prev_line = line

                            out_file.write(f"{line}\n")

    print("Processing Closed Airfields")
    for root,dirs,_ in os.walk("_data\Closed Airfields"):
        if "Ground Map" in dirs:
            path = os.path.join(root,"Ground Map")
            for smr_file in os.listdir(path):
                file_path = os.path.join(path, smr_file)
                if os.path.isfile(file_path):
                    type_ = file_path.split("\\")[-1].split(".")[0]
                    with open(file_path,"r")as in_file:
                        data = in_file.read().splitlines()
                    with open(file_path,"w")as out_file:
                        for line in data:
                            if type_ == "Geo" or type_ == "Labels":
                                if not line.startswith(";") and line != "":
                                    content ,_ ,_ = line.partition(";")
                                    colour = content.split()[-1]
                                    if colour.lower() in flattened_map:
                                        line = line.replace(colour,flattened_map[colour.lower()])
                            elif type_ == "Regions":
                                if prev_line.startswith("REGIONNAME"):
                                    colour = line.split(" ")[0]
                                    if colour.lower() in flattened_map:
                                        line = line.replace(colour, flattened_map[colour.lower()])
                                prev_line = line

                            out_file.write(f"{line}\n")
    
    print("Processing Misc")
    for path in glob.glob(os.path.join("Misc Geo", "*txt")):
        with open(path,"r")as in_file:
            data = in_file.read().splitlines()
        with open(path, "w")as out_file:
            for line in data:
                if not line.startswith(";") and line != "":
                    content ,_ ,_ = line.partition(";")
                    colour = content.split()[-1]
                    if colour.lower() in flattened_map:
                        line = line.replace(colour,flattened_map[colour.lower()])
                out_file.write(f"{line}\n")

    for path in glob.glob(os.path.join("Misc Other", "*txt")):
        with open(path,"r")as in_file:
            data = in_file.read().splitlines()
        with open(path, "w")as out_file:
            for line in data:
                if not line.startswith(";") and line != "":
                    content ,_ ,_ = line.partition(";")
                    colour = content.split()[-1]
                    if colour.lower() in flattened_map:
                        line = line.replace(colour,flattened_map[colour.lower()])
                out_file.write(f"{line}\n")

    for path in glob.glob(os.path.join("Misc Regions", "*txt")):
        with open(path,"r")as in_file:
            data = in_file.read().splitlines()
        with open(path, "w")as out_file:
            for line in data:
                if prev_line.startswith("REGIONNAME"):
                    colour = line.split()[0]
                    if colour.lower() in flattened_map:
                        line = line.replace(colour, flattened_map[colour.lower()])
                prev_line = line

                out_file.write(f"{line}\n")
    
    print("Colours Merged")

def remove_blank_ends() -> None:

    for root,dirs,_ in os.walk("Airports"):
        if "SMR" in dirs:
            smr_path = os.path.join(root,"SMR")
            for smr_file in os.listdir(smr_path):
                file_path = os.path.join(smr_path, smr_file)
                if os.path.isfile(file_path):
                    with open(file_path,"r")as file:
                        lines = file.readlines()
                    for i in range(len(lines) - 1, -1, -1):
                        if lines[i].strip():
                            break
                    lines = lines[:i+1]
                    with open(file_path, 'w') as file:
                        for i, line in enumerate(lines):
                            if i < len(lines) - 1:
                                file.write(line)
                            else:
                                file.write(line.rstrip('\n'))


    for root,dirs,_ in os.walk("_data\Closed Airfields"):
        if "Ground Map" in dirs:
            smr_path = os.path.join(root,"Ground Map")
            for smr_file in os.listdir(smr_path):
                file_path = os.path.join(smr_path, smr_file)
                if os.path.isfile(file_path):
                    with open(file_path,"r")as file:
                        lines = file.readlines()
                    for i in range(len(lines) - 1, -1, -1):
                        if lines[i].strip():
                            break
                    lines = lines[:i+1]
                    with open(file_path, 'w') as file:
                        for i, line in enumerate(lines):
                            if i < len(lines) - 1:
                                file.write(line)
                            else:
                                file.write(line.rstrip('\n'))

    for path in glob.glob(os.path.join("Misc Geo","*txt")):
        with open(path,"r")as file:
            lines = file.readlines()
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip():
                break
        lines = lines[:i+1]
        with open(path, 'w') as file:
            for i, line in enumerate(lines):
                if i < len(lines) - 1:
                    file.write(line)
                else:
                    file.write(line.rstrip('\n'))

    for path in glob.glob(os.path.join("Misc Other","*txt")):
        with open(path,"r")as file:
            lines = file.readlines()
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip():
                break
        lines = lines[:i+1]
        with open(path, 'w') as file:
            for i, line in enumerate(lines):
                if i < len(lines) - 1:
                    file.write(line)
                else:
                    file.write(line.rstrip('\n'))

    for path in glob.glob(os.path.join("Misc Regions","*txt")):
        with open(path,"r")as file:
            lines = file.readlines()
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip():
                break
        lines = lines[:i+1]
        with open(path, 'w') as file:
            for i, line in enumerate(lines):
                if i < len(lines) - 1:
                    file.write(line)
                else:
                    file.write(line.rstrip('\n'))


    print("Removed Blank Ends")

def are_colours_close(col1 : int, col2: int, threshold : int = 1) -> bool:
    if col1 == col2:
        return 0
    rgb1 = conv_rgb(col1)
    rgb2 = conv_rgb(col2)
    return sum((a-b) ** 2 for a,b in zip(rgb1,rgb2))** 0.5 <= threshold

def compile_sf() -> bool:
    command = r" .\cli-windows-x64.exe --config-file ./compiler.config.json --no-wait"
    process = subprocess.run(command,shell=True)
    if process.returncode == 0:
        print("SF compiled Succesfully")
        return 1
    else:
        print("There was an error")
        return 0

def create_color_block(rgb : tuple[int,int,int], width : int =100, height : int =100) -> Image:
    return Image.new("RGB", (width, height), color=rgb)

def close_colours(display : bool = False) -> None:
    close = []
    with open("Colours.txt","r")as file:
        data = file.read().splitlines()
    colours = [(line.split()[-2], line.split()[-1]) for line in data if line.startswith("#define")]
    for i,(name1,colour1) in enumerate(colours):
        for name2,colour2 in colours[i+1:]:
            if are_colours_close(colour1,colour2):
                close.append((name1,conv_rgb(colour1),name2,conv_rgb(colour2)))

    # with open("Close_Colours.txt","w")as file:
    #     for pair in close:
    #         file.write(f"{pair}\n")

    if display:
        img_width = 800
        total_height = len(close) * 100
        img = Image.new('RGB', (img_width, total_height), "white")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf",20)
        for index, (name1, rgb1, name2, rgb2) in enumerate(close):
            y_offset = index * 100
            
            draw.rectangle([0, y_offset, 99, y_offset + 99], fill=rgb1)
            draw.rectangle([100, y_offset, 199, y_offset + 99], fill=rgb2)
           
            draw.text((205, y_offset + 40), f"{name1} / {name2}", fill="black", font=font)

            

        
        #img.show("threshold_1.png")

def clean_up() -> None:
    to_remove = ["colours.csv","defs.csv"]
    for file_path in to_remove:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File {file_path} has been deleted.")
        else:
            print(f"The file {file_path} does not exist.")




if __name__ == "__main__":
    compress_colours()
    sort_colours()
    if not compile_sf():
        sys.exit()
    remove_unused()
    remove_blank_ends()
    if not compile_sf():
        sys.exit()
    check()
    #close_colours(display=True)
    clean_up()
    print("Completed")