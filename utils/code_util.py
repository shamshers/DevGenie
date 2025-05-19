import ast
import black

def is_valid_python(code_str):
    """Check if code compiles."""
    try:
        ast.parse(code_str)
        return True
    except SyntaxError:
        return False

def format_code_black(code_str):
    """Format code using Black."""
    try:
        return black.format_str(code_str, mode=black.FileMode())
    except Exception:
        return code_str

def extract_functions(code_str):
    """Extract all function names from code."""
    try:
        tree = ast.parse(code_str)
        return [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    except Exception:
        return []

def get_docstring(code_str):
    """Extract module-level docstring, if any."""
    try:
        tree = ast.parse(code_str)
        return ast.get_docstring(tree)
    except Exception:
        return None
