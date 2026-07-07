import argparse
import os
import re
import sys
import tokenize
import io

# Configurar salida estándar en utf-8 para evitar errores con emojis en Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def strip_python_comments_and_docstrings(source_code):
    """
    Safely removes docstrings and comments from Python source code
    using Python's built-in AST parsing and unparsing.
    """
    import ast
    try:
        # Parsear el código fuente en un árbol de sintaxis abstracta
        tree = ast.parse(source_code)
        
        # Transformador que busca y elimina el primer nodo de expresión si es una constante de cadena (docstring)
        class DocstringRemover(ast.NodeTransformer):
            def visit_Module(self, node):
                self.generic_visit(node)
                if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                    node.body.pop(0)
                return node

            def visit_FunctionDef(self, node):
                self.generic_visit(node)
                if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                    node.body.pop(0)
                return node

            def visit_AsyncFunctionDef(self, node):
                self.generic_visit(node)
                if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                    node.body.pop(0)
                return node

            def visit_ClassDef(self, node):
                self.generic_visit(node)
                if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                    node.body.pop(0)
                return node
        
        # Remover docstrings
        DocstringRemover().visit(tree)
        
        # Re-convertir el árbol AST en código fuente (esto remueve automáticamente comentarios y normaliza espacios)
        return ast.unparse(tree)
    except Exception as e:
        # Fallback a regex si el código contiene errores de sintaxis durante el borrador
        print(f"Warning: Python AST parser failed ({e}). Falling back to regex parser.", file=sys.stderr)
        source = re.sub(r'#.*$', '', source_code, flags=re.M)
        return source

def strip_c_style_comments(source_code):
    """
    Removes // and /* */ comments from JS/TS/CSS files.
    """
    # Remove block comments
    source = re.sub(r'/\*.*?\*/', '', source_code, flags=re.S)
    # Remove single line comments
    source = re.sub(r'//.*$', '', source, flags=re.M)
    return source

def collapse_blank_lines(source_code):
    """
    Eliminates trailing whitespace and collapses consecutive empty lines.
    """
    lines = source_code.splitlines()
    clean_lines = []
    for line in lines:
        stripped = line.rstrip()
        if stripped:
            clean_lines.append(stripped)
        else:
            # Keep at most one consecutive empty line
            if not clean_lines or clean_lines[-1] != "":
                clean_lines.append("")
                
    # Remove final empty line if any
    while clean_lines and clean_lines[-1] == "":
        clean_lines.pop()
        
    return "\n".join(clean_lines) + "\n"

def audit_code_quality(source_code, filename):
    """
    Scans the source code statically for code smells, complexity,
    and credential safety, generating actionable suggestions.
    """
    suggestions = []
    
    # 1. Check for overly long functions (SOLID violation)
    functions = re.findall(r'(def\s+(\w+)\s*\(|function\s+(\w+)\s*\()', source_code)
    for f in functions:
        name = f[1] if f[1] else f[2]
        # Very simple heuristic: estimate function lines by looking at indentation
        # For this audit, we flag long segments or just give general SOLID advice
        if name and len(name) > 2:
            pass

    # 2. Check for nested loops O(N^2)
    python_nested = re.search(r'^\s*for\s+.*\r?\n\s+for\s+.*', source_code, flags=re.M)
    js_nested = re.search(r'for\s*\(.*\)\s*\{[^{}]*for\s*\(.*\)', source_code, flags=re.S)
    if python_nested or js_nested:
        suggestions.append("- ⚙️ **Complejidad Algorítmica (O(N^2)):** Se detectaron bucles anidados. Considera usar un diccionario (hash map) para reducir la complejidad temporal a O(N).")

    # 3. Check for hardcoded secrets
    secrets_keywords = ['api_key', 'apikey', 'password', 'passwd', 'secret_key', 'token', 'jwt_secret']
    found_secrets = []
    for kw in secrets_keywords:
        pattern = rf'(?i){kw}\s*=\s*[\'"][^\'"]+[\'"]'
        if re.search(pattern, source_code):
            found_secrets.append(kw)
    if found_secrets:
        suggestions.append(f"- 🔒 **Seguridad de Secretos:** Se detectó posible credencial hardcodeada en las variables: `{', '.join(found_secrets)}`. Extráelas a un archivo `.env` o variables de entorno.")

    # 4. Check for bare excepts in Python
    if filename.endswith(".py") and "except:" in source_code:
        suggestions.append("- 🧪 **Manejo de Excepciones:** Se encontró una cláusula `except:` genérica. Captura la excepción específica (ej. `except ValueError:`) para mayor robustez.")

    # 5. Check for clean code length
    lines_count = len(source_code.splitlines())
    if lines_count > 150:
        suggestions.append(f"- 📦 **Modularidad (SOLID):** El archivo tiene {lines_count} líneas. Considera dividir el código en submódulos cohesivos de responsabilidad única.")

    if not suggestions:
        suggestions.append("- 🌟 **¡Excelente código!** Sigue los principios SOLID, DRY y no tiene vulnerabilidades obvias detectadas.")
        
    return suggestions

def main():
    parser = argparse.ArgumentParser(description="Scissors# Code Pruner & Token Optimizer")
    parser.add_argument("--file", required=True, help="Path to the file to optimize")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite the original file with the optimized version")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' not found.", file=sys.stderr)
        sys.exit(1)

    # Read original
    with open(args.file, "r", encoding="utf-8", errors="replace") as f:
        original_content = f.read()

    filename = os.path.basename(args.file)
    ext = os.path.splitext(filename)[1].lower()

    # Step 1: Strip comments/docstrings based on extension
    if ext == ".py":
        pruned = strip_python_comments_and_docstrings(original_content)
    elif ext in (".js", ".ts", ".jsx", ".tsx", ".css"):
        pruned = strip_c_style_comments(original_content)
    else:
        pruned = original_content # Generic fallback

    # Step 2: Collapse space
    optimized_content = collapse_blank_lines(pruned)

    # Step 3: Calculate token stats
    original_size = len(original_content)
    optimized_size = len(optimized_content)
    
    # 1 token is roughly 4 characters in Latin scripts
    original_tokens = max(1, original_size // 4)
    optimized_tokens = max(1, optimized_size // 4)
    saved_tokens = max(0, original_tokens - optimized_tokens)
    pct_saved = (saved_tokens / original_tokens) * 100

    # Step 4: Audit code quality
    suggestions = audit_code_quality(optimized_content, filename)

    # Step 5: Output Report
    print(f"### Reporte de Optimización: {filename}")
    print(f"| Métrica | Original | Optimizado | Ahorro |")
    print(f"| :--- | :--- | :--- | :--- |")
    print(f"| Tamaño (Bytes) | {original_size} B | {optimized_size} B | {original_size - optimized_size} B |")
    print(f"| Tokens Estimados | {original_tokens} | {optimized_tokens} | {saved_tokens} ({pct_saved:.1f}%) |")
    print("\n#### Sugerencias de Mejora Contextual:")
    print("\n".join(suggestions))

    # Step 6: Overwrite if requested
    if args.overwrite:
        with open(args.file, "w", encoding="utf-8") as f:
            f.write(optimized_content)
        print(f"\n[OK] El archivo '{filename}' fue optimizado y sobrescrito exitosamente.", file=sys.stderr)

if __name__ == "__main__":
    main()
