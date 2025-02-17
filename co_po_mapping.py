import re
import numpy as np
import pandas as pd

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
    # Extract K-level from text (K1-K6)
    match = re.search(r'K(\d)', text)
    return int(match.group(1)) if match else 0

def read_cos(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip() and 'CO' in line]

def clean_text(text):
    # Remove the CO/PO/PSO number and knowledge level
    text = re.sub(r'(CO|PO|PSO)\d+:', '', text)
    text = re.sub(r'\[K\d\]', '', text)
    # Convert to lowercase
    text = text.lower()
    return text.strip()

def get_keywords(text):
    # Define domain-specific keywords for different categories
    algorithm_keywords = {'algorithm', 'divide and conquer', 'greedy', 'backtracking', 'dynamic programming', 
                        'optimization', 'complexity', 'logarithmic', 'programming'}
    problem_solving_keywords = {'problem', 'solution', 'analyze', 'solve', 'design', 'implement', 'develop'}
    engineering_keywords = {'engineering', 'mathematical', 'mathematics', 'science', 'technical'}
    tools_keywords = {'tool', 'technique', 'method', 'implementation', 'technology', 'software'}
    
    text = clean_text(text)
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
    
    # Calculate matching score based on keyword categories
    matching_categories = sum(1 for k in co_keywords if co_keywords[k] and po_keywords[k])
    total_co_categories = sum(1 for k in co_keywords if co_keywords[k])
    
    if total_co_categories == 0:
        return False
        
    # If more than 50% of CO categories match with PO categories, consider it a match
    return (matching_categories / total_co_categories) >= 0.5

def create_mapping_matrix(cos, reference_statements):
    # Initialize matrix with zeros
    matrix = np.zeros((len(cos), len(reference_statements)))
    
    for i, co in enumerate(cos):
        co_level = extract_k_level(co)
        for j, ref in enumerate(reference_statements):
            ref_level = extract_k_level(ref)
            
            # Check semantic match between CO and reference statement
            if check_semantic_match(co, ref):
                if co_level > ref_level:
                    matrix[i][j] = 3
                elif co_level == ref_level:
                    matrix[i][j] = 2
                else:
                    matrix[i][j] = 1
            else:
                matrix[i][j] = np.nan  # Empty cell instead of 0
    
    return matrix

def calculate_column_averages(matrix):
    # Get number of columns
    num_cols = matrix.shape[1]
    averages = np.zeros(num_cols)
    
    # Calculate average for each column
    for col in range(num_cols):
        # Get all non-nan values in the column (mapped values only)
        mapped_values = matrix[:, col][~np.isnan(matrix[:, col])]
        if len(mapped_values) > 0:  # Only calculate average if there are mapped values
            averages[col] = np.mean(mapped_values)
        else:
            averages[col] = np.nan
            
    return averages

def main():
    # Read CO statements
    cos = read_cos('co.txt')
    
    # Combine POs and PSOs into a single list
    all_outcomes = POS + PSOS
    
    # Create single mapping matrix for both POs and PSOs
    mapping_matrix = create_mapping_matrix(cos, all_outcomes)
    
    # Calculate column averages
    averages = calculate_column_averages(mapping_matrix)
    
    # Create column headers
    headers = ([f"PO{i+1}" for i in range(len(POS))] + 
              [f"PSO{i+1}" for i in range(len(PSOS))])
    
    # Create row indices
    row_indices = [f"CO{i+1}" for i in range(len(cos))]
    
    # Create DataFrame with the mapping matrix
    df = pd.DataFrame(mapping_matrix, columns=headers, index=row_indices)
    
    # Add averages row
    df.loc['Average'] = averages
    
    # Save to CSV
    csv_filename = 'co_po_mapping.csv'
    df.to_csv(csv_filename)
    print(f"\nMatrix saved to {csv_filename}")
    
    # Print results to console
    print("\nCO-PO-PSO Mapping Matrix:")
    print("-" * 100)
    
    # Print header with PO and PSO numbers
    print("     ", end="")
    for i in range(len(POS)):
        print(f"PO{i+1:2d}", end=" ")
    for i in range(len(PSOS)):
        print(f"PSO{i+1:2d}", end=" ")
    print("\n" + "-" * 100)
    
    # Print matrix rows
    for i, row in enumerate(mapping_matrix):
        print(f"CO{i+1:2d}", end=" ")
        # Print values, replacing NaN with spaces
        print(" ".join(f"{int(val):2d}" if not np.isnan(val) else "  " for val in row))
    
    # Print separator line
    print("-" * 100)
    
    # Print average row
    print("AVG ", end="")
    # Print averages with 2 decimal places, or spaces for NaN
    print(" ".join(f"{val:2.1f}" if not np.isnan(val) else "  " for val in averages))

if __name__ == "__main__":
    main()
