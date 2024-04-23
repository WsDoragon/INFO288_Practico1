import socket
import signal
import sys

def manejar_conexion(conexion, direccion_cliente):
    print(f"Conexión entrante desde {direccion_cliente}")

    try:
        while True:
            # Recibir datos del cliente
            datos = conexion.recv(1024)
            if not datos:
                break

            mensaje_cliente = datos.decode()
            print(f"Mensaje recibido del cliente {direccion_cliente}: {mensaje_cliente}")

            # Enviar respuesta al cliente
            respuesta = f"Me llegó tu mensaje: {mensaje_cliente}"
            conexion.sendall(respuesta.encode())

    except KeyboardInterrupt:
        print("Se recibió una señal de interrupción. Cerrando la conexión con el cliente.")
    finally:
        # Cerrar la conexión
        conexion.close()

def iniciar_servidor(ip, puerto):
    # Crear un objeto socket TCP/IP
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Permitir reutilizar el puerto después de cerrar el socket
        servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Enlazar el socket a la dirección y puerto especificados
        servidor_socket.bind((ip, puerto))

        # Escuchar por conexiones entrantes
        servidor_socket.listen(5)

        print(f"Servidor escuchando en {ip}:{puerto}")

        while True:
            # Esperar por una conexión
            conexion, direccion_cliente = servidor_socket.accept()
            manejar_conexion(conexion, direccion_cliente)

    except KeyboardInterrupt:
        print("Se recibió una señal de interrupción. Cerrando el servidor.")
        servidor_socket.close()
        sys.exit()
    except ConnectionRefusedError:
        print("No se pudo establecer conexión con el cliente.")

    finally:
        # Cerrar el socket del servidor
        servidor_socket.close()

if __name__ == "__main__":
    # Dirección IP y puerto en el que escuchará el servidor
    ip_servidor = "127.0.0.1"  # Puedes cambiar esta dirección por la que necesites
    puerto_servidor = 12345     # Puedes cambiar este puerto por el que desees utilizar

    # Iniciar el servidor
    iniciar_servidor(ip_servidor, puerto_servidor)


