import varint
import sys
def lz78_compress(input_text):
    dictionary = {}
    next_code = 0
    compressed = bytearray()
    i = 0
    while i < len(input_text):
        if input_text[i] not in dictionary.values():
            x=0
            compressed.extend(varint.encode(0))
            compressed.extend(input_text[i].encode('utf-8'))
            next_code += 1
            dictionary[next_code] = input_text[i]
        else:
            phrase = input_text[i]
            while phrase in dictionary.values() and i<len(input_text)-1:
                i += 1
                phrase += input_text[i]
            code=0
            for x in dictionary.keys():
                if dictionary[x]==phrase[0:-1]:
                    code=x
                    break
            compressed.extend(varint.encode(code))
            compressed.extend(phrase[-1].encode('utf-8'))
            next_code += 1
            dictionary[next_code] = phrase
        # print(dictionary.get(next_code),next_code)
        i += 1

    return compressed

def lz78_decompress(compressed):
    dictionary = {0: b""}
    next_code = 0
    i = 0
    decompressed_text = ""

    while i < len(compressed):
        code= varint.decode_bytes(compressed[i:])
        consumed=len(varint.encode(code))
        i += consumed
        if code == 0:
            char = chr(varint.decode_bytes(compressed[i:]))
            i += 1
            decompressed_text+=char
            # print(char)
            next_code += 1
            dictionary[next_code] = char

        else:
            phrase = dictionary[code]
            char = chr(varint.decode_bytes(compressed[i:]))
            i += 1

            phrase += char
            decompressed_text+=phrase

            next_code += 1
            dictionary[next_code] = phrase

    return decompressed_text


def main():
    with open("new.txt", "r", encoding="utf-8") as file:
        input_text = file.read()
    print("Input size:", len(input_text))

    compressed_data = lz78_compress(input_text)
    print("Compressed Size:", len(compressed_data))

    with open("../../results/lz78/compressed_lz78.bin", "wb") as file:
        file.write(compressed_data)
    
    decompressed_text = lz78_decompress(compressed_data)
    print("Decompressed Size:", len(decompressed_text))

    with open("../../results/lz78/decompressed_lz78.txt", "w", encoding="utf-8") as file:
        file.write(decompressed_text)

if __name__ == "__main__":
    main()
