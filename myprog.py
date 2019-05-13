#!/usr/bin/env python

# compared to a program written in C the python version would run slower since it needs to call about C functions in order to execute commands

from __future__ import division
import sys
import argparse
import collections
from operator import itemgetter
import string
import re
import time
from nltk.util import ngrams
import pandas as pd


def main():

    # creats timer to time the execution time of the program
    start_time = time.time()

    # parser to take arguments given in command line as variables and be able to accept files as input
    parser=argparse.ArgumentParser(
    description='''Help page for myprog: ''')
    parser.add_argument('-help', action='store_true', help='Show the help screen.')
    parser.add_argument('-ngram', type=int, help='Determine histogram number.')
    parser.add_argument('-pattern', type=str, help='Determine a keyword to look for.')
    parser.add_argument('file', type=argparse.FileType('r'), nargs='+', help='Files to be opened for histogram.')
    args=parser.parse_args()

    # output the help screen if user enters in -help
    if args.help:
        parser.print_help()
        exit(0)

    # assign variables from paraser and those needed for counting
    x = args.ngram
    y = args.pattern
    newy = y.lower()
    directories = []
    z = 0
    array = []
    cumulative = 0
    my_list = list()

    # open files then adds each word to an array then resets the file pointer to get the file count
    for f in args.file:
        for line in f:
            line = line.strip('\n')
            fopen = open(line)
            for line in fopen:
                line = line.lower()
                line = line.translate(None, string.punctuation)
                for w in line.split():
                    array.append(w)
            fopen.close()
        f.seek(0)
                
    # create histogram list and then use counter to get the frequency of each pairing 
    output = list(ngrams(array, x))
    result = collections.Counter(output)

    # total number of histograms for use in percentage 
    total = sum(result.values())

    # check through each file given and count if the word given is in each file
    for f in args.file:
        for line in f:
            line = line.strip('\n')
            fopen = open(line)
            for line in fopen:
                if newy in line.lower():
                    z += 1

    # for loop that will combine the data from the histograms and find the percentage of each apperance
    # the loop will then add each of the histograms found when compared to the given word and output to a list
    print ("")
    print ("A total of %d file(s) contained the word %s." % (z, y))    
    print ("")
    for letter, count in result.most_common():
        letter = [s.translate(None, string.punctuation) for s in letter]
        number = count / total * 100
        cumulative += number
        if any(newy in s for s in letter):
            number = round(number,4)
            cumulative = round(cumulative,4)
            my_list.append([' '.join(letter), count, number, cumulative])

    # set up DataFrame that will act as the table to hold the given information and output in the desired format
    df = pd.DataFrame(data=my_list, columns=['Trigram', 'No.', 'Percentage', 'Cumulative'])
    df['Percentage'] = df['Percentage'].astype(str) + '%'
    df['Cumulative'] = df['Cumulative'].astype(str) + '%'
    df.set_index('Trigram', inplace=True)
    print (df)

    # print out execution time
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__": 
    main()