import bz2
import csv,os
from datetime import datetime
def main():
    compressed_file="../../results/bzip2/compressed_bzip2"
    decompressed_file="../../results/bzip2/decompressed_bzip2.txt"
    start_time=datetime.now()
    with open(compressed_file,"rb") as file:
        compressed_data=file.read()
    
    decompressed_data_byte=bz2.decompress(compressed_data)
    decompressed_data=decompressed_data_byte.decode()

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
        if i[0]=="bzip2":
            i[2]=decompressed_time
            found=1
    if found==0:
        csv_data.append(["bzip2","",decompressed_time,"",""])
    with open(csv_file,"w+") as file:
        csv_writer=csv.writer(file)
        csv_writer.writerows(csv_data)


if __name__=="__main__":
    main()
    
