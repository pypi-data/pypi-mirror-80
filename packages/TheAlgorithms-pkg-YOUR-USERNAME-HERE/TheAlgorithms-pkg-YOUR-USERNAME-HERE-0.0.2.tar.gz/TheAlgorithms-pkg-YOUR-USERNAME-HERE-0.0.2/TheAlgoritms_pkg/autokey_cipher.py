ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '

class AutokeyCipher:
    def __init__(self, key = 0):
        self.__key = key

    def encrypt (self, messages, keys):  
        cipher = []
        k_index = 0
        key = keys.upper()
        for i in messages:
            text = ALPHA.find(i.upper())
            text += ALPHA.find(key[k_index])
            key += i.upper()
            text %= len(ALPHA)
            k_index += 1
    
            cipher.append(ALPHA[text])
        return ''.join(cipher)
            
            
    def decrypt(self, messages, keys):
        cipher = []
        k_index = 0
        key = keys.upper()
        for i in messages:
            text = ALPHA.find(i.upper())
            text -= ALPHA.find(key[k_index])
            key += ALPHA[text]
            text %= len(ALPHA)
            k_index += 1
    
            cipher.append(ALPHA[text])
        return ''.join(cipher)



        