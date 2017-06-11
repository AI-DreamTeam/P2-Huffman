# ('C', freq, bin)

import collections
from operator import itemgetter;

class Huffman:
    def __init__(self):
        #Message to be coded (when user chooses to code a string)
        self.originalMessage = ''

        #Three-value tuple for the freqTable. (Char char, Int freq, String code)
        self.freqTable = ();

        #List representing the Huffman codes tree
        self.node_list = list();

    def getFrequency (self):
        letters = collections.Counter (self.originalMessage);

        for letter in letters.most_common ():
            print ("%s : %s" % (letter[0] , letter[1]))
            node = Huffman.create_node (letter[0], letter[1], None, None);
            Huffman.add_to_list (self.node_list, node);

        while (len (self.node_list) > 1):
            a = self.node_list.pop ();
            b = self.node_list.pop ();

            node = Huffman.create_node (None, a[1] + b[1], b, a);
            Huffman.add_to_list (self.node_list, node);

        print (self.node_list[0])

    def create_node (string, freq, a, b):
          return (string, freq, a, b);

    def add_to_list (node_list, node):
          node_list.append (node);
          node_list.sort (key=itemgetter (1), reverse=True)

    def letter_cmp (a, b):
        if a[1] > b[1]:
            return -1
        elif a[1] == b[1]:
            if a[0] > b[0]:
                return 1
            else:
                return -1
        else:
            return 1

    #Node (Char char, Int freq, Node left, Node right)
