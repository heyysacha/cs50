#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

string cipher(string plaintext, int key);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Error: please input one key.\n");
        return 1;
    }
    else
    {
        for (int i = 0, length = strlen(argv[1]); i < length; i++)
        {
            if (!isdigit(argv[1][i]))
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
        string input = get_string("plaintext:  ");
        int cipher_key = atoi(argv[1]);
        printf("ciphertext: %s\n", cipher(input, cipher_key));
    }
}

string cipher(string plaintext, int key)
{
    while (key > 26)
    {
        key -= 26;
    }
    for (int i = 0; i < strlen(plaintext); i++)
    {
        if (isalpha(plaintext[i]))
        {
            if (isupper(plaintext[i]))
            {
                if (plaintext[i] + key <= 90)
                {
                    plaintext[i] = plaintext[i] + key;
                }
                else
                {
                    plaintext[i] = plaintext[i] + key - 26;
                }
            }
            else
            {
                if (plaintext[i] + key <= 122)
                {
                    plaintext[i] = plaintext[i] + key;
                }
                else
                {
                    plaintext[i] = plaintext[i] + key - 26;
                }
            }
        }
    }
    return plaintext;
}
