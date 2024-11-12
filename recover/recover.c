#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // If your program is not executed with exactly one command-line argument,
    //  it should remind the user of correct usage, and main should return 1.
    //  Accept a single command-line argument

    if (argc != 2)
    {
        printf("This program only takes one argument, the file we're searching.\n");
        return 1;
    }

    // Open the memory card
    // If the forensic image cannot be opened for reading, your program should inform the user as
    // much, and main should return 1.

    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Cannot open file.\n");
        return 1;
    }

    // Create a buffer for a block of data
    uint8_t buffer[512];
    int counter = 0;
    char filename[8];
    FILE *img = NULL;

    // While there's still data left to read from the memory card
    while (fread(buffer, 1, 512, card) == 512)
    {
        // Create JPEGs from the data

        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            if (img == NULL)
            {
                sprintf(filename, "%03i.jpg", counter);
                img = fopen(filename, "w");
                fwrite(buffer, 1, 512, img);
                counter++;
            }
            else
            {
                fclose(img);
                sprintf(filename, "%03i.jpg", counter);
                img = fopen(filename, "w");
                fwrite(buffer, 1, 512, img);
                counter++;
            }
            // The files you generate should each be named ###.jpg,
            // where ### is a three-digit decimal number, starting with 000 for the first image and
            // counting up.
        }
        else if (img != NULL)
        {
            fwrite(buffer, 1, 512, img);
        }
    }

    fclose(img);
    fclose(card);
}
