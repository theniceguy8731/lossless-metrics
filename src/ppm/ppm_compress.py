# 
# Compression application using prediction by partial matching (PPM) with arithmetic coding
# 
# Usage: python ppm-compress.py InputFile OutputFile
# Then use the corresponding ppm-decompress.py application to recreate the original input file.
# Note that both the compressor and decompressor need to use the same PPM context modeling logic.
# The PPM algorithm can be thought of as a powerful generalization of adaptive arithmetic coding.
# 
# Copyright (c) Project Nayuki
# MIT License. See readme file.
# https://www.nayuki.io/page/reference-arithmetic-coding
# 

import contextlib
import arithmeticcoding, ppmmodel
import csv,os
from datetime import datetime


# Must be at least -1 and match ppm-decompress.py. Warning: Exponential memory usage at O(257^n).
MODEL_ORDER = 3


# Command line main application function.


def compress(inp, bitout):
	# Set up encoder and model. In this PPM model, symbol 256 represents EOF;
	# its frequency is 1 in the order -1 context but its frequency
	# is 0 in all other contexts (which have non-negative order).
	enc = arithmeticcoding.ArithmeticEncoder(32, bitout)
	model = ppmmodel.PpmModel(MODEL_ORDER, 257, 256)
	history = []
	
	while True:
		# Read and encode one byte
		symbol = inp.read(1)
		if len(symbol) == 0:
			break
		symbol = symbol[0]
		symbol=ord(symbol)
		encode_symbol(model, history, symbol, enc)
		model.increment_contexts(history, symbol)
		
		if model.model_order >= 1:
			# Prepend current symbol, dropping oldest symbol if necessary
			if len(history) == model.model_order:
				history.pop()
			history.insert(0, symbol)
	
	encode_symbol(model, history, 256, enc)  # EOF
	enc.finish()  # Flush remaining code bits


def encode_symbol(model, history, symbol, enc):
	# Try to use highest order context that exists based on the history suffix, such
	# that the next symbol has non-zero frequency. When symbol 256 is produced at a context
	# at any non-negative order, it means "escape to the next lower order with non-empty
	# context". When symbol 256 is produced at the order -1 context, it means "EOF".
	for order in reversed(range(len(history) + 1)):
		ctx = model.root_context
		for sym in history[ : order]:
			assert ctx.subcontexts is not None
			ctx = ctx.subcontexts[sym]
			if ctx is None:
				break
		else:  # ctx is not None
			if symbol != 256 and ctx.frequencies.get(symbol) > 0:
				enc.write(ctx.frequencies, symbol)
				return
			# Else write context escape symbol and continue decrementing the order
			enc.write(ctx.frequencies, 256)
	# Logic for order = -1
	enc.write(model.order_minus1_freqs, symbol)

def main():
	# Handle command line arguments
	data_file  = "../../data/data.txt"
	compressed_file = "../../results/ppm/compressed_ppm.bin"
	start_time=datetime.now()

	# Perform file compression
	with open(data_file, "r", encoding="utf-8") as inp, \
			contextlib.closing(arithmeticcoding.BitOutputStream(open(compressed_file, "wb+"))) as bitout:
		compress(inp, bitout)
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
		if i[0]=="ppm":
			i[1]=compressed_time
			found=1
	if found==0:
		csv_data.append(["ppm",compressed_time,"",compressed_file_size,data_file_size])
	with open(csv_file,"w+") as file:
		csv_writer=csv.writer(file)
		csv_writer.writerows(csv_data)

# Main launcher
if __name__ == "__main__":
	main()