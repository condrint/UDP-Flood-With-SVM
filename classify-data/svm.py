from __future__ import division
import numpy
import os
from sklearn import svm
from collections import deque

protocolIndicators = {
    6: 0,
    17: 1,
    1: 2,
}

# variable to change time frame of parameters
second = 10

class SVM:
    def __init__(self):
        """
        train the model from generated training data in generate-data folder
        """
        data = numpy.loadtxt(open('pox/forwarding/generate-data/processedData.csv', 'rb'), delimiter=',', dtype='str')

        self.svm = svm.SVC()

        # train the model - y values are locationed in last (index 3) column
        self.svm.fit(data[:, 0:4], data[:, 4])
                              
        # initialize variables for classification
        self.packetsSeen = 0
        self.packetsQueue = deque([])
        self.uniqueSourceIPs = {} 
        self.destinationIPHitCountInLastSecond = {}

        # used to calculate precision / accuracy (i think)
        self.normalPacketsCorrect = 0
        self.normalPacketsIncorrect = 0 # false positive
        self.badPacketsCorrect = 0
        self.badPacketsIncorrect = 0 # true negative

    def classify(self, packet):
        """
        input is an array with the following structure
        [time, source IP, destination IP, protocol, ttl]

        this function converts the input to
        [protocol, total # of packets in last second, total # of unique source IP addresses in last second, and normal / bad class]

        then prints out the current accuracy of the algorithm with the new packet classified

        returns nothing (so far)
        """
        print 'packet received'
        # convert ip address objects to strings
        packet[1], packet[2] = str(packet[1]), str(packet[2])
        print packet
        self._evictOldPackets(packet[0])
        self._updateQueue(packet)

        processedPacket = numpy.zeros((1, 4))
        processedPacket[:,0] = protocolIndicators[packet[3]]
        processedPacket[:,1] = len(self.packetsQueue)
        processedPacket[:,2] = len(self.uniqueSourceIPs)
        processedPacket[:,3] = len(self.destinationIPHitCountInLastSecond)
        classOfPacket = packet[4]

        prediction = self.svm.predict(processedPacket)
        self.packetsSeen += 1


        if prediction[0] == classOfPacket:
            if prediction == '1':
                self.badPacketsCorrect += 1
            else:
                self.normalPacketsCorrect += 1
        else:
            if prediction == '0':
                self.badPacketsIncorrect += 1
            else:
                self.normalPacketsIncorrect += 1
        
        print 'Current accuracy: ' + str((self.normalPacketsCorrect + self.badPacketsCorrect)/self.packetsSeen)
        print self.normalPacketsCorrect, self.normalPacketsIncorrect, self.badPacketsCorrect, self.badPacketsIncorrect
        print '\n'

    def _evictOldPackets(self, currentTime):
        """
        input is a new time value

        removes any packets older than a second from both queues and updates
        uniqueSourceIPs dictionary if necessary
        """
        if self.packetsQueue:

            # if the packet is older than one second pop it
            while currentTime - self.packetsQueue[0][0] > second:
                packet = self.packetsQueue.popleft()
                evictedPacketSrcIP, evictedPacketDstIP = packet[1], packet[2]
                
                
                self.uniqueSourceIPs[evictedPacketSrcIP] -= 1

                if self.uniqueSourceIPs[evictedPacketSrcIP] < 1:
                    del self.uniqueSourceIPs[evictedPacketSrcIP]

                self.destinationIPHitCountInLastSecond[evictedPacketDstIP] -= 1

                if self.destinationIPHitCountInLastSecond[evictedPacketDstIP] < 1:
                    del self.destinationIPHitCountInLastSecond[evictedPacketDstIP]
        
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

        newIP = packet[2]
        if newIP in self.destinationIPHitCountInLastSecond:
            self.destinationIPHitCountInLastSecond[newIP] += 1
        else:
            self.destinationIPHitCountInLastSecond[newIP] = 1



