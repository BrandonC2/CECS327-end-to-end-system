import socket
"""
    Server:
    1.	Receives the message from the client. 
    2.	Change the letters of the message to “capital letters” 
        and send it back to the client by using the same socket. 
    3.	The server should be able to send multiple messages to the client. 
        You may need to consider using the infinite loop 
        as we discussed in the class. 

    User Manual:
    1. Input a valid/open port
    2. Wait for a client to connect and respond
    3. Server shuts off when client disconnect 

For assignment 8:
        Update your TCP server from Assignment 6 to:
    • Connect to the database created in Assignment 7 to retrieve relevant IoT data.
    • Use metadata for each IoT device created in dataniz to manage and process queries
    effectively. Metadata might include device ID, data source type, time zone, and unit of
    measure.
    • Perform calculations or unit conversions where needed:
    - Convert moisture readings to RH% (Relative Humidity).
    - Provide results in PST and imperial units (e.g., gallons, kWh).
    • Use an efficient data structure (e.g., binary tree) for searching and managing the data
"""

# Server Connection Info
# Router IP: 192.168.1.14
# Server Port: 4000
# Public IP: 45.50.84.18

def server():
    # Creates socket
    Port = int(input("Port number: "))
    myTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Binds to user input port, open to communication from any IP address
    myTCPSocket.bind(('0.0.0.0', Port))

    # Start listening for incoming connections
    myTCPSocket.listen(5)
    print(f"Server listening on port {Port}...")

    # Accept an incoming connection from a client
    incomingSocket, incomingAddress = myTCPSocket.accept()
    print(f"Connection established with {incomingAddress}")

    # infinite runloop until condition to exit is met
    running = True
    while running:
        # Receive data from the client
        myData = incomingSocket.recv(1024)

        # Ends loop when no message is sent by client (i.e client quit)
        if not myData:
            print("Server Disconnect")
            break

        # Decode the received data (bytes to string) and convert to uppercase
        someData = myData.decode("utf-8")

        # Ends loop when EXIT is typed by user (alt case to close server)
        if someData == "EXIT":
            print("Client Disconnect")
            break

        print(f"Client sends message: {someData}")

        # Converts user message to Uppercase, includes exit statement
        someData = ' '.join([someData, "(Enter 'EXIT' to Disconnect from server)"])
        someData = someData.upper()

        # Send the updated uppercase data back to client as response
        incomingSocket.send(bytearray(someData, encoding="utf-8"))

    # Close connection with client
    incomingSocket.close()
    print("Connection closed.")


if __name__ == "__main__":

    # Run the server function
    server()
