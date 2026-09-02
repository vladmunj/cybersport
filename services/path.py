from pathlib import Path

def root_path():
    current_path = Path(__file__).resolve()
    for parent in current_path.parents:
        if(parent / '.env').exists() or (parent / '.git').exists() : return parent
    return current_path.parent