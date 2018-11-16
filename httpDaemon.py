import os
import socketserver
from http.server import BaseHTTPRequestHandler
from urllib import parse
import shutil
import hashlib

def some_function(i):
    print("some_function got called " + str(i))


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        data = parse.urlparse(self.path)

        if data.path == '/download':
            params = parse.parse_qs(data.query)
            file_hash = params["hash"]
            common_path = "/home/user/Desktop"

            try:
                shutil.copyfile(common_path + "/Store/" + ''.join(file_hash)[:2] + "/" + ''.join(file_hash),
                                common_path + "/clientStore/" + ''.join(file_hash))
                self.send_response(200)
                self.end_headers()
                return

            except:
                self.send_error(400, "download unsuccessful")

        if data.path == '/upload':
            params = parse.parse_qs(data.query)

            try:
                file = open("/home/user/Desktop/clientStore/" + str(params["file"][0]))
                file_hash = hashlib.md5(file.read().encode('utf-8')).hexdigest()
                common_path = "/home/user/Desktop"
                if not os.path.exists(common_path + "/Store/" + str(file_hash[:2])):
                    os.mkdir(common_path + "/Store/" + str(file_hash[:2]))
                shutil.copyfile(common_path + "/clientStore/" + str(params["file"][0]),
                                common_path + "/Store/" + str(file_hash[:2] + "/" + file_hash))


                self.send_response(200)
                self.send_header("file_hash", file_hash)
                self.end_headers()
                return

            except:
                self.send_error(400, "upload unsuccessful")

        if data.path == '/delete':
            params = parse.parse_qs(data.query)
            file_hash = params["hash"]
            print(file_hash)

            try:
                path_to_file = "/home/user/Desktop/Store/" + ''.join(file_hash)[:2] + "/" + \
                               ''.join(file_hash)
                if os.path.isfile(path_to_file):
                    os.remove(path_to_file)
                print(path_to_file)
                self.send_response(200)
                self.end_headers()
                return

            except:
                self.send_error(400, "delete unsuccessful")

httpd = socketserver.TCPServer(("", 8080), MyHandler)
httpd.serve_forever()
