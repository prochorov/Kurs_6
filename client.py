import socket
import os

def main():
    # Создаем TCP сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Подключаемся к серверу
    client_socket.connect(('localhost', 8080))

    try:
        # Отправляем имя пользователя на сервер
        username = input("Введите ваше имя: ")
        client_socket.send(username.encode("utf-8"))

        while True:
            # Выводим меню команд для пользователя
            print("\nМеню команд:")
            print("1. Скачать файл")
            print("2. Вывести список файлов на сервере")
            choice = input("Выберите команду (1/2): ")

            if choice == "1":
                client_socket.send("download".encode("utf-8"))
                # Запрашиваем имя файла у пользователя
                filename = input("Введите имя файла для скачивания: ")
                # Отправляем имя файла на сервер
                client_socket.send(filename.encode("utf-8"))
                # Получаем данные файла от сервера и сохраняем на локальном компьютере
                file_data = client_socket.recv(1024)
                user_folder = os.path.join(CLIENTS_FOLDER, username)
                if not os.path.exists(user_folder):
                    os.makedirs(user_folder)
                file_path = os.path.join(user_folder, filename)
                with open(file_path, "wb") as f:
                    while file_data:
                        f.write(file_data)
                        file_data = client_socket.recv(1024)
                print(f"Файл {filename} успешно скачан")
            elif choice == "2":
                client_socket.send("list".encode("utf-8"))
                # Получаем список файлов с сервера и выводим их
                file_list = client_socket.recv(1024).decode("utf-8")
                print("Список файлов на сервере:")
                print(file_list)
            else:
                print("Неверная команда, попробуйте еще раз.")

    except KeyboardInterrupt:
        print("Выход...")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()

