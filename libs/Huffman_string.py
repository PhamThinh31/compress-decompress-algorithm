class NodeTree(object):
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return (self.left, self.right)

    def L(self):
        return (self.left)

    def R(self):
        return (self.right)

    def nodes(self):
        return (self.left, self.right)

    def __str__(self):
        return "%s_%s" % (self.left, self.right)


def CodeTree(node, left=True, binString=''):
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(CodeTree(l, True, binString + "0"))
    d.update(CodeTree(r, False, binString + "1"))
    return d


class HM_String(object):

    def __int__(self):
        pass

    def Decode_string(node, encodetext):
        encode = ''
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
            if type(node) is str:
                encode += node
                code = ''
        return encode

    def Coding_string(string):
        freq = {}
        for c in string:
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

    def Encode_string(string, HMcode):
        s = ""
        for i in string:
            s += HMcode[i]
        return s
