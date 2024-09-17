# Complete Puzzle README

This README file contains both the explanation of the puzzle structure and a step-by-step write-up of the solution.

## Table of Contents
1. [Puzzle Explanation](#puzzle-explanation)
2. [Puzzle Write-up](#puzzle-write-up)
3. [Code Snippets](#code-snippets)

## Puzzle Explanation

### Overview

The puzzle consists of multiple stages, involving network packet analysis, website interaction, image steganography, and reverse engineering. Each stage provides clues or tools necessary for the next stage.

### Components

#### 1. Documentation File

- Created using the Scapy package in Python
- Contains network packets with DNS requests and responses
- Includes encrypted messages using Vigenère cipher

#### 2. Website

- Built using Flask
- Hosted on PythonAnywhere
- Requires specific referrer and language headers
- Password protected

![Initial website security message](images/image1.png)

#### 3. Image File

- Contains two hidden executable files (EXE)

![Downloaded image file](images/image9.png)

#### 4. Executable Files

##### First Executable (Python-compiled EXE)
- Implements a simple SMTP email server
- Expects an email from a specific address
- Sends back a message containing the flag

![Second executable SMTP server output](images/image12.png)

##### Second Executable (C-compiled EXE)
- Password validation file
- Uses a custom hashing algorithm
- Employs anti-debugging techniques
- Provides an encrypted email address when correct password is entered

![First executable password prompt](images/image11.png)

### Puzzle Flow

1. Analyze the documentation file to find the correct referrer for the website
2. Access the website using the correct referrer and language headers
3. Decrypt the Vigenère cipher messages to find the website password
4. Download the image file from the website
5. Extract the two executable files from the image
6. Reverse engineer or patch the second executable to obtain the email address
7. Use the first executable (SMTP server) to send an email to the obtained address
8. Receive the flag in the response email

## Puzzle Write-up

### Step 1: Website Access

- Open the provided website link
- Website is secure and requires access from another site

![Initial website security message](images/image1.png)

### Step 2: Finding the Referrer

- Analyze the documentation file using Wireshark
- Filter DNS requests with positive responses
- Identify the domain: www.SuperSecretSite.IRAN.gov.com

![Wireshark filtered DNS requests](images/image2.png)
![DNS response with correct domain](images/image3.png)

### Step 3: Accessing the Website

- Use Burp Suite to send an HTTP request with the correct referrer
- Change the language field to Persian

![Burp Suite modified HTTP request](images/image4.png)
![Server response indicating language issue](images/image5.png)

### Step 4: Decrypting the Password

- Extract packets with correct checksums using Python and Scapy
- Decrypt the Vigenère cipher messages
- Identify the password hint: "It needs to be pointy!"

![Extracted encrypted messages](images/image6.png)
![Vigenère cipher decryption](images/image7.png)

### Step 5: Downloading the Image

- Enter the password "Pointy" on the website
- Download the provided image

![Website after successful password entry](images/image8.png)
![Downloaded image file](images/image9.png)

### Step 6: Extracting Hidden Files

- Open the image in a hex editor
- Identify two MZ prefixes (PE format)
- Extract two executable files

![Hex editor view showing MZ prefixes](images/image10.png)

### Step 7: Analyzing the Executables

- First file: Requires a password
- Second file: SMTP server

![First executable password prompt](images/image11.png)
![Second executable SMTP server output](images/image12.png)

### Step 8: Reversing the Second Executable

- Perform static analysis due to anti-debugging measures
- Identify the encryption mechanism (XOR with a key)
- Patch the executable to bypass password check

![Disassembly showing encryption mechanism](images/image13.png)
![Code section highlighting patch location](images/image14.png)

### Step 9: Obtaining the Email Address

- Run the patched executable to get the email address

![Patched executable output with email address](images/image15.png)

### Step 10: Sending Email to SMTP Server

- Write a Python client to communicate with the SMTP server
- Send an email to the obtained address

![Python SMTP client code](images/image16.png)
![Terminal output of email being sent](images/image17.png)

### Step 11: Retrieving the Flag

- Receive the response email containing the flag

![Received email with flag](images/image18.png)

### Flag

The final flag is: Flag{Who_Dares_Winds}

## Code Snippets

### Documentation File Generation

```python
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
BAD_CHECKSUM_STR = "Lozablv: Wn lhs pfm exyswvt mfxg buxl ivqf pygbqaz gh twe rmj. Sdrkw lczq rmj fmnw mu hpvl shstrlq uwvr ipxbb vl yccbuxp hskbgb dtn lhsg zqsx. Bdb't lhs wodr hrwsz gagcua gh bd? Wa lhsg zqsx qd sucmw ivig rmj vwaxqizg ptl'i hpvgi dt i oxrisz jtw ic acxls hprlc bcurgrh? Cz nkc ncc fh gbdzrlqtr evmf pibuhpxhg gayi mwh zgks zrlntqb ngb rfmqxlrs bb tja hpnm aaoqz br? Sc gbn ptol rocgmbublv mwh'kc hixchqtr bb kcpr? Lb rmj hpvgi tjmer rwwvt rmj'fm fnnecarw rd hpvgi? Qig jayi mwh'kc ictq mm lovg? Zci ccg hd ncce tnpfbzxli. Amrm y bsuoxp dt bux medwfbrt umawcg. Gbbi rws mkvchgqix qwcxcblv ovq fyhhceuyiwwa. Jsxh gbnp ycj. Fmygh i sbewh. Xehtt mwh'kc pzqix. Gu mwh wmc'h kytgb mwhk fjaiabrn mwh pgaz jrvmbs i fmyiwagba. Ncc uttt pmrg upfvrw."
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
    random.shuffle(all_words) # Shuffle the words

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
```

### Custom Checksum Function

```python
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
```

### Website Code (Flask)

```python
from flask import Flask, request, Response, render_template_string

app = Flask(__name__)

REFERER = "www.SuperSecretSite.IRAN.gov.com"
PASSWORD_SUM = 57
HTML_FILE_PATH = '//home//yosef147yosef//mysite//form.html'
JPG_FILE_PATH = '//home//yosef147yosef//mysite//secret.jpg'

def read_file(file_path):
    """Read file content."""
    with open(file_path, 'r') as file:
        return file.read()

def read_binary_file(file_path):
    """Read binary file content."""
    with open(file_path, 'rb') as file:
        return file.read()

def check_referer():
    referer = request.headers.get('Referer', '')
    if REFERER not in referer:
        return False, "Sorry, you didnt got from our secure site. Only Iranin with very high clearnes can insert to that site, and only from this site this site can be reached"
    return True, ""

def check_language():
    accept_language = request.headers.get('Accept-Language', '')
    if 'fa' not in accept_language:
        return False, "Good try Mosad. But I see you didnt learn our langue yet!!"
    return True, ""

def send_jpg():
    try:
        jpg_data = read_binary_file(JPG_FILE_PATH)
    except FileNotFoundError:
        return "Error: JPG file not found", 500

    response = Response(jpg_data, mimetype='image/jpeg')
    response.headers['Content-Disposition'] = 'attachment; filename="secret.jpg"'
    return response

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        referer_check, referer_message = check_referer()
        if not referer_check:
            return referer_message, 403

        language_check, language_message = check_language()
        if not language_check:
            return language_message, 403

        html_content = read_file(