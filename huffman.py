import heapq
import os


class HuffmanNode:
    def __init__(self, character, frequency):
        self.character = character
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency



class HuffmanCompressor:
    def __init__(self):
        self.heap = []
        self.codes = {}

    def frequency_counter(self, text):
        frequency = {}
        for character in text:
            frequency[character] = frequency.get(character, 0) + 1
        return frequency

    def build_heap(self, frequency):
        for character, freq in frequency.items():
            node = HuffmanNode(character, freq)
            heapq.heappush(self.heap, node)

    def build_tree(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            merged_node = HuffmanNode(None, node1.frequency + node2.frequency)
            merged_node.left = node1
            merged_node.right = node2
            heapq.heappush(self.heap, merged_node)

    def build_codes(self, root, current_code):
        if root is None:
            return

        if root.character is not None:
            self.codes[root.character] = current_code
            return

        self.build_codes(root.left, current_code + "0")
        self.build_codes(root.right, current_code + "1")

    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    def pad_encoded_text(self, encoded_text):
        padding_amount = 8 - (len(encoded_text) % 8)
        for _ in range(padding_amount):
            encoded_text += "0"

        padding_info = "{0:08b}".format(padding_amount)
        padded_encoded_text = padding_info + encoded_text
        return padded_encoded_text

    def get_byte_array(self, padded_encoded_text):
        if len(padded_encoded_text) % 8 != 0:
            raise ValueError("O texto codificado precisa estar em um múltiplo de 8 bits.")

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

    def compress(self, input_file, output_file):
        with open(input_file, "r") as file:
            text = file.read()
            text = text.rstrip()

        frequency = self.frequency_counter(text)
        self.build_heap(frequency)
        self.build_tree()
        self.build_codes(self.heap[0], "")

        encoded_text = self.get_encoded_text(text)
        padded_encoded_text = self.pad_encoded_text(encoded_text)

        byte_array = self.get_byte_array(padded_encoded_text)

        with open(output_file, "wb") as file:
            file.write(bytes(byte_array))

        print("Comprimindo ", output_file, "...")
        original_size = os.path.getsize(input_file)
        compressed_size = os.path.getsize(output_file)
        compression_ratio = 100 * (original_size / compressed_size)

        print(f"Taxa de Compressão: 100 * ({original_size} / {compressed_size}) ==> ""{0:.2f}%".format(compression_ratio))



class HuffmanDecompressor:
    def __init__(self):
        self.codes = {}

    def decode_text(self, encoded_text, root):
        decoded_text = ""
        current_node = root
        for bit in encoded_text:
            if bit == "0":
                current_node = current_node.left
            else:
                current_node = current_node.right

            if current_node.character is not None:
                decoded_text += current_node.character
                current_node = root

        return decoded_text

    def remove_padding(self, padded_encoded_text):
        padding_info = padded_encoded_text[:8]
        padding_amount = int(padding_info, 2)
        encoded_text = padded_encoded_text[8:-padding_amount]
        return encoded_text

    def decompress(self, input_file, output_file):
        with open(input_file, "rb") as file:
            bit_string = ""
            byte = file.read(1)
            while byte:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, "0")
                bit_string += bits
                byte = file.read(1)

        encoded_text = self.remove_padding(bit_string)
        decoded_text = self.decode_text(encoded_text, self.root)

        with open(output_file, "w") as file:
            file.write(decoded_text)

        print("Descomprimindo", output_file, "...")
        original_size = os.path.getsize(input_file)
        compressed_size = os.path.getsize(output_file)
        compression_ratio = 100 * (original_size / compressed_size)

        print(f"Taxa de Compressão: 100 * ({original_size} / {compressed_size}) ==> ""{0:.2f}%".format(compression_ratio))




class HuffmanFrequencyAnalyzer:
    def __init__(self):
        self.frequency = {}

    def frequency_counter(self, text):
        for character in text:
            self.frequency[character] = self.frequency.get(character, 0) + 1

    def print_symbol_table(self):
        print("Tabela de Símbolos:")
        print("-------------------")
        print("| Símbolo | Frequência |")
        print("-------------------")
        for symbol, freq in self.frequency.items():
            print("|   {:4s}  |   {:6d}   |".format(symbol, freq))
        print("-------------------")

    def analyze(self, input_file):
        with open(input_file, "r") as file:
            text = file.read()
            text = text.rstrip()

        self.frequency_counter(text)
        self.print_symbol_table()
