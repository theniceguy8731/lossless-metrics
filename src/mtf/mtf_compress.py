import varint
import csv,os
from datetime import datetime

def search(list_symbols,character):
    for i in range(len(list_symbols)):
        if list_symbols[i]==character:
            return i
        

def move_front(index,list_symbols):
    character=list_symbols.pop(index)
    list_symbols.insert(0,character)

def mtf_encode(input_txt,list_symbols,output_txt):
    for i in input_txt:
        index=search(list_symbols,i)
        output_txt.append(index)
        move_front(index,list_symbols)

def main():
    data_file="../../data/data.txt"
    compressed_file="../../results/mtf/compressed_mtf.bin"
    
    start_time=datetime.now()
    list_symbol= list()
    for i in range(128):
        list_symbol.append(chr(i))
    with open(data_file,"r") as file:
        input_text = file.read()
    output_list=list()
    mtf_encode(input_text,list_symbol,output_list)
    compressed=bytearray()
    for i in output_list:
        compressed.extend(varint.encode(i))
    with open(compressed_file,"wb+") as file:
        file.write(compressed)
    end_time=datetime.now()
    compressed_time=(end_time-start_time).microseconds
    compressed_file_size=os.path.getsize(compressed_file)
    data_file_size=os.path.getsize(data_file)
    csv_file="../../results/final-result.csv"
    csv_data=[]
    with open(csv_file,"r+") as file:
        csv_reader=csv.reader(file)
        for row in csv_reader:
            csv_data.append(row)
    found=0
    for i in csv_data:
        if i[0]=="mtf":
            i[1]=compressed_time
            found=1
    if found==0:
        csv_data.append(["mtf",compressed_time,"",compressed_file_size,data_file_size])
    with open(csv_file,"w+") as file:
        csv_writer=csv.writer(file)
        csv_writer.writerows(csv_data)
if __name__ == "__main__":
    main()

 
    