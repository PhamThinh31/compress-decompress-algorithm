# Compress Decompress 
Build by **JetBrains PyCharm Community Edition 2019.1.1**

Python 3:

    numpy 1.16.3
    opencv-python 4.1.0.25
    prettytable 0.7.2
    matplotlib 3.0.3

### Algorithm use in this project and Reference

**[Huffman Coding][1]**

**[Run Length Coding][2]**

**[LZW Algorithm][3]**


[1]: http://pythonfiddle.com/huffman-coding-text/ "Huffman code" 

[2]: https://www.rosettacode.org/wiki/Run-length_encoding#Python "RLC"

[3]: https://rosettacode.org/wiki/LZW_compression#Python "LZW"

### Original Ideas

From naive idea compress character -> compress gray image -> compress RBG image
I want to save exactly compress file size follow original algorithm.

Algorithm LZW has not resolved is write to file. I want to save exactly file size so my proposal is save 1 file for 1 element LWZ.Consequently, LWZ will take more time because save all file.
If you have a better way, please let me know.


Example input:
![Input image](/image/tiger.bmp)

Output RBG:
![OutputRGB](/captions/tiger-color.png)

Output GRAY:
![OutputGray](/captions/tiger1.png)
