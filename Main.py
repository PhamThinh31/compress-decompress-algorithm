import os
import time

import cv2 as cv
import numpy as np

from Compress_Decompress.libs.Huffman_image import HM_image
from Compress_Decompress.libs.Huffman_string import HM_String
from Compress_Decompress.libs.LZW_image import LZW_image
from Compress_Decompress.libs.LZW_string import LZW_string
from Compress_Decompress.libs.RLC_image import RLC_image
from Compress_Decompress.libs.RLC_string import RLC_string
from Compress_Decompress.libs.Compare import imageCompare


def user_choice_main():
    print("****************************")
    print(" COMPRESSION & DECOMPRESSION")
    print("****************************")
    string = str(input(
        "1. Type 'H' for HUFFMAN compression.\n2.Type 'L' for LZW compression.\n3.Type 'R' for Run-Length-Coding algorithms.\n4.Type 'C' for compare two algorithms\n=> "))
    if string is 'H' or string is 'h':
        return 1
    elif string is 'L' or string is 'l':
        return 2
    elif string is 'R' or string is 'r':
        return 3
    elif string is 'C' or string is 'c':
        return 4
    else:
        return -1


def user_choice_RLC():
    print("*******************************")
    print(" Run-Length-Coding COMPRESSION ")
    print("*******************************")
    string = str(input("1. Type 'D' for data compression.\n2.Type 'I' for image compression.\n=> "))
    if string is 'D' or string is 'd':
        return 1
    elif string is 'I' or string is 'i':
        return 2
    else:
        return -1


def user_choice_huffman():
    print("*********************")
    print(" HUFFMAN COMPRESSION ")
    print("*********************")
    string = str(input("1. Type 'D' for data compression.\n2.Type 'I' for image compression.\n=> "))
    if string is 'D' or string is 'd':
        return 1
    elif string is 'I' or string is 'i':
        return 2
    else:
        return -1


def user_choice_lzw():
    print("*********************")
    print("   LZW COMPRESSION   ")
    print("*********************")
    string = str(input("1. Type 'D' for data compression.\n2.Type 'I' for image compression.\n=> "))
    if string is 'D' or string is 'd':
        return 1
    elif string is 'I' or string is 'i':
        return 2
    else:
        return -1


def HM_compress_for_string(string):
    freq, h_code, root_tree = HM_String.Coding_string(string)
    print(" Char | Freq  | Huffman code ")
    print("-----------------------------")
    for char, frequency in freq:
        print(" %4s | %5d | %12s" % (char, frequency, h_code[char]))
    sum_bit_compressed = HM_String.Sum_Bit(freq, h_code)
    input_string_len_bit = len(string) * 8
    # encoded of string
    encoded = HM_String.Encode_string(string, h_code)
    # decoded string
    decoded = HM_String.Decode_string(root_tree, encoded)

    print("Huffman code: %s" % encoded)
    print("Number of bits required to represent the data before compression:", input_string_len_bit)
    print("Number of bits required to represent the data after compression:", sum_bit_compressed)
    print("Compression ratio: ", (input_string_len_bit / sum_bit_compressed))
    print("String after decompress: %s" % decoded)
    print("DONE COMPRESSS\n\n\n")


def HM_compress_for_GRAY_image(path):
    img = cv.imread(path, cv.IMREAD_GRAYSCALE)
    list_data_of_img = list(img.ravel())
    start_time = time.time()
    # Histogram
    freq, huffmancode, treeHM = HM_image.Coding(list_data_of_img)
    height = img.shape[0]
    width = img.shape[1]
    input_bits = width * height * 8
    summ = HM_image.Sum_Bit(freq, huffmancode)
    print("Number of bits required to represent the data before compression:", input_bits)
    print("Number of bits required to represent the data after compression:", summ)
    ratio = (input_bits / summ)
    print("Compression ratio: ", ratio)
    print("WRITE DATA TO FILE")
    filename = HM_image.filename_from_path(path)
    print("File compress will save at folder .\compress_file_HM\\%s" % filename)
    filename_compress = os.getcwd() + '/compressed_file_HM/compressed_file_' + filename
    HM_image.Write_to_file(list_data_of_img, huffmancode, filename_compress)
    print("DONE COMPRESSS")
    end_time = time.time()
    time_es = (end_time - start_time) * 1000
    return time_es, ratio, treeHM, height, width, filename_compress


def Huffman_GRAY_image_decompress(root, H, W, filename):
    S_T = time.time()

    encode = HM_image.Decode_from_file(filename)
    image_1 = HM_image.Decode_Image(root, encode)
    size = H * W
    if len(image_1) < size:
        while (len(image_1) != size):
            image_1.append(0)
    else:
        image_1 = image_1[0:size]
    temp = np.asarray(image_1)
    image_2 = temp.reshape(H, W)
    E_T = time.time()
    cv.imshow('DECOMPRESS FROM HUFFMAN DECODE', image_2)
    k = cv.waitKey(0)
    if k == 27:  # wait for ESC key to exit
        cv.destroyAllWindows()
    print("DONE DECOMPRESSS\n\n\n")
    time_elapsed = (E_T - S_T) * 1000
    return time_elapsed


def Huffman_COLOR_image_compress(path):
    img = cv.imread(path, cv.IMREAD_COLOR)
    S_T = time.time()
    b, g, r = cv.split(img)

    xb = list(b.ravel())
    xg = list(g.ravel())
    xr = list(r.ravel())

    # hist = np.bincount(im.ravel(), minlength=256)
    freq_B, HMcode_B, Treenode_B = HM_image.Coding(xb)
    freq_G, HMcode_G, Treenode_G = HM_image.Coding(xg)
    freq_R, HMcode_R, Treenode_R = HM_image.Coding(xr)
    height = img.shape[0]
    width = img.shape[1]
    input_bits = img.shape[0] * img.shape[1] * 8 * 3

    summ = HM_image.Sum_Bit(freq_B, HMcode_B) + HM_image.Sum_Bit(freq_G, HMcode_G) + HM_image.Sum_Bit(freq_R, HMcode_R)

    print("Number of bits required to represent the data before compression:", input_bits)
    print("Number of bits required to represent the data after compression:", summ)
    ratio = (input_bits / summ)
    print("Compression ratio: ", ratio)
    # Write_to_file(xg, h, 'texttttt')
    filename = HM_image.filename_from_path(path)
    print("\nFile compress will save at folder .\compress_file\\%s" % filename)
    filename_compress = os.getcwd() + '/compressed_file_HM/compressed_file_' + filename
    HM_image.Write_to_file(xb, HMcode_B, filename_compress + '_B')
    HM_image.Write_to_file(xg, HMcode_G, filename_compress + '_G')
    HM_image.Write_to_file(xr, HMcode_R, filename_compress + '_R')
    E_T = time.time()
    time_elapsed = (E_T - S_T) * 1000
    print("DONE COMPRESSS\n\n\n")
    return time_elapsed, ratio, Treenode_B, Treenode_G, Treenode_R, height, width, filename_compress


def Huffman_COLOR_image_decompress(rootB, rootG, rootR, H, W, filepath):
    print("Read file compressed from folder: %s" % filepath)
    if (not os.path.isfile(filepath + "_B")):
        print("Loi khong tim thay file %s" % filepath)
    else:
        print("File hop le")
    S_T = time.time()
    encode_B = HM_image.Decode_from_file(filepath + '_B')
    encode_G = HM_image.Decode_from_file(filepath + '_G')
    encode_R = HM_image.Decode_from_file(filepath + '_R')

    data_of_B = HM_image.Decode_Image(rootB, encode_B)
    data_of_R = HM_image.Decode_Image(rootR, encode_R)
    data_of_G = HM_image.Decode_Image(rootG, encode_G)

    size = H * W
    if len(data_of_B) < size:
        while (len(data_of_B) != size):
            data_of_B.append(0)
    else:
        data_of_B = data_of_B[0:size]

    if len(data_of_R) < size:
        while (len(data_of_R) != size):
            data_of_R.append(0)
    else:
        data_of_R = data_of_R[0:size]

    if len(data_of_G) < size:
        while (len(data_of_G) != size):
            data_of_G.append(0)
    else:
        data_of_G = data_of_G[0:size]
    temp1 = np.asarray(data_of_B)
    temp2 = np.asarray(data_of_G)
    temp3 = np.asarray(data_of_R)

    img_B = temp1.reshape(H, W)
    img_G = temp2.reshape(H, W)
    img_R = temp3.reshape(H, W)
    img = cv.merge((img_B, img_G, img_R))

    E_T = time.time()
    time_elapsed = (E_T - S_T) * 1000
    cv.imshow('DECOMPRESSS BY HUFFMAN DECODE', img)
    k = cv.waitKey(0)
    if k == 27:  # wait for ESC key to exit
        cv.destroyAllWindows()
    print("DONEEEEEEEEE\n\n\n")

    return time_elapsed


def Huffman_compresss():
    option = user_choice_huffman()
    if option is -1:
        print("Chon sai vui long chay lai chuong trinh")
    elif option is 1:
        # string compress by HUFFMAN algorithms
        print("Input string want to compress:")
        string = input()
        HM_compress_for_string(string)
    elif option is 2:
        # image compress by HUFFMAN algorithms
        print("Compress GRAY image or COLOR image (G or C) =")
        nhap = input()
        if nhap is 'G' or nhap is 'g':
            print("choose GRAY")
            print("Input path of file (GRAY IMAGE): ")
            path = input()
            _, _, root, H, W, filename = HM_compress_for_GRAY_image(path)
            print("******DECOMPRESS******")
            _ = Huffman_GRAY_image_decompress(root, H, W, filename)
        else:
            print("Choose COLOR")
            print("Input path of file (COLOR IMAGE): ")
            path = input()
            _, _, rB, rG, rR, H, W, File_name = Huffman_COLOR_image_compress(path)
            print("**DECOMPRESS**")
            _ = Huffman_COLOR_image_decompress(rB, rG, rR, H, W, File_name)


############################################
# #LZW


def lzw_compress_for_string(string):
    compress = LZW_string.compress(string)
    input_string_len_bit = len(string) * 8
    sum_bit_compressed = len(compress) * 8
    decoded = LZW_string.decompress(compress)
    print("LWZ array:", compress)
    print("Number of bits required to represent the data before compression:", input_string_len_bit)
    print("Number of bits required to represent the data after compression:", sum_bit_compressed)
    print("Compression ratio: ", (input_string_len_bit / sum_bit_compressed))
    print("String after decompress: %s" % decoded)
    print("DONE COMPRESSS\n\n\n")


def LWZ_compress_GRAY_image(path):
    img = cv.imread(path, cv.IMREAD_GRAYSCALE)
    list_data_of_img = np.array(img.ravel())
    S_T = time.time()
    compress = LZW_image.Compress(list_data_of_img)
    height = img.shape[0]
    width = img.shape[1]
    input_bits = width * height * 8
    summ = LZW_image.Sum_bit(compress)
    print("20 element of LWZ array:", compress[0:20])
    print("Number of bits required to represent the data before compression:", input_bits)
    print("Number of bits required to represent the data after compression:", summ)
    # print("P/s: One number of LWZ array represent by %d to optimal compression ratio." % len_bit)
    ratio = (input_bits / summ)
    print("Compression ratio: ", ratio)
    print("WRITE DATA TO FILE")
    filename = HM_image.filename_from_path(path)
    print("File compress will save at folder .\compress_file_LZW\\%s" % filename)
    filename_compress = os.getcwd() + '\compressed_file_LZW\\' + filename
    LZW_image.Write_to_file(compress, filename_compress)
    print("DONE COMPRESSS\n\n\n")
    E_T = time.time()
    time_elapsed = (E_T - S_T) * 1000
    return time_elapsed, ratio, height, width, filename_compress


def LZW_decompress_GRAY_image(height, width, filename):
    S_T = time.time()
    o = LZW_image.Decode_from_file(filename)
    # olist=[]
    # for i in range(0,len(o)):
    #     olist.append(o[i])
    image_1 = LZW_image.Decompress(o)
    data = []
    # # dem=0
    for i in image_1:
        if type(i) is int:
            data.append(np.uint8(i))
        else:
            l = i.split()
            for p in l:
                data.append(np.uint8(p))

    temp = np.asarray(data)
    image_2 = temp.reshape(height, width)
    E_T = time.time()
    time_elapsed = (E_T - S_T) * 1000
    cv.imshow('DECOMPRESS FROM LZW ALGORITHM', image_2)

    k = cv.waitKey(0)
    if k == 27:  # wait for ESC key to exit
        cv.destroyAllWindows()
    return time_elapsed


def LWZ_compress_for_COLOR_image(path):
    img = cv.imread(path, cv.IMREAD_COLOR)
    S_T = time.time()
    # list_data_of_img = np.array(img.ravel())
    b, g, r = cv.split(img)

    xb = list(b.ravel())
    xg = list(g.ravel())
    xr = list(r.ravel())
    b_compress = LZW_image.Compress(xb)
    g_compress = LZW_image.Compress(xg)
    r_compress = LZW_image.Compress(xr)

    height = img.shape[0]
    width = img.shape[1]
    input_bits = width * height * 8 * 3
    summ = LZW_image.Sum_bit(b_compress) + LZW_image.Sum_bit(g_compress) + LZW_image.Sum_bit(r_compress)
    print("Number of bits required to represent the data before compression:", input_bits)
    print("Number of bits required to represent the data after compression:", summ)
    ratio = (input_bits / summ)
    print("Compression ratio: ", ratio)
    print("WRITE DATA TO FILE")
    filename = HM_image.filename_from_path(path)
    print("File compress will save at folder .\compress_file_LZW\\%s" % filename)
    filename_compress = os.getcwd() + '\compressed_file_LZW\\' + filename
    LZW_image.Write_to_file(b_compress, filename_compress + "_B")
    LZW_image.Write_to_file(g_compress, filename_compress + "_G")
    LZW_image.Write_to_file(r_compress, filename_compress + "_R")
    E_T = time.time()
    time_elapsed = (E_T - S_T) * 1000
    print("DONE COMPRESSS\n\n\n")
    return time_elapsed, ratio, height, width, filename_compress


def LWZ_decompress_for_COLOR_image(height, width, filename):
    S_T = time.time()
    b_list = LZW_image.Decode_from_file(filename + "_B")
    r_list = LZW_image.Decode_from_file(filename + "_R")
    g_list = LZW_image.Decode_from_file(filename + "_G")

    temp_b = LZW_image.Decompress(b_list)
    temp_r = LZW_image.Decompress(r_list)
    temp_g = LZW_image.Decompress(g_list)
    data_b = []
    data_r = []
    data_g = []
    # # dem=0
    for i in temp_b:
        if type(i) is int:
            data_b.append(np.uint8(i))
        else:
            l = i.split()
            for p in l:
                data_b.append(np.uint8(p))
    # R
    for i in temp_r:
        if type(i) is int:
            data_r.append(np.uint8(i))
        else:
            l = i.split()
            for p in l:
                data_r.append(np.uint8(p))
    # G
    for i in temp_g:
        if type(i) is int:
            data_g.append(np.uint8(i))
        else:
            l = i.split()
            for p in l:
                data_g.append(np.uint8(p))

    temp1 = np.asarray(data_b)
    temp2 = np.asarray(data_g)
    temp3 = np.asarray(data_r)

    img_B = temp1.reshape(height, width)
    img_G = temp2.reshape(height, width)
    img_R = temp3.reshape(height, width)
    img = cv.merge((img_B, img_G, img_R))
    E_T = time.time()
    time_elapsed = (E_T - S_T) * 1000
    cv.imshow('DECOMPRESSS BY LZW ALGORITHM', img)
    k = cv.waitKey(0)
    if k == 27:  # wait for ESC key to exit
        cv.destroyAllWindows()
    print("DONEEEEEEEEE\n\n\n")
    return time_elapsed


def LZW_compress():
    option = user_choice_lzw()
    if option is -1:
        print("Chon sai vui long chay lai chuong trinh")
    elif option is 1:
        # string compress by LZW algorithms
        print("Input string want to compress:")
        string = input()
        lzw_compress_for_string(string)
    elif option is 2:
        # image compress by LWZ algorithms
        print("Compress GRAY image or COLOR image (G or C) =")
        nhap = input()
        if nhap is 'G' or nhap is 'g':
            print("choose GRAY")
            print("Input path of file (GRAY IMAGE): ")
            path = input()
            _, _, H, W, file = LWZ_compress_GRAY_image(path)
            print("******DECOMPRESS******")
            _ = LZW_decompress_GRAY_image(H, W, file)
        else:
            print("Choose COLOR")
            print("Input path of file (COLOR IMAGE): ")
            path = input()
            _, _, H, W, File_name = LWZ_compress_for_COLOR_image(path)
            print("**DECOMPRESS**")
            _ = LWZ_decompress_for_COLOR_image(H, W, File_name)


def RLC_compress_for_string(string):
    compress = RLC_string.encode(string)
    input_string_len_bit = len(string) * 8
    sum_bit_compressed = len(compress[0]) * 2 * 8
    print(compress[0])
    decoded = RLC_string.decode(compress[0])
    print("Number of bits required to represent the data before compression:", input_string_len_bit)
    print("Number of bits required to represent the data after compression:", sum_bit_compressed)
    print("Compression ratio: ", (input_string_len_bit / sum_bit_compressed))
    print("String after decompress: %s" % decoded)
    print("DONE COMPRESSS\n\n\n")


def RLC_compress_GRAY_image(path):
    im = cv.imread(path, cv.IMREAD_GRAYSCALE)
    list_data_of_img = np.array(im.ravel())
    value = RLC_image.encode(list_data_of_img)
    height = im.shape[0]
    width = im.shape[1]
    print("20 element of RLC array:", (value[0][0:20]))
    data = []
    image_1 = RLC_image.decode(value[0])
    for i in image_1:
        data.append(np.uint8(i))

    temp = np.asarray(data)
    image_2 = temp.reshape(height, width)
    cv.imshow('DECOMPRESS FROM RLC ALGORITHM', image_2)

    k = cv.waitKey(0)
    if k == 27:  # wait for ESC key to exit
        cv.destroyAllWindows()


def RLC_compress():
    option = user_choice_RLC()
    if option is -1:
        print("Chon sai vui long chay lai chuong trinh")
    elif option is 1:
        # string compress by LZW algorithms
        print("Input string want to compress:")
        string = input()
        RLC_compress_for_string(string)
    elif option is 2:
        print("Input path of file (GRAY IMAGE): ")
        path = input()
        RLC_compress_GRAY_image(path)
        print("******DECOMPRESS******")



def main():
    while (True):
        option = user_choice_main()
        if option is -1:
            print("Thoat chuong trinh")
            break
        elif option is 1:
            Huffman_compresss()
        elif option is 2:
            LZW_compress()
        elif option is 3:
            RLC_compress()
        elif option is 4:
            imageCompare()


main()
