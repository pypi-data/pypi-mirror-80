from string import ascii_letters


class CaesarCipher:
    def __init__(self, key = 0):
        self.__key = key

    def encrypt(self, input_string: str, key: int, alphabet=None) -> str:
        """
        encrypt
        =======
        Encodes a given string with the caesar cipher and returns the encoded
        message
        Parameters:
        -----------
        *   input_string: the plain-text that needs to be encoded
        *   key: the number of letters to shift the message by
        Optional:
        *   alphabet (None): the alphabet used to encode the cipher, if not
            specified, the standard english alphabet with upper and lowercase
            letters is used
        Returns:
        *   A string containing the encoded cipher-text
        More on the caesar cipher
        =========================
        The caesar cipher is named after Julius Caesar who used it when sending
        secret military messages to his troops. This is a simple substitution cipher
        where very character in the plain-text is shifted by a certain number known
        as the "key" or "shift".
        Example:
        Say we have the following message:
        "Hello, captain"
        And our alphabet is made up of lower and uppercase letters:
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        And our shift is "2"
        We can then encode the message, one letter at a time. "H" would become "J",
        since "J" is two letters away, and so on. If the shift is ever two large, or
        our letter is at the end of the alphabet, we just start at the beginning
        ("Z" would shift to "a" then "b" and so on).
        Our final message would be "Jgnnq, ecrvckp"
        Further reading
        ===============
        *   https://en.m.wikipedia.org/wiki/Caesar_cipher
        Doctests
        ========
        >>> encrypt('The quick brown fox jumps over the lazy dog', 8)
        'bpm yCqks jzwEv nwF rCuxA wDmz Bpm tiHG lwo'
        >>> encrypt('A very large key', 8000)
        's nWjq dSjYW cWq'
        >>> encrypt('a lowercase alphabet', 5, 'abcdefghijklmnopqrstuvwxyz')
        'f qtbjwhfxj fqumfgjy'
        """
        # Set default alphabet to lower and upper case english chars
        alpha = alphabet or ascii_letters

        # The final result string
        result = ""

        for character in input_string:
            if character not in alpha:
                # Append without encryption if character is not in the alphabet
                result += character
            else:
                # Get the index of the new key and make sure it isn't too large
                new_key = (alpha.index(character) + key) % len(alpha)

                # Append the encoded character to the alphabet
                result += alpha[new_key]

        return result


    def decrypt(self, input_string: str, key: int, alphabet=None) -> str:
        """
        decrypt
        =======
        Decodes a given string of cipher-text and returns the decoded plain-text
        Parameters:
        -----------
        *   input_string: the cipher-text that needs to be decoded
        *   key: the number of letters to shift the message backwards by to decode
        Optional:
        *   alphabet (None): the alphabet used to decode the cipher, if not
            specified, the standard english alphabet with upper and lowercase
            letters is used
        Returns:
        *   A string containing the decoded plain-text
        More on the caesar cipher
        =========================
        The caesar cipher is named after Julius Caesar who used it when sending
        secret military messages to his troops. This is a simple substitution cipher
        where very character in the plain-text is shifted by a certain number known
        as the "key" or "shift". Please keep in mind, here we will be focused on
        decryption.
        Example:
        Say we have the following cipher-text:
        "Jgnnq, ecrvckp"
        And our alphabet is made up of lower and uppercase letters:
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        And our shift is "2"
        To decode the message, we would do the same thing as encoding, but in
        reverse. The first letter, "J" would become "H" (remember: we are decoding)
        because "H" is two letters in reverse (to the left) of "J". We would
        continue doing this. A letter like "a" would shift back to the end of
        the alphabet, and would become "Z" or "Y" and so on.
        Our final message would be "Hello, captain"
        Further reading
        ===============
        *   https://en.m.wikipedia.org/wiki/Caesar_cipher
        Doctests
        ========
        >>> decrypt('bpm yCqks jzwEv nwF rCuxA wDmz Bpm tiHG lwo', 8)
        'The quick brown fox jumps over the lazy dog'
        >>> decrypt('s nWjq dSjYW cWq', 8000)
        'A very large key'
        >>> decrypt('f qtbjwhfxj fqumfgjy', 5, 'abcdefghijklmnopqrstuvwxyz')
        'a lowercase alphabet'
        """
        # Turn on decode mode by making the key negative
        key *= -1

        return self.encrypt(input_string, key, alphabet)

