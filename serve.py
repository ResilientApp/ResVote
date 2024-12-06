from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import fire
from src.util import load_server_config



def serve(config_path: str = "config.yaml"):

    host, port = load_server_config(config_path).unwrap()
    
    # Create server
    with SimpleXMLRPCServer((host, port),
                            requestHandler=SimpleXMLRPCRequestHandler) as server:
        server.register_introspection_functions()

        # Register pow() function; this will use the value of
        # pow.__name__ as the name, which is just 'pow'.
        server.register_function(pow)

        # Register a function under a different name
        def adder_function(x, y):
            return x + y
        server.register_function(adder_function, 'add')

        # Register an instance; all the methods of the instance are
        # published as XML-RPC methods (in this case, just 'mul').
        class MyFuncs:
            def mul(self, x, y):
                return x * y

        server.register_instance(MyFuncs())

        # Run the server's main loop
        server.serve_forever()
        
if __name__ == "__main__":
    fire.Fire(serve)