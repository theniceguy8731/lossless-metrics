import varint

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
    list_symbol= list()
    for i in range(128):
        list_symbol.append(chr(i))
    input_file="../../data/data.txt"
    with open(input_file,"r") as file:
        input_text = file.read()
    output_list=list()
    mtf_encode(input_text,list_symbol,output_list)
    output_file="../../results/mtf/compressed_mtf.bin"
    compressed=bytearray()
    for i in output_list:
        compressed.extend(varint.encode(i))
    with open(output_file,"wb+") as file:
        file.write(compressed)

if __name__ == "__main__":
    main()

 
    