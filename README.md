# exc2-7-2  
A simple Netwrok protocol designed to invoke specific actions in the server machine. Each message is composed of a command, denoting the intended action, and accompanying binary data.

        Command Length+Command+Data Length+Data

        Command Length: 4 bytes (unsigned integer, network byte order)  
        Command: Variable length, ASCII-encoded string  
        Data Length: 4 bytes (unsigned integer, network byte order)  
        Data: Variable length, binary data relevant to the specified command.  

sequence diagram (created using plantuml.com):   
![sequence](https://github.com/EniacARC/exc2-7-2/assets/94797541/3c66b397-81c7-40c1-9e89-74aa1ab4ae40)
