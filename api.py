#!/usr/bin/python3

import http.server
import socketserver

import os

PORT = 80
HOST = "0.0.0.0"


class My_http_handler(http.server.BaseHTTPRequestHandler):

    def send_error(self):
        self.send_response(404)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes('{"error": "No video ID provided"}\n', "utf-8"))

    def do_GET(self):
        path_str = self.path[1:] if self.path[-1] != "/" else self.path[1:-1]
        path_lst = path_str.split("/")
        if (len(path_lst) == 1) and (path_lst[0].strip() != ""):
            video_id = path_lst[0]
            video_filename = video_id + ".mp4"
            os.system("youtube-dl -o '%(id)s.%(ext)s' -f mp4 https://www.youtube.com/watch?v=" + video_id)
            try:
                with open(video_filename, "rb") as vf:
                    video_as_bytes = vf.read()
                os.remove(video_filename)
                self.send_response(200)
                self.send_header("Content-type", "media/mp4")
                self.end_headers()
                self.wfile.write(video_as_bytes)
            except:
                self.send_error()
        else:
            self.send_error()


if __name__ == "__main__":
    with socketserver.TCPServer((HOST, PORT), My_http_handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
