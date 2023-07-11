from huffman import *

nome_arquivo = ""
print("\nCompressão de Huffman – Análise de frequência símbolos e compressão de Huffman")


while True:
    entrada = input()
    opcao = entrada[:9]
    nome_arquivo = entrada[13:]


    if opcao == "./huff -h":
        print("""Options:
-h Mostra este texto de ajuda
-c Realiza a compressão
-d Realiza a descompressão
-s Realiza apenas a análise de frequência e imprime a tabela de símbolos
-f <file> Indica o arquivo a ser processado (comprimido, descomprimido ou para apresentar a tabela de símbolos)
        """)

    elif opcao == "./huff -c":
        compressor = HuffmanCompressor()
        compressor.compress(nome_arquivo, f"{nome_arquivo}.huff")

    elif opcao == "./huff -d":
        decompressor = HuffmanDecompressor()
        decompressor.root = compressor.heap[0]
        decompressor.decompress(nome_arquivo, "descomp_arquivo.txt")

    elif opcao == "./huff -s":
        analyzer = HuffmanFrequencyAnalyzer()
        analyzer.analyze(nome_arquivo)
