def lz78_compress(input_text):
    dictionary = {}
    next_code = 1
    compressed = bytearray()
    current_phrase = ""

    for char in input_text:
        current_phrase += char
        if current_phrase not in dictionary:
            dictionary[current_phrase] = next_code
            compressed.append(dictionary[current_phrase[:-1]])
            current_phrase = char
            next_code += 1

    if current_phrase in dictionary:
        compressed.append(dictionary[current_phrase])

    return compressed


def lz78_decompress(compressed):
    dictionary = {0: ""}
    next_code = 1
    decompressed = bytearray()
    current_code = compressed[0]

    for code in compressed[1:]:
        if code in dictionary:
            phrase = dictionary[code]
        elif code == next_code:
            phrase = dictionary[current_code] + dictionary[current_code][0]
        else:
            raise ValueError("Invalid compressed data")

        decompressed.extend(map(ord, phrase))
        dictionary[next_code] = dictionary[current_code] + phrase[0]
        next_code += 1
        current_code = code

    return decompressed.decode('utf-8')


def main():
    with open("input.txt", "r", encoding="utf-8") as file:
        input_text = file.read()

    compressed_data = lz78_compress(input_text)
    print("Compressed Size:", len(compressed_data))

    with open("compressed_lz78.bin", "wb") as file:
        file.write(compressed_data)

    decompressed_text = lz78_decompress(compressed_data)
    print("Decompressed Size:", len(decompressed_text))

    with open("decompressed_lz78.txt", "w", encoding="utf-8") as file:
        file.write(decompressed_text)


if __name__ == "__main__":
    main()
