import hashlib
import random
from scapy.all import IP, UDP, Raw, wrpcap, DNS, DNSQR, DNSRR
import Server

# Configuration
SERVER_IP = '44.99.1.1'
PORT = 6553
FAKE_CLIENT_IP = '192.168.1.100'
DNS_SERVER = '8.8.8.8'

# Strings for responses
GOOD_CHECKSUM_STR = "Ivqf bq pb qzimghiam ktganzc ucz nej ivm rgexbmrkq ufwz hsg gcckcbs trtbtf. Bux pdqsrm gh bwg zmdr.Qg bq icw ehscr wa mft hwc Mfxg evej eib n lkxzm bg rws nnvch cn gac tbmzr.Rwwa Zxqhoor pyh svpkwehmq ucriar pc ptznbb ufwz mft waetcam Ublys"
BAD_CHECKSUM_STR = "Lozablv: Wn lhs pfm exyswvt mfxg buxl ivqf pygbqaz gh twe rmj. Sdrkw lczq rmj fmnw mu hpvl shstrlq uwvr ipxbb vl yccbuxp hskbgb dtn lhsg zqsx. Bdb'b lhs wodr hrwsz gagcua gh bd? Wa lhsg zqsx qd sucmw ivig rmj vwaxqizg ptl'i hpvgi dt i oxrisz jtw ic acxls hprlc bcurgrh? Cz nkc ncc fh gbdzrlqtr evmf pibuhpxhg gayi mwh zgks zrlntqb ngb rfmqxlrs bb tja hpnm aaoqz br? Sc gbn ptol rocgmbublv mwh'kc hixchqtr bb kcpr? Lb rmj hpvgi tjmer rwwvt rmj'fm fnnecarw rd hpvgi? Qig jayi mwh'kc ictq mm lovg? Zci ccg hd ncce tnpfbzxli. Amrm y bsuoxp dt bux medwfbrt umawcg. Gbbi rws mkvchgqix qwcxcblv ovq fyhhceuyiwwa. Jsxh gbnp ycj. Fmygh i sbewh. Xehtt mwh'kc pzqix. Gu mwh wmc'h kytgb mwhk fjaiabrn mwh pgaz jrvmbs i fmyiwagba. Ncc uttt pmrg upfvrw."
BAD_CHECKSUM_STR+="Ufiadjn, ag qxyg, W lbg'r vwdr t bpav.Uxpt'g tbhixbo nm wdi, svw.Wdi bneixbo gh kt?.Hpnm'q p pqazm!.Ivm abewh qf wygy iaw djzt by rtfzbkq.Pfm lhs vcvat zpfs nej sog, ybrizm qhevm, we tpt mwh zmcbi obrt?"

good_checksum_words = GOOD_CHECKSUM_STR.split('.')
bad_checksum_words = BAD_CHECKSUM_STR.split('.')

def create_packet(data, dst=SERVER_IP, dport=PORT, fake_ip=FAKE_CLIENT_IP, bad_checksum=False):
    """Create an IP/UDP packet with the given data and optionally a bad checksum."""
    packet = IP(src=fake_ip, dst=dst) / UDP(sport=12345, dport=dport) / Raw(load=data)
    checksum = Server.custom_checksum(packet)
    if bad_checksum:
        packet[UDP].chksum = (checksum+1)&0xffff
    else:
        packet[UDP].chksum = checksum
    return packet

def create_dns_request(domain):
    """Create a DNS request packet."""
    return IP(src=FAKE_CLIENT_IP, dst=DNS_SERVER) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=domain))

def create_dns_response(domain, ip=None):
    """Create a DNS response packet."""
    if ip:
        return IP(src=DNS_SERVER, dst=FAKE_CLIENT_IP) / UDP(sport=53) / DNS(qr=1, aa=1, qd=DNSQR(qname=domain), an=DNSRR(rrname=domain, rdata=ip))
    else:
        return IP(src=DNS_SERVER, dst=FAKE_CLIENT_IP) / UDP(sport=53) / DNS(qr=1, aa=1, rcode=3, qd=DNSQR(qname=domain))

def main():
    packets = []

    # Create interleaved request-response pairs
    all_words = [(word, True) for word in bad_checksum_words] + [(word, False) for word in good_checksum_words]
    random.shuffle(all_words)  # Shuffle the words

    for word, bad_checksum in all_words:
        request_packet = create_packet(word.encode(), bad_checksum=bad_checksum)
        packets.append(request_packet)

        response_word = "got " + word
        response_data = response_word.encode()
        response_packet = IP(src=SERVER_IP, dst=FAKE_CLIENT_IP) / UDP(dport=PORT) / Raw(load=response_data)
        packets.append(response_packet)

        if bad_checksum:
            print(f"Simulated sending response for bad checksum: {response_word}")
        else:
            print(f"Simulated sending response for good checksum: {response_word}")

    # Prepare DNS requests and responses
    correct_domain = "www.SuperSecretSite.IRAN.gov.com"
    similar_domains = [
        f"www.SuperSecret{chr(i)}.IRAN.gov.com" for i in range(97, 123)
    ] + [
        f"www.SuperSecretSite.{chr(i)}RAN.gov.com" for i in range(65, 71)
    ]

    # Prepare all DNS requests and responses
    dns_packets = []

    # Add 30 similar domain requests with non-existing responses
    for domain in random.sample(similar_domains, 30):
        dns_request = create_dns_request(domain)
        dns_response = create_dns_response(domain)
        dns_packets.extend([dns_request, dns_response])
        print(f"Added DNS request and non-existing response for: {domain}")

    # Add the correct domain request and response
    correct_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    dns_request = create_dns_request(correct_domain)
    dns_response = create_dns_response(correct_domain, correct_ip)
    dns_packets.extend([dns_request, dns_response])
    print(f"Added DNS request and correct response for: {correct_domain} -> {correct_ip}")

    # Shuffle all DNS packets
    random.shuffle(dns_packets)

    # Add shuffled DNS packets to the main packet list
    packets.extend(dns_packets)

    # Save all the packets to a single pcap file
    wrpcap('all_packets.pcap', packets)
    print("All packets saved to all_packets.pcap")

if __name__ == "__main__":
    main()
