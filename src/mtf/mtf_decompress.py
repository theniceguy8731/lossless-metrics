import varint
import csv,os
from datetime import datetime

def search(list_symbols,index):
    return list_symbols[index]
        

def move_front(index,list_symbols):
    character=list_symbols.pop(index)
    list_symbols.insert(0,character)

def mtf_decode(compressed_data,list_symbols,decompressed_list):
    for index in compressed_data:
        symbol=search(list_symbols,index)
        decompressed_list.append(symbol)
        move_front(index,list_symbols)


def main():
    compressed_file="../../results/mtf/compressed_mtf.bin"
    decompressed_file="../../results/mtf/decompressed_mtf.txt"
    start_time=datetime.now() 
    list_symbol= list()
    for i in range(128):
        list_symbol.append(chr(i))
    with open(compressed_file,"rb") as file:
        encoded_data=file.read()
    i=0
    compressed_data=[]
    while(i<len(encoded_data)):
        num=varint.decode_bytes(encoded_data[i:])
        compressed_data.append(num)
        i+=1
    decompressed_list=[]
    mtf_decode(compressed_data,list_symbol,decompressed_list)
    decompressed_data=''
    for i in decompressed_list:
        decompressed_data+=i
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
        if i[0]=="mtf":
            i[2]=decompressed_time
            found=1
    if found==0:
        csv_data.append(["mtf","",decompressed_time,"",""])
    with open(csv_file,"w+") as file:
        csv_writer=csv.writer(file)
        csv_writer.writerows(csv_data)

if __name__ == "__main__":
    main()

 
    