import sys
import varint

def lzw_compress(input_text):
    table = {chr(i): i for i in range(256)}
    next_code = 256
    compressed = bytearray()
    phrase = input_text[0]

    for char in input_text[1:]:
        if phrase + char in table:
            phrase += char
        else:
            compressed.extend(varint.encode(table[phrase]))
            table[phrase + char] = next_code
            next_code += 1
            phrase = char

    compressed.extend(varint.encode(table[phrase]))
    return compressed

def lzw_decompress(compressed):
    table = {i: chr(i) for i in range(256)}
    next_code = 256
    decompressed_text = []

    i = 0
    phrase = table[compressed[i]]
    decompressed_text.append(phrase)
    i += 1

    while i < len(compressed):
        code= varint.decode_bytes(compressed[i:])
        bytes_read=len(varint.encode(code))
        i += bytes_read

        if code in table:
            entry = table[code]
        elif code == next_code:
            entry = phrase + phrase[0]
        else:
            raise ValueError("Invalid compressed code")

        decompressed_text.append(entry)
        table[next_code] = phrase + entry[0]
        next_code += 1
        phrase = entry

    return ''.join(decompressed_text)


def main():
    with open("../../data/data.txt", "r", encoding="utf-8") as file:
        input_text = file.read()
    print("Input size:", len(input_text))

    compressed_data = lzw_compress(input_text)
    print("Compressed Size:", sys.getsizeof(compressed_data))

    with open("../../results/lzw/compressed_lzw.bin", "wb") as file:
        file.write(compressed_data)

    decompressed_text = lzw_decompress(compressed_data)
    print("Decompressed Size:", len(decompressed_text))

    with open("../../results/lzw/decompressed_lzw.txt", "w", encoding="utf-8") as file:
        file.write(decompressed_text)


if __name__ == "__main__":
    main()
