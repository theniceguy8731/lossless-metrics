import sys
import varint
import csv,os
from datetime import datetime

def lzw_compress(input_text):
    table = {chr(i): i for i in range(256)}
    next_code = 256
    compressed = bytearray()
    phrase = input_text[0]

    for char in input_text[1:]:
        if phrase + char in table:
            phrase += char
        else:
            compressed.extend(varint.encode(table[phrase]))
            table[phrase + char] = next_code
            next_code += 1
            phrase = char

    compressed.extend(varint.encode(table[phrase]))
    return compressed

def lzw_decompress(compressed):
    table = {i: chr(i) for i in range(256)}
    next_code = 256
    decompressed_text = []

    i = 0
    phrase = table[compressed[i]]
    decompressed_text.append(phrase)
    i += 1

    while i < len(compressed):
        code= varint.decode_bytes(compressed[i:])
        bytes_read=len(varint.encode(code))
        i += bytes_read

        if code in table:
            entry = table[code]
        elif code == next_code:
            entry = phrase + phrase[0]
        else:
            raise ValueError("Invalid compressed code")

        decompressed_text.append(entry)
        table[next_code] = phrase + entry[0]
        next_code += 1
        phrase = entry

    return ''.join(decompressed_text)


def main():
    data_file="../../data/data.txt"
    compressed_file="../../results/lzw/lzw_compressed.bin"
    decompressed_file="../../results/lzw/lzw_decompressed.txt"

    start_time=datetime.now()
    with open(data_file, "r", encoding="utf-8") as file:
        input_text = file.read()

    compressed_data = lzw_compress(input_text)

    with open(compressed_file, "wb") as file:
        file.write(compressed_data)

    end_time=datetime.now()
    compressed_time=(end_time-start_time).microseconds
    compressed_file_size=os.path.getsize(compressed_file)
    data_file_size=os.path.getsize(data_file)

    start_time=datetime.now()
    decompressed_text = lzw_decompress(compressed_data)

    with open(decompressed_file, "w", encoding="utf-8") as file:
        file.write(decompressed_text)
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
        if i[0]=="lzw":
            i[1]=compressed_time
            i[2]=decompressed_time
            i[3]=compressed_file_size
            i[4]=data_file_size
            found=1
    if found==0:
        csv_data.append(["lzw",compressed_time,decompressed_time,compressed_file_size,data_file_size])
    with open(csv_file,"w+") as file:
        csv_writer=csv.writer(file)
        csv_writer.writerows(csv_data)

if __name__ == "__main__":
    main()
