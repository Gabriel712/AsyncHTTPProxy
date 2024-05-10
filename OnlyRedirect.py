import asyncio
import argparse
import logging

class HTTPProxyServer:
    def __init__(self, host, port, destination_host, destination_port, debug=False):
        """
        Initialize the HTTP proxy server.

        Args:
            host (str): The IP address of the host where the proxy server will run.
            port (int): The port where the proxy server will listen for connections.
            destination_host (str): The IP address of the destination host.
            destination_port (int): The port of the destination host.
            debug (bool): If True, enables debug output.
        """
        self.host = host
        self.port = port
        self.destination_host = destination_host
        self.destination_port = destination_port
        self.debug = debug

        # Logger configuration
        self.logger = logging.getLogger(__name__)
        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Add a file handler if debug mode is enabled
        if debug:
            file_handler = logging.FileHandler('debug.log')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    async def handle_client(self, client_reader, client_writer):
        """
        Handle a client connection.

        Args:
            client_reader: The reader for client data.
            client_writer: The writer for client data.
        """
        try:
            destination_reader, destination_writer = await asyncio.open_connection(
                self.destination_host, self.destination_port
            )
            self.logger.debug(f"Connected to destination server at {self.destination_host}:{self.destination_port}")

            async def transfer_data(source, target, description):
                """
                Transfer data from a source to a target.

                Args:
                    source: The data source reader.
                    target: The data target writer.
                    description (str): Description of the data transfer direction.
                """
                try:
                    while True:
                        data = await source.read(4096)
                        if not data:
                            self.logger.debug(f"No more data from {description}.")
                            break
                        self.logger.debug(f"Transferring {len(data)} bytes from {description}: {data}")
                        target.write(data)
                        await target.drain()
                except Exception as e:
                    self.logger.error(f"Error during data transfer from {description}: {e}")

            # Execute both transfer coroutines until they finish
            await asyncio.gather(
                transfer_data(client_reader, destination_writer, "client to destination"),
                transfer_data(destination_reader, client_writer, "destination to client")
            )
        finally:
            client_writer.close()
            destination_writer.close()
            self.logger.debug("Closed connections")

    async def start_server(self):
        """
        Start the HTTPProxy server.
        """
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        self.logger.info(f'Server HTTP started at {self.host}:{self.port}')
        async with server:
            await server.serve_forever()

def parse_args():
    """
    Parse command line arguments.

    Returns:
        Namespace: The namespace containing the arguments.
    """
    parser = argparse.ArgumentParser(description="HTTP Proxy Server to redirect traffic to another host and port.")
    parser.add_argument("host", help="The IP address of the HTTP Proxy server.")
    parser.add_argument("port", type=int, help="The port of the HTTP Proxy server.")
    parser.add_argument("destination_host", help="The IP address of the destination host.")
    parser.add_argument("destination_port", type=int, help="The port of the destination host.")
    parser.add_argument("--debug", action="store_true", help="Enable debug output and save to a file.")
    return parser.parse_args()

def main():
    args = parse_args()
    proxy_server = HTTPProxyServer(args.host, args.port, args.destination_host, args.destination_port, args.debug)
    asyncio.run(proxy_server.start_server())

if __name__ == '__main__':
    main()
