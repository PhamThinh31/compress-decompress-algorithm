import os
import time

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from Compress_Decompress.libs.Huffman_image import HM_image
from Compress_Decompress.libs.Huffman_string import HM_String
from Compress_Decompress.libs.LZW_image import LZW_image
from Compress_Decompress.libs.LZW_string import LZW_string
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from prettytable import PrettyTable


def HM_Gray_C(path):
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
    print("Number of bits required to represent the data after compression by Huffman coding:", summ)
    ratio = (input_bits / summ)
    print("Compression ratio: ", ratio)
    print("WRITE DATA TO FILE")
    filename = HM_image.filename_from_path(path)
    filename_compress = os.getcwd() + '/compressed_file_HM/compressed_file_' + filename
    HM_image.Write_to_file(list_data_of_img, huffmancode, filename_compress)
    print("DONE HUFFMAN COMPRESSS")
    end_time = time.time()
    time_es = (end_time - start_time)
    return time_es, ratio, treeHM, height, width, filename_compress


def HM_Gray_D(root, H, W, filename):
    S_T = time.time()
    encode = HM_image.Decode_from_file(filename)
    image_1 = HM_image.Decode_Image(root, encode)
    temp = np.asarray(image_1)
    image_2 = temp.reshape(H, W)
    E_T = time.time()
    print("DONE HUFFMAN DECOMPRESSS\n\n\n")
    time_elapsed = (E_T - S_T)
    return time_elapsed


def HM_Color_C(path):
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
    print("Number of bits required to represent the data after compression by Huffman coding:", summ)
    ratio = (input_bits / summ)
    print("Compression ratio: ", ratio)
    # Write_to_file(xg, h, 'texttttt')
    filename = HM_image.filename_from_path(path)
    filename_compress = os.getcwd() + '/compressed_file_HM/compressed_file_' + filename
    HM_image.Write_to_file(xb, HMcode_B, filename_compress + '_B')
    HM_image.Write_to_file(xg, HMcode_G, filename_compress + '_G')
    HM_image.Write_to_file(xr, HMcode_R, filename_compress + '_R')
    E_T = time.time()
    time_elapsed = (E_T - S_T)
    print("DONE COMPRESSS\n\n\n")
    return time_elapsed, ratio, Treenode_B, Treenode_G, Treenode_R, height, width, filename_compress


def HM_Color_D(rootB, rootG, rootR, H, W, filepath):
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
    if len(data_of_B) <size:
        while(len(data_of_B)!=size):
            data_of_B.append(0)
    else:
        data_of_B= data_of_B[0:size]

    if len(data_of_R) <size:
        while(len(data_of_R)!=size):
            data_of_R.append(0)
    else:
        data_of_R= data_of_R[0:size]

    if len(data_of_G) <size:
        while(len(data_of_G)!=size):
            data_of_G.append(0)
    else:
        data_of_G= data_of_G[0:size]
    temp1 = np.asarray(data_of_B)
    temp2 = np.asarray(data_of_G)
    temp3 = np.asarray(data_of_R)
    size = H*W
    if len(temp1) <size:
        while(len(temp1)!=size):
            temp1
    img_B = temp1.reshape(H, W)
    img_G = temp2.reshape(H, W)
    img_R = temp3.reshape(H, W)
    img = cv.merge((img_B, img_G, img_R))

    E_T = time.time()
    time_elapsed = (E_T - S_T)
    print("DONEEEEEEEEE\n\n\n")

    return time_elapsed
############################################
# #LZW


def LWZ_Gray_C(path):
    img = cv.imread(path, cv.IMREAD_GRAYSCALE)
    list_data_of_img = np.array(img.ravel())
    S_T = time.time()
    compress = LZW_image.Compress(list_data_of_img)
    height = img.shape[0]
    width = img.shape[1]
    input_bits = width * height * 8
    summ = LZW_image.Sum_bit(compress)
    print("Number of bits required to represent the data before compression:", input_bits)
    print("Number of bits required to represent the data after compression by LZW:", summ)
    # print("P/s: One number of LWZ array represent by %d to optimal compression ratio." % len_bit)
    ratio = (input_bits / summ)
    print("Compression ratio: ", ratio)
    print("WRITE DATA TO FILE")
    filename = HM_image.filename_from_path(path)
    filename_compress = os.getcwd() + '\compressed_file_LZW\\' + filename
    LZW_image.Write_to_file(compress, filename_compress)
    print("DONE LZW COMPRESSS\n\n\n")
    E_T = time.time()
    time_elapsed = (E_T - S_T)
    return time_elapsed, ratio, height, width, filename_compress


def LWZ_Gray_D(height, width, filename):
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
    time_elapsed = (E_T - S_T)
    return time_elapsed


def LWZ_Color_C(path):
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
    print("Number of bits required to represent the data after compression by LZW:", summ)
    ratio = (input_bits / summ)
    print("Compression ratio: ", ratio)
    print("WRITE DATA TO FILE")
    filename = HM_image.filename_from_path(path)
    filename_compress = os.getcwd() + '\compressed_file_LZW\\' + filename
    LZW_image.Write_to_file(b_compress, filename_compress+"_B")
    LZW_image.Write_to_file(g_compress, filename_compress + "_G")
    LZW_image.Write_to_file(r_compress, filename_compress + "_R")
    E_T = time.time()
    time_elapsed = (E_T - S_T)
    print("DONE LZW COMPRESSS\n\n\n")
    return time_elapsed, ratio, height, width, filename_compress


def LWZ_Color_D(height, width, filename):
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
    time_elapsed = (E_T - S_T)
    print("DONEEEEEEEEE\n\n\n")
    return time_elapsed
def show_2cowl(bars,colorr,nametitle,x):
    plt.figure(x)
    rc('font', weight='bold')
    names = ['Huffman', 'LZW']
    barWidth = 0.5
    r = [0, 1]
    plt.bar(r, bars, color=colorr, edgecolor='white', width=barWidth)
    plt.xticks(r, names, fontweight='bold')
    plt.title(nametitle)

def show_time(bar,x):
    # y-axis in bold
    plt.figure(x)
    rc('font', weight='bold')

    # Values of each group
    bars1 = bar[0]
    bars2 = bar[1]
    # Heights of bars1 + bars2
    bars = np.add(bars1, bars2).tolist()

    # The position of the bars on the x-axis
    r = [0, 1]

    # Names of group and bar width
    names = ['Huffman', 'LZW']
    barWidth = 0.5

    # Create brown bars
    plt.bar(r, bars1, color='#0000ff', edgecolor='white', width=barWidth,label='Time Compress')
    # Create green bars (middle), on top of the firs ones
    plt.bar(r, bars2, bottom=bars1, color='#ff0080', edgecolor='white', width=barWidth,label='Time Decompress')

    plt.ylabel("s",fontweight='bold')
    plt.xticks(r, names, fontweight='bold')
    plt.title("Execution Time")
    plt.legend()
def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size
def get_size_HM(path,x):
    if x is True:
        return os.path.getsize(path)
    if x is False:
        return os.path.getsize(path+'_B')+os.path.getsize(path+'_R')+os.path.getsize(path+'_G')
def get_size_LZW(path,x):
    if x is True:
        return get_size(path)
    if x is False:
        return get_size(path+'_B')+get_size(path+'_R')+get_size(path+'_G')
def imageCompare():
    print("Choose Gray or Color?")
    string = str(input(
        "1. Type 'G' for GRAY IMAGE.\n2.Type 'C' for COLOR IMAGE.\n=> "))
    print("input file path:")
    path = input()
    if string is 'G' or string is 'g':
        print("Choose GRAY")
        print("HUFFMAN CODING")
        time_HM_C, ratio_HM, root, H, W, filename = HM_Gray_C(path)
        time_HM_D = HM_Gray_D(root, H, W, filename)
        print("LZW")
        time_LZW_C, ratio_LZW, H, W, file = LWZ_Gray_C(path)
        time_LZW_D= LWZ_Gray_D(H, W, file)
        size_HM = get_size_HM(filename,True)
        size_LZW = get_size_LZW(file,True)
        print("HM",filename,"LZW",file)
    elif string is 'C' or string is 'c':
        print("Choose Color")
        print("HUFFMAN CODING")
        time_HM_C, ratio_HM, rB, rG, rR, H, W, File_name = HM_Color_C(path)
        time_HM_D = HM_Color_D(rB, rG, rR, H, W, File_name)
        print("LZW")
        time_LZW_C, ratio_LZW, H, W, File = LWZ_Color_C(path)
        time_LZW_D = LWZ_Color_D(H, W, File)
        size_HM = get_size_HM(File_name,False)
        size_LZW = get_size_LZW(File,False)
        print("HM",File_name,"LZW",File)
    else:
        print("ERORR")
    ratio_list = [ratio_HM,ratio_LZW]
    size_list = [size_HM,size_LZW]
    bars = bar2 = [[time_HM_C,time_LZW_C],[time_HM_D,time_LZW_D]]
    sum_HM = time_HM_C+time_HM_D
    sum_LZW = time_LZW_D+time_LZW_C
    data = [
        [ratio_HM, time_HM_C,time_HM_D,size_HM,sum_HM],
        [ratio_LZW, time_LZW_C, time_LZW_D,size_LZW,sum_LZW]]
    x = PrettyTable()
    x.field_names = ['Algorithms', 'Ratio', 'Time Compress(s)', 'Time Decompress(s)', 'Size on Disk(Mb)',
                     'TOTAL TIME(s)']
    x.add_row(['Huffman', ratio_HM, time_HM_C,time_HM_D,size_HM,sum_HM])
    x.add_row(['LZW', ratio_LZW, time_LZW_C, time_LZW_D,size_LZW,sum_LZW])
    print(x)
    show_2cowl(ratio_list,"#1205c6","Compress Ratio",1)
    show_2cowl(size_list, "#02e89b","Size on disk",2)
    show_time(bars,3)
    plt.show()