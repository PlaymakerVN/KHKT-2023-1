import subprocess
import os 
def open_docx_file(file_path):
    if os.name == 'nt': # Windows
        os.startfile(file_path)
    else: # MacOS and Linux
        subprocess.run(['open', file_path] if os.name == 'posix' else ['start', file_path])

# Example usage
open_docx_file('text.docx')