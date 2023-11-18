import varint

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
    list_symbol= list()
    for i in range(128):
        list_symbol.append(chr(i))
    compressed_file="../../results/mtf/compressed_mtf.bin"
    with open(compressed_file,"rb") as file:
        encoded_data=file.read()
    i=0
    compressed_data=[]
    while(i<len(encoded_data)):
        num=varint.decode_bytes(encoded_data[i:])
        compressed_data.append(num)
        i+=1
    decompressed_list=[]
    decompressed_file="../../results/mtf/decompressed_mtf.txt"
    mtf_decode(compressed_data,list_symbol,decompressed_list)
    decompressed_data=''
    for i in decompressed_list:
        decompressed_data+=i
    with open(decompressed_file,"w+") as file:
        file.write(decompressed_data)    


if __name__ == "__main__":
    main()

 
    