# Detecting UDP Flood with SVM

## Mininet & Pox 
### Software Requirements
- Python 2.7+
- VirutalBox (Ubuntu for Minimet simulations)

SDN VM: http://sdnhub.org/tutorials/sdn-tutorial-vm/

### SVM Parameters
- Entropy from Source IP (more random means more likely to be spoofed)
- Entropy from Destination IP
- Number of bytes per packet (lower number of bytes means more likely to be an attack)
- Number of packets/unique ports per second

### Related Papers
- https://www.hindawi.com/journals/scn/2018/9804061/
