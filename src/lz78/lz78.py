import varint
import csv,os
from datetime import datetime

def lz78_compress(input_text):
    dictionary = {}
    next_code = 0
    compressed = bytearray()
    i = 0
    while i < len(input_text):
        if input_text[i] not in dictionary.values():
            x=0
            compressed.extend(varint.encode(0))
            compressed.extend(input_text[i].encode('utf-8'))
            next_code += 1
            dictionary[next_code] = input_text[i]
        else:
            phrase = input_text[i]
            while phrase in dictionary.values() and i<len(input_text)-1:
                i += 1
                phrase += input_text[i]
            code=0
            for x in dictionary.keys():
                if dictionary[x]==phrase[0:-1]:
                    code=x
                    break
            compressed.extend(varint.encode(code))
            compressed.extend(phrase[-1].encode('utf-8'))
            next_code += 1
            dictionary[next_code] = phrase
        # print(dictionary.get(next_code),next_code)
        i += 1

    return compressed

def lz78_decompress(compressed):
    dictionary = {0: b""}
    next_code = 0
    i = 0
    decompressed_text = ""

    while i < len(compressed):
        code= varint.decode_bytes(compressed[i:])
        consumed=len(varint.encode(code))
        i += consumed
        if code == 0:
            char = chr(varint.decode_bytes(compressed[i:]))
            i += 1
            decompressed_text+=char
            # print(char)
            next_code += 1
            dictionary[next_code] = char

        else:
            phrase = dictionary[code]
            char = chr(varint.decode_bytes(compressed[i:]))
            i += 1

            phrase += char
            decompressed_text+=phrase

            next_code += 1
            dictionary[next_code] = phrase

    return decompressed_text


def main():
    input_file="../../data/data.txt"
    compressed_file="../../results/lz78/lz78_compressed.bin"
    decompressed_file="../../results/lz78/lz78_decompressed.txt"

    start_time=datetime.now()
    with open(input_file, "r", encoding="utf-8") as file:
        input_text = file.read()

    compressed_data = lz78_compress(input_text)
    
    with open(compressed_file, "wb") as file:
        file.write(compressed_data)
    
    end_time=datetime.now()
    compressed_time=(end_time-start_time).microseconds
    compressed_file_size=os.path.getsize(compressed_file)
    data_file_size=os.path.getsize(input_file)

    start_time=datetime.now()
    decompressed_text = lz78_decompress(compressed_data)

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
        if i[0]=="lz78":
            i[1]=compressed_time
            i[2]=decompressed_time
            i[3]=compressed_file_size
            i[4]=data_file_size
            found=1
    if found==0:
        csv_data.append(["lz78",compressed_time,decompressed_time,compressed_file_size,data_file_size])
    with open(csv_file,"w+") as file:
        csv_writer=csv.writer(file)
        csv_writer.writerows(csv_data)
if __name__ == "__main__":
    main()
