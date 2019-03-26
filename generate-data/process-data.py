import numpy

# This data structure encodes the data for the model instead of using 
# arbitrary protocol numbers. This should probably be imported from the root directory somehow
protocolIndicators = {
    '6': 0,
    '17': 1,
}


def processData():
    """
    input: no parameters, but expects a csv in the same directory with columns:
    time, source IP, destination IP, protocol, destination port

    output: a csv in the same directory named processed-data.csv with the following columns:
    protocol, total # of packets in last second, total # of unique destination ports in last second,
    and total # of unique source IP addresses in last second
    """

    # import the all the raw data as strings into a numpy array
    data = numpy.loadtxt(open('test.csv', 'rb'), delimiter=',', skiprows=0, dtype='str')

    # ensure packets are sorted by time
    data = numpy.sort(data, axis=0)

    for i in range(len(data)):
        # convert protocol to encoded value
        data[i, 3] = protocolIndicators[data[i, 3]]

    # create new array that will be used to generate processed-data.csv
    processedData = numpy.zeros((len(data), 4))

    # copy over protocol
    processedData[:, 0] = data[:, 3]

    # calculate total # of packets in last second for each packet
    # initialize pointers and fill out first row
    lowPointer = 0
    processedData[0, 1] = 0
    for highPointer in range(1, len(data)):
        while lowPointer < highPointer and float(data[highPointer, 0]) - float(data[lowPointer, 0]) > 1:
            lowPointer += 1

        # for this next line, lowPointer will always point to a packet
        # that is within one second of the currently pointed to packet
        # by highPointer. The difference is the total number of packets 
        # in the last second + one for the current packet
        processedData[highPointer, 1] = 1 + (highPointer - lowPointer)

    # calculate total # of unique source IPs in last second for each packet
    uniqueIPsInLastSecond = {} # a counter for # of unique IPs - when an IP's count reaches zero it's removed
    lowPointer = 0

    # add first packet's IP to counter
    uniqueIPsInLastSecond[data[lowPointer, 1]] = 1
    
    for highPointer in range(1, len(data)):
        newIP = data[highPointer, 1]
        if newIP in uniqueIPsInLastSecond:
            uniqueIPsInLastSecond[newIP] += 1
        else:
            uniqueIPsInLastSecond[newIP] = 1

        # remove any IPs from uniqueIPsInLastSecond if they're more than a second old and
        # their count reaches 0
        while lowPointer < highPointer and float(data[highPointer, 0]) - float(data[lowPointer, 0]) > 1:
            IPtoRemove = data[lowPointer, 1]
            uniqueIPsInLastSecond[IPtoRemove] -= 1

            if uniqueIPsInLastSecond[IPtoRemove] < 1:
                del uniqueIPsInLastSecond[IPtoRemove]
            lowPointer += 1 
        
        processedData[highPointer, 3] = len(uniqueIPsInLastSecond)
        
    print(processedData)


if __name__ == '__main__':
    processData()