import sys
import tkinter as tk
from tkinter import messagebox, filedialog
import numpy as np
import pandas as pd
import os
from datetime import datetime

# Copy all the POS, PSOS, and helper functions from co_po_mapping.py
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

def calculate_column_averages(matrix):
    num_cols = matrix.shape[1]
    averages = np.zeros(num_cols)
    
    for col in range(num_cols):
        mapped_values = matrix[:, col][~np.isnan(matrix[:, col])]
        if len(mapped_values) > 0:
            averages[col] = np.mean(mapped_values)
        else:
            averages[col] = np.nan
            
    return averages

class COPOMappingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CO-PO Mapping Generator")
        self.root.geometry("600x400")
        
        # Create main frame
        main_frame = tk.Frame(root, padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')
        
        # Title
        title = tk.Label(main_frame, text="CO-PO Mapping Matrix Generator", font=("Arial", 16, "bold"))
        title.pack(pady=(0, 20))
        
        # Instructions
        instructions = """Instructions:
1. Create a text file containing your Course Outcomes (COs)
2. Each CO should be on a new line
3. Include the knowledge level in square brackets [K1] to [K6]
4. Example:
   CO1: Apply Divide and Conquer algorithm technique to solve complex problems in logarithmic time. [K3]"""
        
        instr_label = tk.Label(main_frame, text=instructions, justify='left')
        instr_label.pack(pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        generate_btn = tk.Button(button_frame, text="Generate Matrix", command=self.generate_matrix)
        generate_btn.pack(side='left', padx=10)
        
        quit_btn = tk.Button(button_frame, text="Quit", command=root.quit)
        quit_btn.pack(side='left', padx=10)

    def generate_matrix(self):
        try:
            # Ask user to select CO file
            file_path = filedialog.askopenfilename(
                title="Select CO File",
                filetypes=[("Text Files", "*.txt")]
            )
            
            if not file_path:
                return
            
            # Read COs from file
            with open(file_path, 'r') as f:
                cos = [line.strip() for line in f if line.strip()]
            
            # Create mapping matrix
            all_outcomes = POS + PSOS
            mapping_matrix = create_mapping_matrix(cos, all_outcomes)
            averages = calculate_column_averages(mapping_matrix)
            
            # Create DataFrame
            headers = ([f"PO{i+1}" for i in range(len(POS))] + 
                      [f"PSO{i+1}" for i in range(len(PSOS))])
            row_indices = [f"CO{i+1}" for i in range(len(cos))]
            df = pd.DataFrame(mapping_matrix, columns=headers, index=row_indices)
            df.loc['Average'] = averages
            
            # Save to CSV in same directory as input file
            output_dir = os.path.dirname(file_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            csv_filename = os.path.join(output_dir, f'co_po_mapping_{timestamp}.csv')
            df.to_csv(csv_filename)
            
            messagebox.showinfo("Success", f"Matrix has been generated and saved to:\n{csv_filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

def main():
    root = tk.Tk()
    app = COPOMappingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
