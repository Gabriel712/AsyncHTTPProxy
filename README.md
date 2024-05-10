# AsyncHTTPProxy

AsyncHTTPProxy is a Python asynchronous HTTP proxy server designed to redirect traffic to another host and port. It leverages asyncio to handle multiple client connections concurrently. This proxy server is particularly useful in scenarios such as redirecting OpenVPN traffic over HTTP.

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/your_username/AsyncHTTPProxy.git
    ```

2. Navigate to the project directory:
    ```
    cd AsyncHTTPProxy
    ```

3. Install the required dependencies using pip:
    ```
    pip install -r requirements.txt
    ```

## Usage

Run the `OnlyRedirect.py` script with the necessary arguments:

```
python OnlyRedirect.py <proxy_host> <proxy_port> <destination_host> <destination_port> [--debug]
```

Replace `<proxy_host>`, `<proxy_port>`, `<destination_host>`, and `<destination_port>` with the appropriate values. The `--debug` flag is optional and enables debug output, including logging to a file.

Example:

```
python OnlyRedirect.py 0.0.0.0 8080 192.168.17.242 8080 --debug
```

## Contributing

Contributions are welcome! Feel free to open issues or pull requests for any improvements or fixes you'd like to see.
