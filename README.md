# exc2-7-2  
A simple Netwrok protocol designed to invoke specific actions in the server machine. Each message is composed of a command, denoting the intended action, and accompanying binary data. The format includes fields for command length and data length, both represented as 4-byte unsigned integers in network byte order.  

        Command Length: 4 bytes (unsigned integer, network byte order)  
        Command: Variable length, ASCII-encoded string  
        Data Length: 4 bytes (unsigned integer, network byte order)  
        Data: Variable length, binary data relevant to the specified command.  

sequence diagram (created using plantuml.com):   
![sequence](https://github.com/EniacARC/exc2-7-2/assets/94797541/9c0cdc9e-ebea-4e33-a215-cdf3ab5dbdb8)

