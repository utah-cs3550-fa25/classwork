import http.server

def router(req):
    write_counter(query_counter() + 1)

    if req.path == "/charlie.png" and\
       req.client_address[0] == "::1":
        req.send_header("Content-Type", "image/png")
        return load_static_file("jim.png")
    elif req.path == "/style.css":
        req.send_header("Content-Type", "text/css")
        return load_static_file("style.css")
    else:
        req.send_header("Content-Type", "text/html")
        return load_template("index.html", query_counter())

def load_static_file(filename):
    body = open(filename, "rb").read()
    return body
    
def load_template(filename, COUNTER):
    body = open(filename, "r").read()
    body = body.replace("{COUNTER}", str(COUNTER))
    return body.encode("utf8")
    
def query_counter():
    try:
        with open("counter.txt", "r") as f:
            COUNTER = int(f.read().strip())
    except FileNotFoundError:
        COUNTER = 0
    
    return COUNTER

def write_counter(COUNTER):
    with open("counter.txt", "w") as f:
        f.write(str(COUNTER))

class Server(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global COUNTER
        self.send_response(200)

        body = router(self)

        self.end_headers()
        self.wfile.write(body)

if __name__ == '__main__':
    http.server.test(HandlerClass=Server, port=8001)
