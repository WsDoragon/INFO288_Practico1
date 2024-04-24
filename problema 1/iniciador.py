import os
import sys



args = sys.argv
if len(args) < 2:
    print("Porfavor ingrese ambiente de conda\nEjemplo: python iniciador.py INFO288")
    sys.exit(1)

print("Arguments:", args)
# Nombre del entorno Conda
conda_env_name = args[1]

# Comando para activar el entorno Conda
activate_cmd = f"call conda activate {conda_env_name}"
# Obtener todos los archivos .env en la carpeta slave_envs
env_files = [f for f in os.listdir("slave_envs")]

# Imprimir los nombres de los archivos .env encontrados
for env_file in env_files:
    print(env_file, "encontrado")
for i in env_files:
    # Comando para ejecutar el archivo slave.py
    execute_cmd = f"python slave1.py ./slave_envs/{i}"

    # Obtener la ruta absoluta del archivo slave.py
    file_path = os.path.abspath(f"slave1.py")

    # Abrir una terminal de comandos, activar el entorno Conda y ejecutar los comandos
    os.system(f"start cmd /k \"{activate_cmd} && cd /D {os.path.dirname(file_path)} && {execute_cmd}\"")
