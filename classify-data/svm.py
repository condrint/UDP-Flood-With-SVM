import numpy
import os
from sklearn import svm
from collections import deque

"""
SVM monitors the rate of incoming packets and will classify if its good/bad
Input and Dataset for SVM:
Source IP, Dest IP, Packet Interval, and Protocl
"""

class SVM:
    def __init__(self):
        """
        train the model from generated training data in generate-data folder
        """
        data = numpy.loadtxt(open('../generate-data/test.csv', 'rb'), delimiter=',', dtype='str')

        self.svm = svm.SVC()

        # train the model - y values are locationed in last (index 3) column
        self.svm.fit(data[:, 0:3], data[:, 3])

        # initialize variables for classification
        self.packetsSeen = 0
        self.packetsClassifiedCorrectly = 0

        # these two queues keep track of packets seen in the last second and evict
        # older entries everytime a new packet comes in
        self.totalPacketsQueue = deque([])
        self.uniqueSourceIPsQueue = deque([])
        self.uniqueSourceIPs = {}



    def openFile(self, filename):
        """

        """
    
    def classify(self, packet):
        """
        input is an array with the following structure
        [time, source IP, destination IP, protocol, ttl]

        this function converts the input to
        [protocol, total # of packets in last second, total # of unique source IP addresses in last second, and normal / bad class]

        then prints out the current accuracy of the algorithm with the new packet classified

        returns nothing (so far)
        """


if __name__ == "__main__":
    while True:
        """
        Use tshark to compature data and store into a .csv file
        """
        #prediction('file.csv')
