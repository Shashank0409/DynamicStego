import random
import zstandard as zstd
import brotli
import lzma
import bz2 

class Compression:
    def __init__(self):
        #initializes all the algorithms available
        self.algorithms = {
            "00": (zstd.ZstdCompressor().compress,zstd.ZstdDecompressor().decompress),
            "01": (brotli.compress, brotli.decompress),
            "10": (lzma.compress, lzma.decompress),
            "11": (bz2.compress, bz2.decompress)
        }
    
    #Returns compressed_data and compression code
    def compressor(self, data):
        #chooses a random algorithm and compresses the data
        compression_code=random.choice(tuple(self.algorithms.keys()))
        compressed_data=self.algorithms[compression_code][0](data)

        return compressed_data,compression_code

    #Returns decompressed data
    def decompressor(self, compressed_data, compression_code):
        #decompresses the data using the chosen algorithm
        decompressed_data=self.algorithms[compression_code][1](compressed_data)

        return decompressed_data

'''
def sample_compression():
    # Sample data
    codes={'00':"Zstandard","01":"Brotli","10":"lzma","11":"bzip2"}
    data = "Generating random paragraphs can be an excellent way for writers to get their creative flow going at the beginning of the day. The writer has no idea what topic the random paragraph will be about when it appears. This forces the writer to use creativity to complete one of three common writing challenges. The writer can use the paragraph as the first one of a short story and build upon it. A second option is to use the random paragraph somewhere in a short story they create. The third option is to have the random paragraph be the ending paragraph in a short story. No matter which of these challenges is undertaken, the writer is forced to use creativity to incorporate the paragraph into their writing. The light was out on the front porch of the house. This was strange. Judy couldn't remember a time when she had ever seen it out. She hopped out of her car and walked to the door. It was slightly ajar and she knew this meant something terrible. She gently pushed the door open and hall her fears were realized. Surprise! Happy Birthday! everyone shouted. If you're looking for random paragraphs, you've come to the right place. When a random word or a random sentence isn't quite enough, the next logical step is to find a random paragraph. We created the Random Paragraph Generator with you in mind. The process is quite simple. Choose the number of random paragraphs you'd like to see and click the button. Your chosen number of paragraphs will instantly appear."
    print("Original Data size: " , len(data))
    data=data.encode()

    #compression
    compressor = Compression()
    compressed_data,compression_code = compressor.compressor(data)
    print("compressed data size: " , len(compressed_data))
    print("Compression algorithm: " ,codes[compression_code])

    #decompression
    decompressed_data = compressor.decompressor(compressed_data,compression_code)
    decompressed_data = decompressed_data.decode()
    print(f"Compression Ratio: {len(compressed_data)/len(data)}")

sample_compression()
'''