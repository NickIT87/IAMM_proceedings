from radon.complexity import cc_rank, cc_visit
from radon.metrics import h_visit


def analyze_code(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    # Get the Cyclomatic Complexity (CC) and maintainability index
    cc_results = cc_visit(code)
    for cr in cc_results:
        print(cr)
    complexity = sum(cr.complexity for cr in cc_results)
    maintainability_index = cc_rank(complexity)

    print(f'File: {file_path}')
    print(f'Total Complexity: {complexity}')
    print(f'Maintainability Index: {maintainability_index}')

    # Calculate Halstead complexity
    halstead_results = h_visit(code)
    #print(halstead_results)

# Specify the path to your Python file
file_path = "../AlgorithmsLibraries/alglib_version_02_current.py"
analyze_code(file_path)
