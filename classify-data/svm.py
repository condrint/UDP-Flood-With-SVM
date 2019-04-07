import numpy
import os
from sklearn import svm
from collections import deque

protocolIndicators = {
    '6': 0,
    '17': 1,
}

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
        self.packetsQueue = deque([])
        self.uniqueSourceIPs = {}

        # used to calculate precision / accuracy (i think)
        self.normalPacketsCorrect = 0
        self.normalPacketsIncorrect = 0
        self.badPacketsCorrect = 0
        self.badPacketsIncorrect = 0

    def classify(self, packet):
        """
        input is an array with the following structure
        [time, source IP, destination IP, protocol, ttl]

        this function converts the input to
        [protocol, total # of packets in last second, total # of unique source IP addresses in last second, and normal / bad class]

        then prints out the current accuracy of the algorithm with the new packet classified

        returns nothing (so far)
        """
        self._evictOldPackets(packet[0])
        self._updateQueue(packet)

        processedPacket = numpy.zeros((1, 3))
        processedPacket[0] = protocolIndicators[packet[3]]
        processedPacket[1] = len(self.packetsQueue)
        processedPacket[2] = len(self.uniqueSourceIPs)
        classOfPacket = numpy.zeros((1, 1))
        classOfPacket[0] = 1 if packet[4]  == '18' else 0

        prediction = self.svm.predict(processedPacket)

        if prediction == classOfPacket:
            if prediction == 1:
                self.badPacketsCorrect += 1
            else:
                self.normalPacketsCorrect += 1
        else:
            if prediction == 1:
                self.badPacketsIncorrect += 1
            else:
                self.normalPacketsIncorrect += 1
        
        self.packetsSeen += 1
        print('Current accuracy: ' + str((self.normalPacketsCorrect + self.badPacketsCorrect)/self.packetsSeen) + '%')

    def _evictOldPackets(self, currentTime):
        """
        input is a new time value

        removes any packets older than a second from both queues and updates
        uniqueSourceIPs dictionary if necessary
        """
        if self.packetsQueue:

            # if the packet is older than one second pop it
            while currentTime - self.packetsQueue[0][0] > 1:
                evictedPacketIP = self.packetsQueue.popleft()[1]
                self.uniqueSourceIPs[evictedPacketIP] -= 1

                if self.uniqueSourceIPs[evictedPacketIP] < 1:
                    del self.uniqueSourceIPs[evictedPacketIP]
        
        return True
        
    def _updateQueue(self, packet):
        """
        add new packet to queue and update uniqueSourceIPs
        """
        self.packetsQueue.append(packet)
        newIP = packet[1]

        if newIP in self.uniqueSourceIPs:
            self.uniqueSourceIPs[newIP] += 1
        else:
            self.uniqueSourceIPs[newIP] = 1

