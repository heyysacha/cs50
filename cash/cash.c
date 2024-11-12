#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int change;
    do
    {
        change = get_int("Change: ");
    }
    while (change <= 0);

    int count = 0;

    do
    {
        if (change - 25 >= 0)
        {
            count++;
            change -= 25;
        }
        else if (change - 10 >= 0)
        {
            count++;
            change -= 10;
        }
        else if (change - 5 >= 0)
        {
            count++;
            change -= 5;
        }
        else if (change - 1 >= 0)
        {
            count++;
            change -= 1;
        }
    }
    while (change > 0);

    printf("%i\n", count);
}
