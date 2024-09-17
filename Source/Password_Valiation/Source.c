#include <windows.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>



#define HASH_SIZE 32
#define PASSWORD_ATTEMPT_DELAY 100 // milliseconds
typedef void (*func_ptr)();
void animate_text(const char* text) {
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hConsole, FOREGROUND_GREEN); // Set text color to green
    int length = strlen(text);
    for (int i = 0; i <= length; i++) {
        printf("\r%.*s", i, text);
        Sleep(100); // sleep for 0.1 seconds
    }
    SetConsoleTextAttribute(hConsole, FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE); // Reset text color
    printf("\n");
}

// Pre-computed hash of the password
const unsigned char PASSWORD_HASH[HASH_SIZE] = {
    0x8f, 0x1a, 0x3b, 0x2c, 0x4d, 0x5e, 0x6f, 0x7a,
    0x9b, 0x8c, 0x7d, 0x6e, 0x5f, 0x4a, 0x3b, 0x2c,
    0x1d, 0x0e, 0xf1, 0xe2, 0xd3, 0xc4, 0xb5, 0xa6,
    0x97, 0x88, 0x79, 0x6a, 0x5b, 0x4c, 0x3d, 0x2e
};
bool check_for_debugger() {
    // Check if a debugger is present
    if (IsDebuggerPresent()) {
        return true;
    }

    return false;
}

void custom_hash(const char* input, unsigned char* output) {
    unsigned int state[8] = { 0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
                             0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19 };

    size_t input_len = strlen(input);
    unsigned char buffer[64] = { 0 };
    memcpy(buffer, input, input_len > 64 ? 64 : input_len);

    for (int i = 0; i < 64; i++) {
        unsigned int temp1 = state[7] +
            ((state[4] >> 6 | state[4] << 26) ^ (state[4] >> 11 | state[4] << 21) ^ (state[4] >> 25 | state[4] << 7)) +
            ((state[4] & state[5]) ^ (~state[4] & state[6])) +
            0x428a2f98 + buffer[i];
        unsigned int temp2 = ((state[0] >> 2 | state[0] << 30) ^ (state[0] >> 13 | state[0] << 19) ^ (state[0] >> 22 | state[0] << 10)) +
            ((state[0] & state[1]) ^ (state[0] & state[2]) ^ (state[1] & state[2]));

        state[7] = state[6];
        state[6] = state[5];
        state[5] = state[4];
        state[4] = state[3] + temp1;
        state[3] = state[2];
        state[2] = state[1];
        state[1] = state[0];
        state[0] = temp1 + temp2;
    }

    for (int i = 0; i < 8; i++) {
        output[i * 4] = (state[i] >> 24) & 0xFF;
        output[i * 4 + 1] = (state[i] >> 16) & 0xFF;
        output[i * 4 + 2] = (state[i] >> 8) & 0xFF;
        output[i * 4 + 3] = state[i] & 0xFF;
    }
}

unsigned char data[] = {
    0xA3, 0x98, 0x8B, 0x84, 0xB5, 0xA7, 0x83, 0x99,
    0x99, 0x8F, 0x86, 0x8F, 0x99, 0xAA, 0xA3, 0x98,
    0x8B, 0x84, 0xC4, 0x8D, 0x85, 0x9C, 0xC4, 0x89,
    0x85, 0xC4, 0x83, 0x86,0xEA
};

unsigned char XOR_KEY = 0xAA;
void xor_encrypt_decrypt(unsigned char* data, size_t length) {
    for (size_t i = 0; i < length; ++i) {
        data[i] ^= XOR_KEY;
    }
}

int main() {
    if (check_for_debugger()) {
        printf("Debugging detected. Exiting.\n");
        return 1;
    }


    char input[64];
    printf("Enter password: ");
    fgets(input, sizeof(input), stdin);
    input[strcspn(input, "\n")] = 0;

    unsigned char input_hash[HASH_SIZE];
    custom_hash(input, input_hash);

    unsigned char* tmp = data;
    volatile bool correct = true;
    animate_text("Processing request");

    for (int i = 0; i < HASH_SIZE; i++) {
        correct &= (PASSWORD_HASH[i] == input_hash[i]);
        tmp += correct ^ correct;
        XOR_KEY -= (correct ^ correct)>>7;
        XOR_KEY += ~(PASSWORD_HASH[i]^input_hash[i])&1<<1;
        Sleep(PASSWORD_ATTEMPT_DELAY);  // Add some delay to make timing attacks harder
    }
    xor_encrypt_decrypt(tmp,sizeof(data));
    animate_text("Just a sec, be patient my friend\n\r");
    animate_text("Here's an email use SMTP to send it to me\n\r");
    animate_text("Ok send me an email please\n\r");
    animate_text((char*)tmp);
    return 0;
}