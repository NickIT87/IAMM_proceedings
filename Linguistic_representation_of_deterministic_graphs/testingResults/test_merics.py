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

def halstead_report_to_dict(report):
    """Converts a HalsteadReport object into a dictionary."""
    return {
        "h1": report.h1,
        "h2": report.h2,
        "N1": report.N1,
        "N2": report.N2,
        "vocabulary": report.vocabulary,
        "length": report.length,
        "calculated_length": report.calculated_length,
        "volume": report.volume,
        "difficulty": report.difficulty,
        "effort": report.effort,
        "time": report.time,
        "bugs": report.bugs,
    }


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
        print(f'  - Function: {cr.name}, Complexity: {cr.complexity} {custom_cc_rank(cr.complexity)}')
    print(f'Total Cyclomatic Complexity: {total_complexity}')
    print(f'Cyclomatic Complexity Rank: {cc_rank_value}')

    # Maintainability Index results
    print(f'Maintainability Index (MI): {mi_score}\n')

    a = list(halstead_results)
    print("Total:\n", halstead_report_to_dict(a[0]))
    print("\nHalsted metric by functions:")
    for i in a[1]:
        print("\n", i[0])
        print(halstead_report_to_dict(i[1]))


# Specify the path to your Python file
file_path = "../AlgorithmsLibraries/alglib_prod_version_1_0_0.py"
analyze_code(file_path)

# file_path = "../AlgorithmsLibraries/alglib_version_01_legacy.py"
# analyze_code(file_path)