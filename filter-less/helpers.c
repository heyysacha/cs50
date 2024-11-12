#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int color =
                round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue = color;
            image[i][j].rgbtGreen = color;
            image[i][j].rgbtRed = color;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sephiaRed = round((image[i][j].rgbtBlue * 0.189) + (image[i][j].rgbtGreen * 0.769) +
                                  (image[i][j].rgbtRed * 0.393));
            int sephiaGreen =
                round((image[i][j].rgbtBlue * 0.168) + (image[i][j].rgbtGreen * 0.686) +
                      (image[i][j].rgbtRed * 0.349));
            int sephiaBlue = round((image[i][j].rgbtBlue * 0.131) +
                                   (image[i][j].rgbtGreen * 0.534) + (image[i][j].rgbtRed * 0.272));

            if (sephiaRed > 255)
            {
                sephiaRed = 255;
            }
            if (sephiaBlue > 255)
            {
                sephiaBlue = 255;
            }
            if (sephiaGreen > 255)
            {
                sephiaGreen = 255;
            }
            image[i][j].rgbtBlue = sephiaBlue;
            image[i][j].rgbtGreen = sephiaGreen;
            image[i][j].rgbtRed = sephiaRed;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE temp;
            temp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of image
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int average_red = 0;
            int average_green = 0;
            int average_blue = 0;
            float counter = 0;

            for (int k = -1; k <= 1; k++)
            {
                for (int l = -1; l <= 1; l++)

                    if (i + k < height && i + k >= 0 && j + l < width && j + l >= 0)
                    {
                        average_red += copy[i + k][j + l].rgbtRed;
                        average_green += copy[i + k][j + l].rgbtGreen;
                        average_blue += copy[i + k][j + l].rgbtBlue;
                        counter++;
                    }
            }
            image[i][j].rgbtRed = round((float) average_red / counter);
            image[i][j].rgbtGreen = round((float) average_green / counter);
            image[i][j].rgbtBlue = round((float) average_blue / counter);
            counter = 0;
            average_red = 0;
            average_green = 0;
            average_blue = 0;
        }
    }
    return;
}
