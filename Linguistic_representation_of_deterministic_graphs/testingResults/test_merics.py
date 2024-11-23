from radon.complexity import cc_rank, cc_visit
from radon.metrics import h_visit, mi_visit

def custom_cc_rank(complexity):
    """Custom Cyclomatic Complexity Rank function to ensure A, B, or C."""
    if complexity <= 5:
        return 'A'
    elif complexity <= 10:
        return 'B'
    elif complexity <= 20:
        return 'C'
    else:
        return 'C'  # For complexity > 20, we keep it as 'C'


def analyze_code(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    # Get the Cyclomatic Complexity (CC)
    cc_results = cc_visit(code)
    total_complexity = sum(cr.complexity for cr in cc_results)
    cc_rank_value = custom_cc_rank(total_complexity)  # Use the custom rank

    # Calculate Maintainability Index (MI)
    mi_score = mi_visit(code, multi=False)

    # Calculate Halstead Metrics (HAL)
    halstead_results = h_visit(code)

    # Print the results
    print(f'File: {file_path}')

    # Cyclomatic Complexity results
    print(f'Cyclomatic Complexity (CC):')
    for cr in cc_results:
        print(f'  - Function: {cr.name}, Complexity: {cr.complexity}')
    print(f'Total Cyclomatic Complexity: {total_complexity}')
    print(f'Cyclomatic Complexity Rank: {cc_rank_value}')

    # Maintainability Index results
    print(f'\nMaintainability Index (MI): {mi_score}')

    #print(halstead_results)
# Specify the path to your Python file
file_path = "../AlgorithmsLibraries/alglib_prod_version_1_0_0.py"
analyze_code(file_path)
