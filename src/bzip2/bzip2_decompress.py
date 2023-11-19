import bz2

def main():
    compressed_file="../../results/bzip2/compressed_bzip2"
    decompressed_file="../../results/bzip2/decompressed_bzip2.txt"

    with open(compressed_file,"rb") as file:
        compressed_data=file.read()
    
    decompressed_data_byte=bz2.decompress(compressed_data)
    decompressed_data=decompressed_data_byte.decode()

    with open(decompressed_file,"w+") as file:
        file.write(decompressed_data)



if __name__=="__main__":
    main()
    
