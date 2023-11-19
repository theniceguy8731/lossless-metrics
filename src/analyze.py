import csv
import numpy as np
import matplotlib.pyplot as plt


csv_data=[]
csv_file="../results/final-result.csv"

with open(csv_file,"r+") as file:
    csv_reader=csv.reader(file)
    for row in csv_reader:
        csv_data.append(row)
print(csv_data)

algo_name=[]
compression_time=[]
decompression_time=[]
compressed_file_size=[]
compression_ratio=[]
for i in csv_data:
    if i[0]=="Algo_name":
        pass
    else:
        algo_name.append(i[0])
        compression_time.append(int(i[1]))
        decompression_time.append(int(i[2]))
        compressed_file_size.append(int(i[3]))
        compression_ratio.append(int(i[3])/int(i[4]))

print(algo_name,compression_time,decompression_time,compressed_file_size)

# fig1 = plt.figure(figsize = (20, 10))
 
# creating the bar plot
plt.figure(200)
plt.bar(algo_name, compression_time, color ='maroon', 
        width = 0.4)
plt.xlabel("Algorithms")
plt.ylabel("Compression time")
plt.title("Compression time comparision graph")
plt.show()


plt.figure(300)
plt.bar(algo_name, decompression_time, color ='maroon', 
        width = 0.4)
plt.xlabel("Algorithms")
plt.ylabel("Decompression time")
plt.title("Decompression time comparision graph")
plt.show()


plt.figure(400)
plt.bar(algo_name, compressed_file_size, color ='maroon', 
        width = 0.4)
plt.xlabel("Algorithms")
plt.ylabel("Compression file size")
plt.title("Compression file size comparision graph")
plt.show()

plt.figure(500)
plt.bar(algo_name, compression_ratio, color ='maroon', 
        width = 0.4)
plt.xlabel("Algorithms")
plt.ylabel("Compression ration")
plt.title("Compression ratio graph")
plt.show()