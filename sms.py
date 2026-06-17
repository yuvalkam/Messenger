import socket
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog


# =========================
# Server
# =========================

class MessengerServer:
    def __init__(self, host="127.0.0.1", port=12343):
        self.host = host
        self.port = port

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        self.clients = {}  # username -> socket
        self.lock = threading.Lock()

        print(f"Server listening on {self.host}:{self.port}")

    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            thread = threading.Thread(
                target=self.handle_client,
                args=(client_socket, client_address),
                daemon=True
            )
            thread.start()

    def handle_client(self, client_socket, client_address):
        username = None

        try:
            username = client_socket.recv(1024).decode("utf-8").strip()

            if not username:
                client_socket.close()
                return

            with self.lock:
                if username in self.clients:
                    client_socket.send("error:Username already taken".encode("utf-8"))
                    client_socket.close()
                    return

                self.clients[username] = client_socket

            print(f"{username} connected from {client_address}")
            self.broadcast_system_message(f"{username} joined the chat")
            self.send_client_list()

            while True:
                data = client_socket.recv(1024)

                if not data:
                    break

                message = data.decode("utf-8")

                if message == "exit":
                    break

                elif message.startswith("private:"):
                    parts = message.split(":", 2)

                    if len(parts) == 3:
                        _, target_username, private_message = parts
                        self.send_private_message(username, target_username, private_message)

                else:
                    self.broadcast(username, message)

        except Exception as e:
            print(f"Error with client {client_address}: {e}")

        finally:
            if username:
                with self.lock:
                    if username in self.clients:
                        del self.clients[username]

                print(f"{username} disconnected")
                self.broadcast_system_message(f"{username} left the chat")
                self.send_client_list()

            client_socket.close()

    def broadcast(self, sender_username, message):
        full_message = f"message:{sender_username}:{message}"

        with self.lock:
            clients_copy = list(self.clients.items())

        for username, client_socket in clients_copy:
            if username != sender_username:
                try:
                    client_socket.send(full_message.encode("utf-8"))
                except:
                    pass

    def send_private_message(self, sender_username, target_username, message):
        with self.lock:
            target_socket = self.clients.get(target_username)
            sender_socket = self.clients.get(sender_username)

        if target_socket:
            try:
                target_socket.send(
                    f"private:{sender_username}:{message}".encode("utf-8")
                )

                if sender_socket:
                    sender_socket.send(
                        f"private_you:{target_username}:{message}".encode("utf-8")
                    )

            except:
                pass
        else:
            if sender_socket:
                sender_socket.send(
                    f"error:User {target_username} not found".encode("utf-8")
                )

    def send_client_list(self):
        with self.lock:
            usernames = list(self.clients.keys())
            clients_copy = list(self.clients.values())

        message = "clients_list:" + ",".join(usernames)

        for client_socket in clients_copy:
            try:
                client_socket.send(message.encode("utf-8"))
            except:
                pass

    def broadcast_system_message(self, message):
        with self.lock:
            clients_copy = list(self.clients.values())

        for client_socket in clients_copy:
            try:
                client_socket.send(f"system:{message}".encode("utf-8"))
            except:
                pass


# =========================
# Client
# =========================

class MessengerClient:
    def __init__(self, root, username, server_ip="127.0.0.1", server_port=12343):
        self.root = root
        self.username = username
        self.server_ip = server_ip
        self.server_port = server_port

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))
        self.client_socket.send(self.username.encode("utf-8"))

        self.messages = []
        self.private_messages = []
        self.users = []

    def start(self):
        thread = threading.Thread(target=self.receive_messages, daemon=True)
        thread.start()

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)

                if not data:
                    break

                message = data.decode("utf-8")

                self.root.after(0, self.handle_server_message, message)

            except:
                break

        self.root.after(0, self.show_disconnected_message)

    def handle_server_message(self, message):
        if message.startswith("clients_list:"):
            users_text = message.split(":", 1)[1]
            self.users = users_text.split(",") if users_text else []
            self.update_user_list()

        elif message.startswith("message:"):
            _, sender, msg = message.split(":", 2)
            self.messages.append(f"{sender}: {msg}")
            self.display_messages()

        elif message.startswith("private:"):
            _, sender, msg = message.split(":", 2)
            self.private_messages.append(f"Private from {sender}: {msg}")
            self.display_private_messages()

        elif message.startswith("private_you:"):
            _, target, msg = message.split(":", 2)
            self.private_messages.append(f"You to {target}: {msg}")
            self.display_private_messages()

        elif message.startswith("system:"):
            system_msg = message.split(":", 1)[1]
            self.messages.append(f"[System] {system_msg}")
            self.display_messages()

        elif message.startswith("error:"):
            error_msg = message.split(":", 1)[1]
            messagebox.showerror("Error", error_msg)

    def send_message(self):
        message = self.message_entry.get().strip()

        if not message:
            messagebox.showwarning("Input Error", "Please enter a message.")
            return

        try:
            self.client_socket.send(message.encode("utf-8"))
            self.messages.append(f"You: {message}")
            self.display_messages()
            self.message_entry.delete(0, tk.END)
        except:
            messagebox.showerror("Connection Error", "Could not send message.")

    def send_private_message(self):
        selected_index = self.users_listbox.curselection()

        if not selected_index:
            messagebox.showwarning("Selection Error", "Please select a user.")
            return

        target_username = self.users_listbox.get(selected_index[0])

        if target_username == self.username:
            messagebox.showwarning("Selection Error", "You cannot send private message to yourself.")
            return

        message = self.message_entry.get().strip()

        if not message:
            messagebox.showwarning("Input Error", "Please enter a message.")
            return

        try:
            self.client_socket.send(
                f"private:{target_username}:{message}".encode("utf-8")
            )
            self.message_entry.delete(0, tk.END)
        except:
            messagebox.showerror("Connection Error", "Could not send private message.")

    def update_user_list(self):
        self.users_listbox.delete(0, tk.END)

        for user in self.users:
            self.users_listbox.insert(tk.END, user)

    def display_messages(self):
        self.messages_box.delete(1.0, tk.END)

        for msg in self.messages:
            self.messages_box.insert(tk.END, msg + "\n")

        self.messages_box.yview(tk.END)

    def display_private_messages(self):
        self.private_messages_box.delete(1.0, tk.END)

        for msg in self.private_messages:
            self.private_messages_box.insert(tk.END, msg + "\n")

        self.private_messages_box.yview(tk.END)

    def show_disconnected_message(self):
        messagebox.showwarning("Disconnected", "Disconnected from server.")

    def create_ui(self):
        title_label = tk.Label(
            self.root,
            text=f"Messenger - Logged in as {self.username}",
            font=("Arial", 14, "bold")
        )
        title_label.pack(pady=10)

        self.messages_box = tk.Text(self.root, height=10, width=50, wrap=tk.WORD)
        self.messages_box.pack(pady=10)

        self.private_messages_box = tk.Text(
            self.root,
            height=7,
            width=50,
            wrap=tk.WORD,
            bg="lightgray"
        )
        self.private_messages_box.pack(pady=10)

        self.message_entry = tk.Entry(self.root, width=50)
        self.message_entry.pack(pady=10)

        send_button = tk.Button(
            self.root,
            text="Send Public Message",
            command=self.send_message
        )
        send_button.pack(pady=5)

        users_label = tk.Label(self.root, text="Connected Users:")
        users_label.pack()

        self.users_listbox = tk.Listbox(self.root, height=8, width=50)
        self.users_listbox.pack(pady=10)

        send_private_button = tk.Button(
            self.root,
            text="Send Private Message",
            command=self.send_private_message
        )
        send_private_button.pack(pady=5)


# =========================
# Run Server + Client
# =========================

def start_server():
    server = MessengerServer()
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()


def start_client():
    root = tk.Tk()
    root.withdraw()

    username = simpledialog.askstring("Username", "Enter your username:")

    if not username:
        return

    root.deiconify()
    root.title("Messenger")

    try:
        client = MessengerClient(root, username)
        client.create_ui()
        client.start()
        root.mainloop()

    except ConnectionRefusedError:
        messagebox.showerror("Connection Error", "Server is not running.")


def start_server_and_client():
    start_server()
    start_client()


if __name__ == "__main__":
    start_server_and_client()