import csv

def parse_co_file(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    cos = []
    current_text = ""
    
    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
        
        # If we find a new CO, process the previous one if exists
        if line.startswith('CO') and current_text:
            # Process previous CO
            co_num = current_text.split(':')[0]
            description = current_text.split(':')[1].rsplit('(K', 1)[0].strip()
            k_level = current_text.split('(K')[1].split(')')[0]
            
            cos.append({
                'CO_Number': co_num,
                'Description': description,
                'Knowledge_Level': f'K{k_level}'
            })
            current_text = line
        elif line.startswith('CO'):
            current_text = line
        else:
            current_text += ' ' + line
    
    # Process the last CO
    if current_text:
        co_num = current_text.split(':')[0]
        description = current_text.split(':')[1].rsplit('(K', 1)[0].strip()
        k_level = current_text.split('(K')[1].split(')')[0]
        
        cos.append({
            'CO_Number': co_num,
            'Description': description,
            'Knowledge_Level': f'K{k_level}'
        })
    
    # Write to CSV
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['CO_Number', 'Description', 'Knowledge_Level'])
        writer.writeheader()
        writer.writerows(cos)

if __name__ == "__main__":
    input_file = "co.txt"
    output_file = "course_outcomes.csv"
    parse_co_file(input_file, output_file)
    print(f"CSV file has been created successfully as {output_file}")
