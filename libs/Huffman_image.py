import numpy as np
from array import *


# define HUFFMAN TREE
class NodeTree(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return (self.left, self.right)

    def nodes(self):
        return (self.left, self.right)

    def __str__(self):
        return "%r_%r" % (self.left, self.right)


def CodeTree(node, left=True, binString=""):
    if type(node) is np.uint8:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(CodeTree(l, True, binString + "0"))
    d.update(CodeTree(r, False, binString + "1"))
    return d


class HM_image(object):
    def __int__(self):
        pass

    def Decode_Image(node, encodetext):
        encode = []
        code = ''
        root = node
        (l, r) = node.children()
        for c in encodetext:
            if (code == ''):
                node = root
            code += c
            (l, r) = node.children()
            if c == '0':
                node = l
            else:
                node = r
            if type(node) is np.uint8:
                encode.append(node)
                code = ''
        return encode

    # define huffman code for each number
    def Coding(array):
        freq = {}
        for c in array:
            if c in freq:
                freq[c] += 1
            else:
                freq[c] = 1

        freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        nodes = freq
        while len(nodes) > 1:
            key1, c1 = nodes[-1]
            key2, c2 = nodes[-2]
            nodes = nodes[:-2]
            node = NodeTree(key1, key2)
            nodes.append((node, c1 + c2))
            # Re-sort the list
            nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
        huffmanCode = CodeTree(nodes[0][0])
        return freq, huffmanCode, nodes[0][0]

    # Number of bit
    def Sum_Bit(freq, HMcode):
        summ = 0
        for char, frequency in freq:
            summ += (len(HMcode[char]) * frequency)
        return summ

    def Write_to_file(array_pixel, HMcode, filename):
        f = open(filename, 'wb')
        encode_string = ""
        for i in array_pixel:
            temp = (HMcode[i])
            encode_string += (str(temp))
        i = 0
        while (i < len(encode_string)):
            bin_array = array('B')

            b = encode_string[i:i + 8]
            bin_array.append(int(b, 2))
            i += 8
            bin_array.tofile(f)
        f.close()

    def Decode_from_file(filename):
        o = open(filename, 'rb')
        encode = o.read()
        o.close()
        bin_array = array('B')
        bin_array.frombytes(encode)
        encode_str = ""
        for i in range(0, len((bin_array))):
            if i is len(bin_array) - 1:
                encode_str += format(bin_array[i], "b")
                break
            len_bit = len(format(bin_array[i], "b"))
            string_bit = format(bin_array[i], "b")
            if len_bit < 8:
                for k in range(0, (8 - len_bit)):
                    encode_str += '0'
                encode_str += string_bit
            else:
                encode_str += string_bit
        return encode_str

        return encode_str

    def filename_from_path(string):
        path = string.split('\\')
        name_file_with_extention = path[len(path) - 1]
        temp = name_file_with_extention.split('.')
        name_file = temp[0]
        return name_file
