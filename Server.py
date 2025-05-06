import socket
import psycopg2

conn = psycopg2.connect("postgresql://neondb_owner:npg_gCjvMmcIH24Y@ep-jolly-river-a5huaine-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require")

cursor = conn.cursor()

# goal: create new dataniz account, and set it up correctly. 
# connect it to the neondb
# research each sensor and provide the appropriate calculations

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
    - Convert moisture readings to RH% (Relative Humidity)
    .
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
        if someData.upper() == "EXIT":
            print("Client Disconnect")
            break

        print(f"Client sends message: {someData}")

        """
         In this portion, connect to NeonDB
         Run queries
         Get data
         send to client
        """
        match someData:
            case "1": # convert the time from the database to PST
                print("Executing query #1 \n")
                #send query to NeonDB
                cursor.execute("""
                    SELECT
                    AVG((payload->>'DHT11 - Fridge1')::FLOAT) AS avg_moisture
                    FROM "NewKitchen_virtual"
                    WHERE
                    payload->>'board_name' = 'Fridge1'
                    AND to_timestamp((payload->>'timestamp')::BIGINT) AT TIME ZONE 'UTC' AT TIME ZONE 'America/Los_Angeles' >= NOW() - INTERVAL '3 hours';
                """)

                #store the data
                avg_moisture = cursor.fetchone()[0]

                #condition if there is no data for the last 3 hours
                if avg_moisture is not None:
                    someData = f"Average Fridge Moisture (last 3 hours): {avg_moisture:.2f}%\n"
                else:
                    someData = "Average Fridge Moisture (last 3 hours): Data not available\n"


            case "2":
                print("Executing query #2 \n")
                #send query to NeonDB
                cursor.execute("""
                    SELECT
                    AVG((payload->>'YF-S201 - Dishwasher')::FLOAT) AS avg_water_per_cycle
                    FROM "NewKitchen_virtual"
                    WHERE
                    payload->>'board_name' = 'Dishwasher';
                """)
                #store the data
                avg_water = cursor.fetchone()[0]
                # Conversion from Liters to Gallons
                avg_water = avg_water * 0.264172
                someData = (f"Average Dishwasher Water Per Cycle: {avg_water:.2f} Gallons\n")

            case "3":
                print("Executing query #3 \n")
                #send query to NeonDB
                #select each 
                cursor.execute("""
                    SELECT device, MAX(electricity) AS electricity
                    FROM (
                        SELECT 
                            payload->>'board_name' AS device,
                            AVG((payload->>'ACS712 - Dishwasher')::FLOAT) AS electricity
                        FROM "NewKitchen_virtual"
                        WHERE (payload::jsonb) ? 'ACS712 - Dishwasher'
                        GROUP BY payload->>'board_name'
                        
                        UNION ALL
                        
                        SELECT 
                            payload->>'board_name' AS device,
                            AVG((payload->>'ACS712 - Fridge2')::FLOAT) AS electricity
                        FROM "NewKitchen_virtual"
                        WHERE (payload::jsonb) ? 'ACS712 - Fridge2'
                        GROUP BY payload->>'board_name'
                        
                        UNION ALL
                        
                        SELECT 
                            payload->>'board_name' AS device,
                            AVG((payload->>'ACS712 - Fridge1')::FLOAT) AS electricity
                        FROM "NewKitchen_virtual"
                        WHERE (payload::jsonb) ? 'ACS712 - Fridge1'
                        GROUP BY payload->>'board_name'
                    ) AS all_data
                    GROUP BY device
                    ORDER BY electricity DESC
                    LIMIT 1;

                """)
                result = cursor.fetchone()
                device = result[0] if result and result[0] is not None else "Unknown"
                electricity = result[1] if result and result[1] is not None else 0.0
                # Conversion from Amps to kWh
                electricity = electricity * 5/ 1000
                someData = (f"Highest Electricity Consumer: {device} ({electricity:.2f} kW average per cycle)\n")
            

        # Send the updated uppercase data back to client as response
        incomingSocket.send(bytearray(someData, encoding="utf-8"))

    # Close connection with client
    incomingSocket.close()
    print("Connection closed.")


if __name__ == "__main__":

    # Run the server function
    server()
