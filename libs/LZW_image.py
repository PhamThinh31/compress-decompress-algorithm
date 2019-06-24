import os
import shutil
from typing import Dict

import numpy as np


class LZW_image(object):
    def Compress(uncompressed):
        # Build the dictionary.
        dict_size = 256
        dictionary: Dict[str, int] = dict((str(i), i) for i in range(dict_size))

        w = ''
        result = []
        wc = ''
        for c in uncompressed:
            wc = str(w) + ' ' + str(c)
            wc = wc.strip()
            w = str(w)
            if wc in dictionary:
                w = wc
            else:
                if w is "":
                    continue
                result.append(dictionary[w])
                # Add wc to the dictionary.
                dictionary[wc] = dict_size
                dict_size += 1
                w = c

        # Output the code for w.
        if w:
            w = str(w)
            result.append(dictionary[w])
        return result

    def Decompress(compressed):
        """Decompress a list of output ks to a string."""
        dict_size = 256
        dictionary = dict((i, str(i)) for i in range(dict_size))
        result = []
        w = compressed[0]
        compressed.pop(0)
        result.append(w)
        for k in compressed:
            if k in dictionary:
                entry = dictionary[k]
            elif k == dict_size:
                if type(w) is int:
                    entry = str(w) + ' ' + str(w)
                else:
                    m = w.split()
                    entry = w + ' ' + m[0]
            else:
                raise ValueError('Bad compressed k: %s' % k)
            result.append(entry)
            a = entry.split()
            b = str(w) + ' ' + str(a[0])
            dictionary[dict_size] = b
            dict_size += 1

            w = entry
        return result

    def Sum_bit(arayyy):
        sum = 0
        for i in arayyy:
            i = int(i)
            sum += i.bit_length()
        return sum

    def Write_to_file(array_pixel, filename):
        # filename
        if os.path.exists(filename) is True:
            shutil.rmtree(filename)
        else:
            os.mkdir(filename)
            print("Successfully created the directory %s " % filename)
        dem = 0
        for x in array_pixel:
            fm = filename + "/e" + str(dem)
            dem += 1
            f = open(fm, "wb")
            lenbit = np.ceil(x.bit_length() / 8)
            # print(lenbit)
            a = x.to_bytes(int(lenbit), byteorder='big')
            f.write(a)
            f.close()

    def Decode_from_file(filename):
        if os.path.exists(filename) is False:
            print("Khong ton tai file")
        result = []
        number_file_train = len(os.listdir(filename))
        for i in range(0, number_file_train):
            fm = filename + "\e" + str(i)
            o = open(fm, 'rb')
            encode = o.read()
            m = int.from_bytes(encode, byteorder='big')
            result.append(m)
        return result

# a = compress_LWZ(thinh)
# print(len(b))
# print(len(c))
# c = decompress_LWZ(a)
# k = c.split()

# print(len(data))
# print(len(thinh))
# print(dem)
# for i in range(0, len(data)):
#    if data[i] is ')' or data[i] is '(':
#        data[i] = 0
#    data2.append(np.uint8(data[i]))

# temp1 = np.asarray(data)
# temp1 = temp1.reshape(img.shape[0], img.shape[1])
# print((type(temp1)))
# cv.imshow('DECOMPRESSSSSS', temp1)
# cv.waitKey(0)
# cv.destroyAllWindows()
