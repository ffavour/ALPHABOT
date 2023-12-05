import random
import string


def genera_stringa_alfanumerica(lunghezza=40):
    caratteri = string.ascii_letters + string.digits  # lettere e numeri
    stringa_alfanumerica = ''.join(random.choice(caratteri) for _ in range(lunghezza))
    return stringa_alfanumerica


