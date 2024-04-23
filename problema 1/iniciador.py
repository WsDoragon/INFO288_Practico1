import os

# Ruta del entorno Conda
conda_env_path = "C:/Users/berna/Anaconda3/Scripts/activate.bat"

# Nombre del entorno Conda
conda_env_name = "INFO288"

# Comando para activar el entorno Conda
activate_cmd = f"call {conda_env_path} {conda_env_name}"

for i in range(1, 3):
    # Comando para ejecutar el archivo slave.py
    execute_cmd = f"python slave{i}.py"

    # Obtener la ruta absoluta del archivo slave.py
    file_path = os.path.abspath(f"slave{i}.py")

    # Abrir una terminal de comandos, activar el entorno Conda y ejecutar los comandos
    os.system(f"start cmd /k \"{activate_cmd} && cd /D {os.path.dirname(file_path)} && {execute_cmd}\"")
