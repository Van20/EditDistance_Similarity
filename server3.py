import socket
import sys

class server:

    def __init__(self,file_name,port):
        self.file_name = file_name
        self.port = port

    def run(self):
        #create server socket using IPv4 addresses and TCP. AF_INET is for IPv4
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #allow reuse of port if we start program again after crash
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #Which machine and port
        server_address = ("0.0.0.0",self.port)
        server_socket.bind(server_address)
        #start listening
        server_socket.listen()

        #Read the entity names from the given file
        with open(self.file_name, encoding="utf-8") as entity_names_file:
            entity_names = entity_names_file.readlines()
        print ("Read %d entity names" % len(entity_names))
            

        while True:
            print("Waiting for connection on port %d.."% self.port,end="")
            #wait for incoming connection(blocking = will not proceed further in code until something happens)
            sys.stdout.flush()
            connection, client_address = server_socket.accept()
            print("incoming connection from %s:%d\n" % client_address, end="")

            #read what is being sent
            max_num_bytes = 4096
            request_bytes = connection.recv(max_num_bytes)
            request = request_bytes.decode("utf-8")
            print("Request : %s" % request.split("\r\n")[0])
            
            #compute the result
            answer_bytes = b"Go away"
            content_type = "text/plain"
            if(request.startswith("GET ")):
                file_name = request.split(" ")[1][1:]
                #check if there are parameters
                pos = file_name.find("?")
                parameters = ""
                if pos > 0:
                    parameters = file_name[pos:]
                    file_name = file_name[:pos]
                    
                
                try:
                    if file_name.find("/") >= 0:
                        raise("no")
                    with open(file_name, "rb") as f:
                        answer_bytes = f.read()
                except:
                        answer_bytes = b"File not found\n"  
                #if query is from example.html

                if file_name == "api" and parameters.startswith("?q="):
                    query_string = parameters[3:]
                    query = query_string.casefold()
                    result = []
                    for entity_name in entity_names:
                        if (entity_name.casefold()).startswith(query):
                            result.append("\""+entity_name.rstrip()+"\"")
                            if len(result) > 10:
                                result[-1] = "\"...\""
                                break
                    #print("Found %d or more matching entity names" % \ len(result))
                    answer_bytes = ("["+",".join(result)+"]").encode()
                    content_type = "application/json"
                   # answer_bytes = \
                   #     answer_bytes.decode() \
                   #             .replace("%QUERY%", query)\
                   #             .replace("%RESULT%", ", ".join(result))\
                   #             .encode()
    
                #Set the right media type
                if file_name.endswith(".html"):
                    content_type = "text/html"
                elif file_name.endswith(".jpg"):
                    content_type = "image/jpeg"
                elif file_name.endswith(".css"):
                    content_type = "text/css"
                elif file_name.endswith(".js"):
                    content_type = "application/javascript"
                        
               # print("Path: \"%s\"" % path)
            #answer_bytes = b"Thanks for the request\n"
            #send something back with correct HTTP headers
            content_length = len(answer_bytes)
            status_code = 200
            headers = "HTTP/1.1 %d OK\r\n" \
                      "Content-Length: %d\r\n" \
                      "Content-Type: %s\r\n" \
                      "\r\n" %\
                    (status_code, content_length, content_type)
            connection.sendall(headers.encode("utf-8"))                        
            connection.sendall(answer_bytes)

            #close connection
            print()
            connection.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 %s <file> <port>" % sys.argv[0])
        sys.exit(1)
    file_name = sys.argv[1] 
    port = int(sys.argv[2])
    server = server(file_name,port)
    server.run()
    
