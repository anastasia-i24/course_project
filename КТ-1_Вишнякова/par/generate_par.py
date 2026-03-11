import zipfile
import os
import shutil
import variables_definition
import process_definition

def generate_par(lanes):
    if os.path.exists('temporary'):
        shutil.rmtree('temporary')
    shutil.copytree('templates', 'temporary')
    try:
        variables_definition('temporary/variables.xml', lanes)
        process_definition('temporary/processdefinition.xml', lanes)
        with zipfile.ZipFile('result.par', 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk('temporary'):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, 'temporary')
                    zf.write(file_path, arc_name)
        return True, f"Создан result.par"
    finally:
        if os.path.exists('temporary'):
            shutil.rmtree('temporary')