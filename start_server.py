import http.server
import socketserver
import webbrowser
import os
import socket

# 查找可用端口
def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

# 获取可用端口
PORT = find_free_port()

# 切换到当前目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 添加CORS头部，允许跨域请求
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

# 启动服务器
with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    # 获取本机IP地址
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    print(f"服务器启动成功！")
    print(f"本地访问: http://localhost:{PORT}")
    print(f"手机访问: http://{local_ip}:{PORT}")
    print("按 Ctrl+C 停止服务器")

    # 自动打开浏览器
    webbrowser.open(f"http://localhost:{PORT}/2.html")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
