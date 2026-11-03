# -*- coding: utf-8 -*-
"""
HTTP-сервер для локального предпросмотра сайта «Успешный Mind»
Поддерживает многопоточность, Three.js 3D-модели (.glb, .gltf),
шейдерные текстуры (.exr, .bin), webfonts (.woff2, .woff) и чистый вывод UTF-8.
"""
import http.server
import socket
import os
import sys

# Настройка UTF-8 вывода для Windows консоли
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Переход в директорию сайта
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def find_free_port(preferred=8090):
    for port in [preferred, 8091, 8092, 8088, 8888, 8080, 5000, 3000]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
                return port
            except OSError:
                continue
    return preferred

port = find_free_port()
url = f"http://localhost:{port}/"

print("=" * 60)
print(f"  Сайт «Успешный Mind» запущен!")
print(f"  Адрес в браузере: {url}")
print("=" * 60)

class CustomHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Добавляем заголовки для предотвращения некорректного кэширования при локальной разработке
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

CustomHTTPHandler.extensions_map.update({
    '.glb': 'model/gltf-binary',
    '.gltf': 'model/gltf+json',
    '.exr': 'image/x-exr',
    '.bin': 'application/octet-stream',
    '.woff2': 'font/woff2',
    '.woff': 'font/woff',
    '.svg': 'image/svg+xml',
    '.webmanifest': 'application/manifest+json',
})

try:
    with http.server.ThreadingHTTPServer(('localhost', port), CustomHTTPHandler) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nСервер остановлен.")
except Exception as e:
    print("Ошибка сервера:", e)
