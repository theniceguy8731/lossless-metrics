def lz77_compress(input_text, window_size=10, buffer_size=10):
    compressed = bytearray()
    index = 0

    while index < len(input_text):
        match_length = 0
        best_match = (0, 0)

        for i in range(1, min(buffer_size + 1, len(input_text) - index + 1)):
            substring = input_text[index:index + i]
            window_index = max(0, index - window_size)
            match_index = input_text.rfind(substring, window_index, index+i-1)
            if match_index != -1 and match_index < index:
                distance = index - match_index
                if distance <= window_size and i > match_length:
                    match_length = i
                    best_match = (distance, match_length)

        if match_length > 0 and index+match_length<len(input_text):
            compressed.append(best_match[0])
            compressed.append(best_match[1])
            compressed.append(ord(input_text[index + match_length]))
            index += match_length+1
        else:
            compressed.append(0)
            compressed.append(0) 
            compressed.append(ord(input_text[index]))
            index += 1
        

    return compressed

def lz77_decompress(compressed):
    decompressed = ""
    index = 0

    while index < len(compressed):
        distance = compressed[index]
        length = compressed[index + 1]
        literal_char = compressed[index + 2]
        if distance > 0:
            start_index = max(0, len(decompressed) - distance)
            for _ in range(length):
                decompressed += decompressed[start_index]
                start_index += 1
            decompressed+=chr(literal_char)
        else:
            decompressed += chr(literal_char)

        index += 3 

    return decompressed


def main():
    with open("../../data/data.txt", "r", encoding="utf-8") as file:
        input_text = file.read()

    compressed_data = lz77_compress(input_text)
    
    with open("../../results/lz77/lz77_compressed.bin", "wb") as file:
        file.write(compressed_data)

    decompressed_text = lz77_decompress(compressed_data)
    
    with open("../../results/lz77/lz77_decompressed.txt", "w", encoding="utf-8") as file:
        file.write(decompressed_text)


if __name__ == "__main__":
    main()


def main():
    with open("../../data/data.txt", "r", encoding="utf-8") as file:
        input_text = file.read()

    compressed_data = lz77_compress(input_text)
    
    with open("../../results/lz77/lz77_compressed.bin", "wb") as file:
        file.write(compressed_data)

    decompressed_text = lz77_decompress(compressed_data)
    
    with open("../../results/lz77/lz77_decompressed.txt", "w", encoding="utf-8") as file:
        file.write(decompressed_text)


if __name__ == "__main__":
    main()
