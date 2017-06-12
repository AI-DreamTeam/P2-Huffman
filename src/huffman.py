# ('C', freq, bin)

import collections
import subprocess as sp
from operator import itemgetter;

class Huffman:
    def __init__(self):
        #Message to be coded
        self.originalMessage = ''

        #Three-tuple for the freqTable. (Char char, Int freq, String code)
        self.freqTable = list();

        #List representing the Huffman codes tree. Each Node is a four-tuple:
        #Node (Char char, Int freq, Node left, Node right)
        self.node_list = list();

    #Method that makes the required magic for Huffman coding
    def startHuffmanCoding (self):
        tmp = sp.call ('clear', shell=True)

        letters = collections.Counter (self.originalMessage);

        #Creates the initial list with a node for each letter in the text
        for letter in letters.most_common ():
            print ("%s : %s" % (letter[0] , letter[1]))
            node = Huffman.create_node (letter[0], letter[1], None, None);
            Huffman.add_to_list (self.node_list, node);

        #Creates the Huffman codes tree from the node list
        while (len (self.node_list) > 1):
            a = self.node_list.pop ();
            b = self.node_list.pop ();
            #Creates a new node with [frequency = sum of two lowest nodes in the list]
            #and sets its leave nodes to the [two lowest nodes in the list]
            node = Huffman.create_node (None, a[1] + b[1], b, a);
            Huffman.add_to_list (self.node_list, node);

        print('Final tree:')
        print (self.node_list[0])
        print('\n\n')

        #List where the 0's or 1's of the code are stored while traversing the tree
        codeArray = list();

        #Gets the code for each letter in the text to be compressed by traversing the tree
        for letter in letters.most_common ():

            codeFound = Huffman.getCode(letter[0], self.node_list[0], False, codeArray)

            if codeFound:
                self.addToFreqTable(codeArray, letter)
                codeArray.clear()

        self.printFreqTable()

    #Recursive method which traverses the tree until it finds the Huffman code for
    #the [letter] parameter and stores it in [codeArray]
    def getCode(letter, currentNode, isCodeFound, codeArray):
        if currentNode[0] == letter:
            isCodeFound = True
            return isCodeFound

        elif Huffman.hasLeaves(currentNode):
            if Huffman.hasLeftNode(currentNode):
                codeArray.append('0')
                isCodeFound = Huffman.getCode(letter, Huffman.getLeftNode(currentNode), isCodeFound, codeArray)

            if Huffman.hasRightNode(currentNode) and not isCodeFound:
                codeArray.append('1')
                isCodeFound = Huffman.getCode(letter, Huffman.getRightNode(currentNode), isCodeFound, codeArray)

        if not isCodeFound:
            if len(codeArray) > 0:
                codeArray.pop()

        return isCodeFound

    def getLeftNode(currentNode):
        return currentNode[2]

    def getRightNode(currentNode):
        return currentNode[3]

    def hasLeftNode(currentNode):
        return currentNode[2] != None

    def hasRightNode(currentNode):
        return currentNode[3] != None

    def hasLeaves(currentNode):
        return currentNode[2] != None or currentNode[3] != None

    def addToFreqTable(self, codeArray, letter):
        codeStr = ''
        for number in codeArray:
            codeStr += number

        newTup = (letter[0], letter[1], codeStr);

        self.freqTable.append(newTup)

    def printFreqTable(self):
        print('Frequency table:\n\n')
        print('---------------------------------------------------')
        print('Character\tFrequency\tCode')

        for element in self.freqTable:
            print('   ' + element[0] + '     \t' + '   ' + str(element[1]) + '     \t' + element[2])

        print('---------------------------------------------------')

    def create_node (string, freq, a, b):
          return (string, freq, a, b);

    def add_to_list (node_list, node):
          node_list.append (node);
          node_list.sort (key=itemgetter (1), reverse=True)

    #Used for sorting the list
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
