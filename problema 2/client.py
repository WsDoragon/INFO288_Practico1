import socket
import sys
import signal

def main():
    # Verificar que se proporcionen la dirección IP y el puerto del servidor como argumentos
    if len(sys.argv) != 3:
        print("Uso: python3 cliente.py <ip_servidor> <puerto_servidor>")
        sys.exit(1)

    ip_servidor = sys.argv[1]
    puerto_servidor = int(sys.argv[2])

    # Crear un objeto socket TCP/IP
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conectar el socket al servidor
        cliente_socket.connect((ip_servidor, puerto_servidor))
        print(f"Conexión establecida con el servidor {ip_servidor}:{puerto_servidor}")

        while True:
            # Esperar por la entrada del usuario para enviar un mensaje al servidor
            mensaje = input("Ingrese un mensaje para enviar al servidor (o 'exit' para salir): ")

            if mensaje.lower() == "exit":
                break

            # Enviar el mensaje al servidor
            cliente_socket.sendall(mensaje.encode())

            # Esperar por la respuesta del servidor
            respuesta = cliente_socket.recv(1024)
            print("Respuesta del servidor:", respuesta.decode())

    except KeyboardInterrupt:
        print("Se recibió una señal de interrupción. Cerrando el cliente.")
        cliente_socket.close()
        sys.exit()
    except ConnectionRefusedError:
        print("No se pudo establecer conexión con el servidor.")

    finally:
        # Cerrar el socket
        cliente_socket.close()

if __name__ == "__main__":
    main()

