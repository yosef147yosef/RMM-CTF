# Puzzle Write-up

This README file provides a step-by-step solution for the puzzle, including references to important images.

## Step 1: Website Access

- Open the provided website link
- Website is secure and requires access from another site

![Initial website security message](images/image1.png)

## Step 2: Finding the Referrer

- Analyze the documentation file using Wireshark
- Filter DNS requests with positive responses
- Identify the domain: www.SuperSecretSite.IRAN.gov.com

![Wireshark filtered DNS requests](images/image2.png)
![DNS response with correct domain](images/image3.png)

## Step 3: Accessing the Website

- Use Burp Suite to send an HTTP request with the correct referrer
- Change the language field to Persian

![Burp Suite modified HTTP request](images/image4.png)
![Server response indicating language issue](images/image5.png)

## Step 4: Decrypting the Password

- Extract packets with correct checksums using Python and Scapy
- Decrypt the Vigenère cipher messages
- Identify the password hint: "It needs to be pointy!"

![Extracted encrypted messages](images/image6.png)
![Vigenère cipher decryption](images/image7.png)

## Step 5: Downloading the Image

- Enter the password "Pointy" on the website
- Download the provided image

![Website after successful password entry](images/image8.png)
![Downloaded image file](images/image9.png)

## Step 6: Extracting Hidden Files

- Open the image in a hex editor
- Identify two MZ prefixes (PE format)
- Extract two executable files

![Hex editor view showing MZ prefixes](images/image10.png)

## Step 7: Analyzing the Executables

- First file: Requires a password
- Second file: SMTP server

![First executable password prompt](images/image11.png)
![Second executable SMTP server output](images/image12.png)

## Step 8: Reversing the Second Executable

- Perform static analysis due to anti-debugging measures
- Identify the encryption mechanism (XOR with a key)
- Patch the executable to bypass password check

![Disassembly showing encryption mechanism](images/image13.png)
![Code section highlighting patch location](images/image14.png)

## Step 9: Obtaining the Email Address

- Run the patched executable to get the email address

![Patched executable output with email address](images/image15.png)

## Step 10: Sending Email to SMTP Server

- Write a Python client to communicate with the SMTP server
- Send an email to the obtained address

![Python SMTP client code](images/image16.png)
![Terminal output of email being sent](images/image17.png)

## Step 11: Retrieving the Flag

- Receive the response email containing the flag

![Received email with flag](images/image18.png)

## Flag

The final flag is: Flag{Who_Dares_Winds}

[The rest of the file contains detailed explanations of each step, including code snippets and analysis of the reverse engineering process.]

Note: Ensure all image files are placed in an 'images' folder in the same directory as this README file.
