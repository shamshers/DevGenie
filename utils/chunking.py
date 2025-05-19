import ast
from typing import List

def chunk_python_code_by_function(code_str: str, min_length=40) -> List[str]:
    """
    Split Python code into chunks per function or class, fallback to generic chunking if needed.
    """
    chunks = []
    try:
        tree = ast.parse(code_str)
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                start = node.lineno - 1
                end = node.end_lineno if hasattr(node, "end_lineno") else None
                lines = code_str.splitlines()[start:end]
                chunk = "\n".join(lines)
                if len(chunk) > min_length:
                    chunks.append(chunk)
        if not chunks:
            # fallback to generic chunking if no functions/classes found
            return chunk_text(code_str)
        return chunks
    except Exception as e:
        # fallback in case of error
        return chunk_text(code_str)

def chunk_text(text: str, max_length=400, overlap=50) -> List[str]:
    """
    Generic text chunking with overlap for long docs.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_length - overlap):
        chunk = " ".join(words[i:i + max_length])
        if len(chunk) > 20:
            chunks.append(chunk)
    return chunks
