import socket
import struct
import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QHeaderView

# Define a function to send a request to a Minecraft server and receive a response
def query_server(address, port):
    # Create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set a timeout for the socket
    s.settimeout(1)
    # Connect to the server
    s.connect((address, port))
    # Send a request to the server
    s.send(b'\xFE\x01')
    # Receive a response from the server
    response = s.recv(1024)
    # Close the socket
    s.close()
    # Check if the response is valid
    if response[0] != b'\xFF':
        return None
    # Split the response into pieces
    pieces = response[3:].split(b'\x00')
    # Return the server information
    return {
        'description': pieces[0].decode('utf-8'),
        'players': int(pieces[1]),
        'max_players': int(pieces[2])
    }

# Define a class for the main window of the GUI
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set the window title
        self.setWindowTitle('Minecraft Server Scanner')
        # Create a table view to display the server information
        self.table_view = QTableView(self)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setCentralWidget(self.table_view)
        # Create a timer to refresh the server list every 5 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(5000)
        # Refresh the server list
        self.refresh()
    
    # Define a function to refresh the server list
    def refresh(self):
        # Create a model to store the server information
        model = QStandardItemModel(0, 3, self)
        model.setHorizontalHeaderLabels(['Address', 'Description', 'Players'])
        # Iterate over a range of IP addresses
        for i in range(1, 255):
            # Try to query the server at the current address
            try:
                info = query_server('192.168.1.' + str(i), 25565)
                if info:
                    # Add the server to the model
                    address_item = QStandardItem('192.168.1.' + str(i))
                    address_item.setTextAlignment(Qt.AlignCenter)
                    description_item = QStandard
