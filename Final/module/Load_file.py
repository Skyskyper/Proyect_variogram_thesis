from module.common_imports import *

def load_data(input_file=None, default_file='test_data.csv'):
    
    # Determine the file path
    if input_file is None:
        input_file = os.path.join(os.path.dirname(__file__), default_file)
    
    # Get absolute path and validate existence
    input_file = os.path.abspath(input_file)
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"File not found: {input_file}")
    
    return input_file
