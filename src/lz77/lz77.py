import csv,os
from datetime import datetime

def lz77_compress(input_text, window_size=10, buffer_size=10):
    compressed = bytearray()
    index = 0

    while index < len(input_text):
        match_length = 0
        best_match = (0, 0)

        for i in range(1, min(buffer_size + 1, len(input_text) - index + 1)):
            substring = input_text[index:index + i]
            window_index = max(0, index - window_size)
            match_index = input_text.rfind(substring, window_index, index+i-1)
            if match_index != -1 and match_index < index:
                distance = index - match_index
                if distance <= window_size and i > match_length:
                    match_length = i
                    best_match = (distance, match_length)

        if match_length > 0 and index+match_length<len(input_text):
            compressed.append(best_match[0])
            compressed.append(best_match[1])
            compressed.append(ord(input_text[index + match_length]))
            index += match_length+1
        else:
            compressed.append(0)
            compressed.append(0) 
            compressed.append(ord(input_text[index]))
            index += 1
        

    return compressed

def lz77_decompress(compressed):
    decompressed = ""
    index = 0

    while index < len(compressed):
        distance = compressed[index]
        length = compressed[index + 1]
        literal_char = compressed[index + 2]
        if distance > 0:
            start_index = max(0, len(decompressed) - distance)
            for _ in range(length):
                decompressed += decompressed[start_index]
                start_index += 1
            decompressed+=chr(literal_char)
        else:
            decompressed += chr(literal_char)

        index += 3 

    return decompressed


def main():
    with open("../../data/data.txt", "r", encoding="utf-8") as file:
        input_text = file.read()

    compressed_data = lz77_compress(input_text)
    
    with open("../../results/lz77/lz77_compressed.bin", "wb") as file:
        file.write(compressed_data)

    decompressed_text = lz77_decompress(compressed_data)
    
    with open("../../results/lz77/lz77_decompressed.txt", "w", encoding="utf-8") as file:
        file.write(decompressed_text)


if __name__ == "__main__":
    main()


def main():
    input_file="../../data/data.txt"
    compressed_file="../../results/lz77/lz77_compressed.bin"
    decompressed_file="../../results/lz77/lz77_decompressed.txt"

    start_time=datetime.now()
    with open(input_file, "r", encoding="utf-8") as file:
        input_text = file.read()

    compressed_data = lz77_compress(input_text)
    with open(compressed_file, "wb") as file:
        file.write(compressed_data)
    end_time=datetime.now()
    compressed_time=(end_time-start_time).microseconds
    compressed_file_size=os.path.getsize(compressed_file)
    data_file_size=os.path.getsize(input_file)

    start_time=datetime.now()
    decompressed_text = lz77_decompress(compressed_data)
    
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
        if i[0]=="lz77":
            i[1]=compressed_time
            i[2]=decompressed_time
            i[3]=compressed_file_size
            i[4]=data_file_size
            found=1
    if found==0:
        csv_data.append(["lz77",compressed_time,decompressed_time,compressed_file_size,data_file_size])    
    with open(csv_file,"w+") as file:
        csv_writer=csv.writer(file)
        csv_writer.writerows(csv_data)
    
if __name__ == "__main__":
    main()
