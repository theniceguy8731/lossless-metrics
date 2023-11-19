import bz2
import csv,os
from datetime import datetime
def main():
    data_file="../../data/data.txt"
    compressed_file="../../results/bzip2/compressed_bzip2"
    start_time=datetime.now()
    with open(data_file,"r") as file:
        data=file.read()
    data_byte=bytearray(data,'utf-8')
    compressed_data=bz2.compress(data_byte)
    with open(compressed_file,"wb+") as file:
        file.write(compressed_data)
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
        if i[0]=="bzip2":
            i[1]=compressed_time
            found=1
    if found==0:
        csv_data.append(["bzip2",compressed_time,"",compressed_file_size,data_file_size])
    with open(csv_file,"w+") as file:
        csv_writer=csv.writer(file)
        csv_writer.writerows(csv_data)


if __name__=="__main__":
    main()
    
