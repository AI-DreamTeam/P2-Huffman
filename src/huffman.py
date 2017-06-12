# ('C', freq, bin)

import collections
import subprocess as sp
import sys
from operator import itemgetter;

class Huffman:
    def __init__(self):
        #Message to be coded
        self.originalMessage = ''

        #Message coded after traversing the tree
        self.codedMessage = ''

        #Efficiency for the compression of the text
        self.efficiencyLevel = 0.0

        #Three-tuple for the freqTable. (Char char, Int freq, String code)
        self.freqTable = list();

        #Dictionary for fast access to the Huffman code of each letter
        # dict = {'letter' : 'HuffmanCode'}
        self.letterDictionary = dict()

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

        print('Letter Dictionary:')
        print(self.letterDictionary)

        self.generateCodedMessage()

        print('\n\nCoded message:')
        print(self.codedMessage)

        self.calculateEfficiencyLevel()

        print('Efficiency level:')
        print(str(self.efficiencyLevel))

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

        #Adds the tuple to the freqTable
        self.freqTable.append(newTup)

        #Adds the letter and its code to the fast access Dictionary
        self.letterDictionary[letter[0]] = codeStr

    def generateCodedMessage(self):
        for letter in self.originalMessage:
            codeForLetter = self.letterDictionary[letter]
            self.codedMessage += codeForLetter

    def calculateEfficiencyLevel(self):
        #We take each char in the originalMessage as 1 byte in storage
        #and we convert it to bits
        textByteSize = len(self.originalMessage) * 8
        print('Size of the originalMessage: ' + str(textByteSize))

        codedMessageByteSize = len(self.codedMessage)
        print('Size of the codedMessage: ' + str(codedMessageByteSize))

        self.efficiencyLevel = (codedMessageByteSize / textByteSize)

    def printFreqTable(self):
        result = '<b>Character\t\tFrequency\t\tCode</b>\n'

        for element in self.freqTable:
            result += ('   <b>' + element[0] + '</b>\t\t\t\t' + str(element[1]) + '\t\t\t\t' + element[2] + "\n")
        return result;

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
