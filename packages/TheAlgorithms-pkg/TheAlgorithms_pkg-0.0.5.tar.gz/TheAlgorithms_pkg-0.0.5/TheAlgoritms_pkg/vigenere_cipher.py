LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class VigenereCipher:
    def __init__(self, key = 0):
        self.__key = key

    def encrypt(self, message, key):
        """
        >>> encryptMessage('HDarji', 'This is Harshil Darji from Dharmaj.')
        'Akij ra Odrjqqs Gaisq muod Mphumrs.'
        """
        return self.translateMessage(message, key, "encrypt")


    def decrypt(self,message, key):
        """
        >>> decryptMessage('HDarji', 'Akij ra Odrjqqs Gaisq muod Mphumrs.')
        'This is Harshil Darji from Dharmaj.'
        """
        return self.translateMessage(message, key, "decrypt")


    def translateMessage(self, message, key, mode):
        translated = []
        keyIndex = 0
        key = key.upper()

        for symbol in message:
            num = LETTERS.find(symbol.upper())
            if num != -1:
                if mode == "encrypt":
                    num += LETTERS.find(key[keyIndex])
                elif mode == "decrypt":
                    num -= LETTERS.find(key[keyIndex])

                num %= len(LETTERS)

                if symbol.isupper():
                    translated.append(LETTERS[num])
                elif symbol.islower():
                    translated.append(LETTERS[num].lower())

                keyIndex += 1
                if keyIndex == len(key):
                    keyIndex = 0
            else:
                translated.append(symbol)
        return "".join(translated)