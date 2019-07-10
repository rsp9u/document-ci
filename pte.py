import zlib
from string import digits, ascii_uppercase, ascii_lowercase


class PlantUML:
    def __init__(self, text):
        self.text = text
        self.pte = self.deflate_and_encode(text)

    def deflate_and_encode(self, plantuml_text):
        zlibbed_str = zlib.compress(plantuml_text.encode('utf-8'))
        compressed_string = zlibbed_str[2:-4]
        return self.encode(compressed_string.decode('latin-1'))

    def encode(self, data):
        res = ""
        for i in range(0, len(data), 3):
            if (i+2 == len(data)):
                res += self._encode3bytes(ord(data[i]), ord(data[i+1]), 0)
            elif (i+1 == len(data)):
                res += self._encode3bytes(ord(data[i]), 0, 0)
            else:
                res += self._encode3bytes(ord(data[i]), ord(data[i+1]), ord(data[i+2]))
        return res

    def _encode3bytes(self, b1, b2, b3):
        c1 = b1 >> 2
        c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
        c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
        c4 = b3 & 0x3F
        res = ""
        res += self._encode6bit(c1 & 0x3F)
        res += self._encode6bit(c2 & 0x3F)
        res += self._encode6bit(c3 & 0x3F)
        res += self._encode6bit(c4 & 0x3F)
        return res

    def _encode6bit(self, b):
        chrmap = digits + ascii_uppercase + ascii_lowercase + '-_'
        if 0b000000 <= b and b <= 0b111111:
            return chrmap[b]
        else:
            return '?'


if __name__ == "__main__":
    import sys
    print(PlantUML(sys.stdin.read()).pte)
