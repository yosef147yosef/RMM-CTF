from scapy.all import *
def custom_checksum(packet):
    if not packet.haslayer(UDP):
        raise ValueError("Packet must contain a UDP layer")

    # Create a copy of the packet with the checksum field set to 0
    packet_no_checksum = packet.copy()
    packet_no_checksum[UDP].chksum = 0

    # Extract the raw bytes without the checksum field
    packet_bytes = bytes(packet_no_checksum)

    # Calculate checksum
    checksum = 0
    for i in range(0, len(packet_bytes)):
        word = packet_bytes[i]<<(i%4)
        checksum += word
    # One's complement
    checksum = ~checksum & 0xffff

    return checksum
result = []
def print_packets_with_checksum(pcap_file):
    global  result
    # Read the pcap file
    packets = rdpcap(pcap_file)
    for packet in packets:
        # Check if the packet has a UDP layer
        if UDP in packet:
            # Check if the UDP checksum is 0xffff
            chcksum = custom_checksum(packet)
            if packet[UDP].chksum == chcksum and packet[IP].src!='44.99.1.1':
                result += [packet[Raw].load.decode()]

# Replace 'your_file.pcap' with the path to your pcap file
pcap_file = 'all_packets.pcap'
print_packets_with_checksum(pcap_file)
print(result)