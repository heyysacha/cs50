// Implements a dictionary's functionality
#include <cs50.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 1000;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    node *check = table[hash(word)];

    while (check != NULL)
    {

        if (strcasecmp(word, check->word) == 0)
        {
            return true;
        }
        else
        {
            check = check->next;
        }
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int sum = 0;
    for (int i = 0, length = strlen(word); i < length; i++)
    {
        sum += toupper(word[i]);
    }
    // TODO: Improve this hash function
    return sum % N;
}

// counter for size function
int counter = 0;

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // open the dictionary file
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        return false;
    }

    // make a node for each word/line

    char dict_word[LENGTH + 1];
    while (fscanf(dict, "%s", dict_word) != EOF)
    {
        node *new = malloc(sizeof(node));
        if (new == NULL)
        {
            return false;
        }
        // hash each node value and put it in a hash table
        else
        {
            strcpy(new->word, dict_word);
            // add node to linked list
            // hash to find where to put it
            if (table[hash(new->word)] == NULL)
            {
                // if it's the first one, make it the head of the list
                table[hash(new->word)] = new;
                new->next = NULL;
                counter++;
            }
            else
            {
                // point the next pointer to first item in list
                new->next = table[hash(new->word)];
                // point head to this item
                table[hash(new->word)] = new;
                counter++;
            }
        }
    }
    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    if (counter == 0)
    {
        // TODO
        return 0;
    }
    else
    {
        return counter;
    }
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        if (table[i] != NULL)
        {
            node *temp = table[i];
            node *check = table[i]->next;
            while (check != NULL)
            {
                free(temp);
                temp = check;
                check = check->next;
            }
            free(temp);
        }
    }
    // TODO
    return true;
}
