import socket
#tạo socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#kết nối máy chủ từ xa 
server_ip = "127.0.0.1"  # Thay bằng địa chỉ IP hoặc hostname đích
server_port = 8080  # Thay bằng cổng đích
try:
    client_socket.connect((server_ip, server_port))
    print(f"Kết nối thành công đến {server_ip}:{server_port}")
    client_socket.send(b"Hello, Server!")
    response = client_socket.recv(1024)
    print(f"Phản hồi từ máy chủ: {response.decode()}")
except Exception as e:
    print(f"Kết nối thất bại: {e}")
finally:
    client_socket.close()