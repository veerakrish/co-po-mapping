from flask import Flask, render_template, request, send_file
import numpy as np
import pandas as pd
import os
from datetime import datetime
from co_parser import parse_co_file

app = Flask(__name__)

# Fixed POs with their knowledge levels
POS = [
    "1. Engineering knowledge: Apply the knowledge of Mathematics, Science, Engineering Fundamentals and Concepts of Computer Science Engineering to the solution of complex Engineering problems.[K3]",
    "2. Problem Analysis: Identify, formulate, review research literature, and analyze complex engineering problems reaching substantiated conclusions using first principles of Mathematics, Natural Sciences and Computer Science.[K4]",
    "3. Design/Development of Solutions: Design solutions for complex Engineering problems and design system components or processes that meet the specified needs with appropriate consideration for the public health and safety, and the cultural, societal, and environmental considerations.[K5]",
    "4. Conduct Investigations of Complex Problems: Use research-based knowledge and research methods including design of experiments, analysis and interpretation of data, and synthesis of the information to provide valid conclusions.[K5]",
    "5. Modern Tool Usage: Create, select, and apply appropriate techniques, resources, and modern Engineering and IT tools including prediction and modeling to complex Engineering activities with an understanding of the limitations.[K3]",
    "6. The Engineer and Society: Apply reasoning informed by the contextual knowledge to assess societal, health, safety, legal and cultural issues and the consequent responsibilities relevant to the professional Engineering practice.[K3]",
    "7. Environment and Sustainability: Understand the impact of the professional Engineering solutions in societal and environmental contexts, and demonstrate the knowledge of, and need for sustainable development.[K3]",
    "8. Ethics: Apply ethical principles and commit to professional ethics and responsibilities and norms of the Engineering practice.[K3]",
    "9. Individual and Team Work: Function effectively as an individual, and as a member or leader in diverse teams, and in multidisciplinary settings.[K3]",
    "10. Communication: Communicate effectively on complex Engineering activities with the Engineering community and with society at large.[K3]",
    "11. Project Management and Finance: Demonstrate knowledge and understanding of the Engineering and management principles and apply these to one's own work, as a member and leader in a team.[K3]",
    "12. Life-long Learning: Recognize the need for, and have the preparation and ability to engage in independent and life-long learning in the broadest context of technological change.[K3]"
]

# Fixed PSOs with their knowledge levels
PSOS = [
    "PSO1: Use Mathematical Abstractions and Algorithmic Design along with Open Source Programming tools to solve complexities involved in Programming.[K3]",
    "PSO2: Use Professional Engineering practices and strategies for development and maintenance of software.[K3]"
]

def extract_k_level(text):
    import re
    match = re.search(r'K(\d)', text)
    return int(match.group(1)) if match else 0

def get_keywords(text):
    # Define domain-specific keywords for different categories
    algorithm_keywords = {'algorithm', 'divide and conquer', 'greedy', 'backtracking', 'dynamic programming', 
                        'optimization', 'complexity', 'logarithmic', 'programming'}
    problem_solving_keywords = {'problem', 'solution', 'analyze', 'solve', 'design', 'implement', 'develop'}
    engineering_keywords = {'engineering', 'mathematical', 'mathematics', 'science', 'technical'}
    tools_keywords = {'tool', 'technique', 'method', 'implementation', 'technology', 'software'}
    
    text = text.lower()
    words = set(text.split())
    
    return {
        'algorithm': bool(words & algorithm_keywords),
        'problem_solving': bool(words & problem_solving_keywords),
        'engineering': bool(words & engineering_keywords),
        'tools': bool(words & tools_keywords)
    }

def check_semantic_match(co_text, po_text):
    co_keywords = get_keywords(co_text)
    po_keywords = get_keywords(po_text)
    
    matching_categories = sum(1 for k in co_keywords if co_keywords[k] and po_keywords[k])
    total_co_categories = sum(1 for k in co_keywords if co_keywords[k])
    
    if total_co_categories == 0:
        return False
    
    return (matching_categories / total_co_categories) >= 0.5

def create_mapping_matrix(cos, reference_statements):
    matrix = np.zeros((len(cos), len(reference_statements)))
    
    for i, co in enumerate(cos):
        co_level = extract_k_level(co)
        for j, ref in enumerate(reference_statements):
            ref_level = extract_k_level(ref)
            
            if check_semantic_match(co, ref):
                if co_level > ref_level:
                    matrix[i][j] = 3
                elif co_level == ref_level:
                    matrix[i][j] = 2
                else:
                    matrix[i][j] = 1
            else:
                matrix[i][j] = np.nan
    
    return matrix

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file uploaded'
        
        file = request.files['file']
        if file.filename == '':
            return 'No file selected'
        
        # Save the uploaded file
        temp_input = 'temp_co_input.txt'
        temp_parsed = 'temp_co_parsed.csv'
        file.save(temp_input)
        
        # Parse the CO file first
        try:
            parse_co_file(temp_input, temp_parsed)
        except Exception as e:
            if os.path.exists(temp_input):
                os.remove(temp_input)
            if os.path.exists(temp_parsed):
                os.remove(temp_parsed)
            return f'Error parsing CO file: {str(e)}'
        
        # Read the parsed COs
        try:
            cos_df = pd.read_csv(temp_parsed)
            cos = [f"{row['CO_Number']}: {row['Description']} [{row['Knowledge_Level']}]" 
                  for _, row in cos_df.iterrows()]
        except Exception as e:
            if os.path.exists(temp_input):
                os.remove(temp_input)
            if os.path.exists(temp_parsed):
                os.remove(temp_parsed)
            return f'Error reading parsed COs: {str(e)}'
        
        # Generate the mapping matrix
        matrix = create_mapping_matrix(cos, POS + PSOS)
        
        # Calculate column averages (only for non-zero values)
        averages = []
        for col in range(matrix.shape[1]):
            col_values = matrix[:, col]
            non_zero_values = col_values[col_values > 0]
            avg = np.mean(non_zero_values) if len(non_zero_values) > 0 else 0
            averages.append(avg)
        
        # Add column averages
        matrix_with_avg = np.vstack([matrix, averages])
        
        # Create DataFrame
        columns = [f'PO{i+1}' for i in range(len(POS))] + [f'PSO{i+1}' for i in range(len(PSOS))]
        index = [f'CO{i+1}' for i in range(len(cos))] + ['Average']
        df = pd.DataFrame(matrix_with_avg, columns=columns, index=index)
        
        # Replace zeros with empty strings and format averages
        df = df.replace({0: '', np.nan: ''})  
        df.loc['Average'] = df.loc['Average'].apply(lambda x: f'{float(x):.2f}' if x != '' else '')
        
        # Save to CSV with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'co_po_mapping_{timestamp}.csv'
        df.to_csv(output_file)
        
        # Clean up temporary files
        if os.path.exists(temp_input):
            os.remove(temp_input)
        if os.path.exists(temp_parsed):
            os.remove(temp_parsed)
        
        # Display results with custom formatting
        table_html = df.to_html(classes='table table-bordered', na_rep='')
        return render_template('result.html', 
                             table=table_html,
                             filename=output_file)
    
    return render_template('index.html')

@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    import webbrowser
    import os
    
    # Create output directory if it doesn't exist
    if not os.path.exists('output'):
        os.makedirs('output')
    
    # Open browser after a short delay
    def open_browser():
        webbrowser.open('http://127.0.0.1:5000/')
    
    from threading import Timer
    Timer(1.5, open_browser).start()
    
    # Run the app
    app.run(host='127.0.0.1', port=5000)
