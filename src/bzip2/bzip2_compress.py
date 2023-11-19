import bz2

def main():
    data_file="../../data/data.txt"
    compressed_file="../../results/bzip2/compressed_bzip2"
    with open(data_file,"r") as file:
        data=file.read()
    data_byte=bytearray(data,'utf-8')
    compressed_data=bz2.compress(data_byte)

    with open(compressed_file,"wb+") as file:
        file.write(compressed_data)


if __name__=="__main__":
    main()
    
