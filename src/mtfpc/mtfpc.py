import heapq
from collections import defaultdict
import csv,os
from datetime import datetime

def mtf_encode(data):
    alphabet = list(set(data))
    mtf_list = list(alphabet)

    encoded_data = []
    for symbol in data:
        symbol_index = mtf_list.index(symbol)
        encoded_data.append(symbol_index)
        mtf_list.remove(symbol)
        mtf_list.insert(0,symbol)

    return encoded_data, alphabet

def huffman_encode(data):
    freq_dict = defaultdict(int)
    for symbol in data:
        freq_dict[symbol] += 1
    heap = [[weight, [symbol, ""]] for symbol, weight in freq_dict.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    huffman_dict = dict(heap[0][1:])
    encoded_data = ''.join(huffman_dict[symbol] for symbol in data)

    return encoded_data, huffman_dict

def compress(data):
    mtf_encoded_data, alphabet = mtf_encode(data)
    huffman_encoded_data, huffman_dict = huffman_encode(mtf_encoded_data)

    return huffman_encoded_data, alphabet, huffman_dict

def decompress(encoded_data, alphabet, huffman_dict):
    reversed_huffman_dict = {code: symbol for symbol, code in huffman_dict.items()}
    mtf_encoded_data =[]
    current_code = ""
    for bit in encoded_data:
        current_code += bit
        if current_code in reversed_huffman_dict:
            symbol = reversed_huffman_dict[current_code]
            mtf_encoded_data .append( symbol)
            current_code = ""
    mtf_list = list(alphabet)
    decoded_data = []
    for symbol_index in mtf_encoded_data:
        symbol = mtf_list[symbol_index]
        decoded_data.append(symbol)
        mtf_list.pop(symbol_index)
        mtf_list.insert(0,symbol)

    return ''.join(decoded_data)

def main():
    data_file="../../data/data.txt"
    compressed_file="../../results/mtfpc/compressed_mtfpc.bin"
    decompressed_file="../../results/mtfpc/decompressed_mtfpc.bin"
    
    start_time=datetime.now()
    with open(data_file,"r") as file:
        data=file.read()
    compressed_data_wite, alphabet, huffman_dict = compress(data)
    padded_length = (8 - len(compressed_data_wite) % 8) % 8
    compressed_data_wite += '0' * padded_length
    output_bytes = bytearray([int(compressed_data_wite[i:i+8], 2) for i in range(0, len(compressed_data_wite), 8)])
    with open(compressed_file, 'wb+') as file:
        file.write(bytes([padded_length]))
        file.write(output_bytes)
    end_time=datetime.now()
    compressed_time=(end_time-start_time).microseconds
    compressed_file_size=os.path.getsize(compressed_file)
    data_file_size=os.path.getsize(data_file)

    start_time=datetime.now()
    with open(compressed_file, 'rb') as file:
        padded_length = file.read(1)[0]
        compressed_data_read = ''.join(format(byte, '08b') for byte in file.read())
    compressed_data_read = compressed_data_read[:-padded_length]
    decompressed_data = decompress(compressed_data_read, alphabet, huffman_dict)
    with open(decompressed_file,"w+") as file:
        file.write(decompressed_data)
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
        if i[0]=="mtfpc":
            i[1]=compressed_time
            i[2]=decompressed_time
            i[3]=compressed_file_size
            i[4]=data_file_size
            found=1
    if found==0:
        csv_data.append(["mtfpc",compressed_time,decompressed_time,compressed_file_size,data_file_size])
    with open(csv_file,"w+") as file:
        csv_writer=csv.writer(file)
        csv_writer.writerows(csv_data)
if __name__=="__main__":
    main()
# # Example
# original_data = "abracadabra"
# compressed_data, alphabet, huffman_dict = compress(original_data)

# print("Original Data:", original_data)
# print("Compressed Data:", compressed_data)
# decompressed_data = decompress(compressed_data, alphabet, huffman_dict)
# print("Decompressed Data:", decompressed_data)
