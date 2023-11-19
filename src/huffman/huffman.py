import heapq
from collections import Counter
import csv,os
from datetime import datetime

class HuffmanNode:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

global_huffman_tree = None

def build_huffman_tree(text):
    char_frequency = Counter(text)
    priority_queue = [HuffmanNode(char, freq) for char, freq in char_frequency.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged_node = HuffmanNode(freq=left.freq + right.freq)
        merged_node.left, merged_node.right = left, right
        heapq.heappush(priority_queue, merged_node)

    if priority_queue:
        return priority_queue[0]
    else:
        return None

def build_huffman_codes(node, current_code="", codes=None):
    if codes is None:
        codes = {}

    if node is not None:
        if node.char is not None:
            codes[node.char] = current_code
        build_huffman_codes(node.left, current_code + "0", codes)
        build_huffman_codes(node.right, current_code + "1", codes)

    return codes

def compress_file(input_file, output_file):
    global global_huffman_tree  # Access the global variable
    with open(input_file, 'r', encoding='ascii') as file:
        text = file.read()

    global_huffman_tree = build_huffman_tree(text)
    codes = build_huffman_codes(global_huffman_tree)

    # Create a binary string representing the compressed data
    compressed_data = ''.join(codes[char] for char in text)

    # Padding
    padded_length = (8 - len(compressed_data) % 8) % 8
    compressed_data += '0' * padded_length

    output_bytes = bytearray([int(compressed_data[i:i+8], 2) for i in range(0, len(compressed_data), 8)])

    with open(output_file, 'wb') as file:
        file.write(bytes([padded_length]))
        file.write(output_bytes)

def decompress_file(input_file, output_file):
    global global_huffman_tree  # Access the global variable
    with open(input_file, 'rb') as file:
        padded_length = file.read(1)[0]
        compressed_data = ''.join(format(byte, '08b') for byte in file.read())
    compressed_data = compressed_data[:-padded_length]

    current = global_huffman_tree

    decoded_text = ""
    for bit in compressed_data:
        if current is not None:
            if bit == '0':
                current = current.left
            else:
                current = current.right

            if current is not None and current.char is not None:
                decoded_text += current.char
                current = global_huffman_tree

    with open(output_file, 'w', encoding='ascii') as file:
        file.write(decoded_text)

input_file = "../../data/data.txt"
compressed_file = "../../results/huffman/huffman_compressed.bin"
decompressed_file = "../../results/huffman/huffman_decompressed.txt"

start_time=datetime.now()
# Compress the file
compress_file(input_file, compressed_file)
end_time=datetime.now()
compressed_time=(end_time-start_time).microseconds
compressed_file_size=os.path.getsize(compressed_file)
data_file_size=os.path.getsize(input_file)

# Decompress the file
start_time=datetime.now()
decompress_file(compressed_file, decompressed_file)
end_time=datetime.now()
decompressed_time=(end_time-start_time).microseconds

csv_file="../../results/final-result.csv"
csv_data=[]
with open(csv_file,"r+") as file:
    csv_reader=csv.reader(file)
    for row in csv_reader:
        csv_data.append(row)
found=0
for i in csv_data:
    if i[0]=="huffman":
        i[1]=compressed_time
        i[2]=decompressed_time
        i[3]=compressed_file_size
        i[4]=data_file_size
        found=1
if found==0:
    csv_data.append(["huffman",compressed_time,decompressed_time,compressed_file_size,data_file_size])
with open(csv_file,"w+") as file:
    csv_writer=csv.writer(file)
    csv_writer.writerows(csv_data)