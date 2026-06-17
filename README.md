# Python TCP Messenger with Private Messaging

A desktop messaging application built with Python, Socket Programming, Multithreading, and Tkinter.

The project allows multiple users to communicate over a TCP network through public chat messages and private conversations. It includes real-time user discovery, threaded communication, GUI interaction, and client-server architecture.

---

## 📋 Overview

This project implements a real-time messaging system using a client-server architecture.

The server manages connected users, distributes messages, and handles private communication between clients.

The application provides:

* Public chat messaging
* Private messaging between users
* Real-time connected users list
* Multi-threaded communication
* Graphical user interface
* Automatic user join/leave notifications

The project demonstrates Networking, Concurrent Programming, GUI Development, and TCP Socket Communication in Python.

---

## 🗂️ Project Structure

```text
├── messenger.py
├── README.md
└── Requirements
    └── Python 3.x
```

---

## ✨ Features

* 💬 Public chat system
* 🔒 Private messaging
* 👥 Live connected users list
* ⚡ Real-time communication
* 🖥️ Tkinter graphical interface
* 🔄 Multi-threaded networking
* 📢 Join and leave notifications
* 🚫 Duplicate username protection
* 📡 TCP/IP communication
* 🛠 Error handling and connection management

---

## 🧠 How It Works

### 1. Start the Server

The server initializes a TCP socket and begins listening for incoming connections.

```python
self.server_socket.listen(5)
```

The server continuously waits for new clients and creates a dedicated thread for each connection.

---

### 2. User Authentication

When a client connects, a username is requested.

```python
username = client_socket.recv(1024).decode("utf-8")
```

The server validates that the username is unique before allowing the user to join the chat.

---

### 3. Client Registration

Connected users are stored in a dictionary.

```python
self.clients[username] = client_socket
```

This allows the server to quickly locate users when sending messages.

---

### 4. Public Messaging

Messages sent by a user are broadcast to all other connected users.

```python
self.broadcast(username, message)
```

Every client immediately receives the new message and updates its interface.

---

### 5. Private Messaging

Private messages are sent directly to a selected user.

```python
private:TargetUser:Hello
```

The server identifies the recipient and forwards the message only to that user.

---

### 6. User List Synchronization

Whenever a user joins or leaves:

```python
self.send_client_list()
```

The server distributes an updated list of active users to every connected client.

---

### 7. Multithreading

Each connected client receives its own communication thread.

```python
threading.Thread(...)
```

This allows multiple users to send and receive messages simultaneously without blocking the application.

---

### 8. Safe GUI Updates

Incoming network messages are transferred safely to the Tkinter main thread.

```python
root.after(...)
```

This prevents crashes caused by updating GUI elements from worker threads.

---

## ⚙️ Main Components

| Component | Purpose                    |
| --------- | -------------------------- |
| Socket    | TCP Communication          |
| Threading | Concurrent Client Handling |
| Tkinter   | Graphical User Interface   |
| Server    | Message Routing            |
| Client    | User Interaction           |
| TCP/IP    | Network Transport          |

---

## 📡 Communication Flow

### Client Connection

```text
Client
   ↓
Server
   ↓
User Registered
   ↓
Updated User List Sent
```

---

### Public Message

```text
User A
   ↓
Server
   ↓
All Connected Users
```

---

### Private Message

```text
User A
   ↓
Server
   ↓
User B
```

---

## 🎮 Available Functions

### Public Message

```text
Hello everyone!
```

Broadcasts a message to all connected users.

---

### Private Message

Select a user from the connected users list.

```text
Hello John
```

The message is sent only to the selected recipient.

---

### User Discovery

The application automatically displays all active users.

```text
Connected Users:
- Alice
- Bob
- Charlie
```

The list updates whenever users join or leave.

---

## 🔄 Message Types

### Public Chat

```text
message:username:text
```

Used for normal chat communication.

---

### Private Chat

```text
private:username:text
```

Used for direct user-to-user communication.

---

### System Notification

```text
system:user joined
```

Used for server-generated events.

---

### User List Update

```text
clients_list:user1,user2,user3
```

Used to synchronize connected clients.

---

## 🖥️ User Interface

The application consists of:

### Public Chat Window

Displays:

* Incoming messages
* Outgoing messages
* System notifications

---

### Private Chat Window

Displays:

* Private conversations
* Sent private messages
* Received private messages

---

### User List

Displays:

* Online users
* Available private message recipients

---

### Message Input

Allows users to:

* Enter text
* Send public messages
* Send private messages

---

## 🛠️ Technologies Used

| Technology | Purpose                   |
| ---------- | ------------------------- |
| Python     | Main programming language |
| Socket     | Network communication     |
| Threading  | Multi-client support      |
| Tkinter    | GUI development           |
| TCP/IP     | Reliable communication    |

---

## 🚀 How to Run

### 1. Install Python

Install Python 3.10 or newer.

Verify installation:

```bash
python --version
```

---

### 2. Save the Project

Place the Python file in a project folder.

```text
Messenger/
│
├── messenger.py
└── README.md
```

---

### 3. Start the Application

Run:

```bash
python messenger.py
```

---

### 4. Enter Username

When prompted:

```text
Enter your username:
```

Provide a unique username.

---

### 5. Open Additional Clients

Run the application in multiple terminals or computers.

Example:

```text
User1
User2
User3
```

All users will automatically appear in the connected users list.

---

## 📊 Example Usage

### Public Chat

```text
You:
Hello everyone!
```

Result:

```text
User1:
Hello everyone!
```

Displayed to all connected clients.

---

### Private Chat

Select:

```text
User2
```

Send:

```text
Meeting at 3 PM
```

Result:

```text
Private message delivered only to User2
```

---

### User Join

```text
John joined the chat
```

All connected users receive a notification.

---

## 🔮 Future Improvements

* 🔑 User authentication system
* 🗄️ Database integration
* 📜 Chat history persistence
* 🌐 Multi-device support
* 🔒 End-to-end encryption
* 📁 File sharing
* 🎤 Voice messages
* 📷 Image sharing
* 🌙 Dark mode interface
* ☁️ Cloud deployment
* 👤 User profiles
* 📱 Mobile application

---

## 👨‍💻 Author

Developed as a Networking and Desktop Application project using Python, TCP Sockets, Multithreading, and Tkinter.

The project demonstrates client-server communication, concurrent programming, GUI development, and real-time messaging systems.
