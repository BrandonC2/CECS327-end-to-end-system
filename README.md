# CECS327-end-to-end-system

This program is designed to fetch data from NeonDB which is created through Dataniz, a website intended to create virtual IoT for experimental and demonstrational purposes.


# Pre-Req

1) pip install psycogy2-binary

# To use the program (using my existing IoT from Dataniz and table from NeonDB)

1) git clone this repo
    - git clone https://github.com/BrandonC2/CECS327_SP25_9.git

2) Get your private ip
    - For Mac: ifconfig, under 'env0'
    - For Windows: ipconfig

7) To run the program:
    - For Server: run 'python Server.py' in the proper directory, then enter the port you want to use
    - For Client: run 'python Client.py' in the proper directory, then enter your ip, and then your port

8) 'Exit' to exit or 'ctrl + c' to forcefully kill the process



# To create your own,

1) Create NeonDB account
    - Create a new project.

2) Create a Dataniz account
    - Link your NeonDB with Dataniz (Note: The data store type should be 'RDBMS').
    - Create your IoT's (make sure each device is has a board that has access to wifi).
    - Create your Metadata.

3) Check your NeonDB table to ensure that the data is being properly sent.
    - After 5 minutes, if there's no data, please restart as there could be wrong information inputted

4) git clone this repo
    - git clone https://github.com/BrandonC2/CECS327_SP25_9.git

5) In 'Server.py', replace the my NeonDB URL with your own.
    - Change the names to properly fit your own in the 'match/case' section

6) Get your private ip
    - For Mac: ifconfig, under 'env0'
    - For Windows: ipconfig

7) To run the program:
    - For Server: run 'python Server.py' in the proper directory, then enter the port you want to use
    - For Client: run 'python Client.py' in the proper directory, then enter your ip, and then your port

8) 'Exit' to exit or 'ctrl + c' to forcefully kill the process