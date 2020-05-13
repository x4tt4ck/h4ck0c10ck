#!/usr/bin/env python3
# This is my solution to Potentially Eazzzy
# You give it an email as input, and it gives a license as output.

try:
    FLAG = open("flag.txt", "r").read()
except:
    FLAG = "DogeCTF{Flag is different on the server}"

import itertools

ALPHABET = [chr(i) for i in range(ord("*"), ord("z")+1)]

def print_flag():
    print("Generating flag...")
    print(FLAG)

a = lambda c: ord(ALPHABET[0]) + (c % len(ALPHABET))

## ord(ALPHABET[0]) == 42
## len(ALPHABET) == 81
## a = lambda c: 42 + (c % 81)

o = lambda c: ord(c)

## o is just short for ord

oa = lambda c: a(o(c))

## easy way to pass an ord into function a.

def indexes(s, needle):
    a = 0
    for idx, c in enumerate(s):
        if c == needle:
            a += idx
    return a

def m(one, two, three, four):
    d = 40
    s = 42
    s1, s2, s3 = one - 42, two - 42, three - 42
    return sum([s1, s2, s3]) % 40 == four % 40

def l(two, three, four):
    one = ((sum([two, three]) + (-42 * 3)) % 40) - (four % 40)
    while one > 0:
        one = one - 40
    one = -one
    while one < 0x2a:
        one += 40
    return one

def getLicense(email):
    email = email.strip()

    key = [ord('A')] * 32 ## contains ascii codes for the key, the key is 32 characters long.

    email = email[:31].ljust(31, "*") ## truncates the email to 31 characters, and then adds stars to the end of the string until it is 31 characters long.
    email += "*" ## adds a star, email is now 32 characters long.

    ## email and key are now both 32 characters long, and the email has trailing stars.

    for c in itertools.chain(email): ## all characters in the email and key has to be in the ascii range 2a-7a
        if c not in ALPHABET:
            return "Sorry! Your email has to be in the ascii range 2A-7A. Look up ascii codes if you don't know what i'm talking about."

    # FAKEKEY*************************

    if email.count("@") != 1: ## email has to have at least one @ sign
        return "You need to have an @ sign in your email."

    key[0] = ord('Z') ## first character of key has to be a z

    dotcount = email.count(".")
    if dotcount < 0 or dotcount >= len(ALPHABET): ## there has to be between 0 and 80 periods in the email
        return "???"

    key[1] = a(dotcount)

    key[2] = a(indexes(email, "*") + 7)

    key[3] = a(key[1]%30 + key[2]%30) + 5

    key[5] = a(key[3] + 52) ## the order of key calculation matters, because the value of key[4] depends on key[5].

    key[4] = a(sum(o(i) for i in email)%60 + key[5]) ## this is getting kind of nuts

    key[7] = a(key[1] + key[2] - key[3])

    key[6] = a((key[7]%8)*2)

    key[8] = a((key[6]%16) / 2)

    key[9] = a(key[6] + key[4] + key[8] - 4)

    key[10] = a((key[1])%2 * 8 + key[2] % 3 + key[3] % 4)

    oldEmail = email[:]
    email = []

    for i in oldEmail:
        email.append(ord(i))

#    if not m(email[16], email[17], key[21], email.count("s")): ## I will just start with this
#        return False

    key[21] = l(email[16], email[17], oldEmail.count('s'))

#    if not m(email[7], key[13], key[4], 18):
#        return False

    key[13] = l(email[7], key[4], 18)

#    if not m(email[11], key[13], key[16], 792):
#        return False

    key[16] = l(email[11], key[13], 792)

#    if not m(email[21], key[24], key[13], 41):
#        return False

    key[24] = l(email[21], key[13], 41)

#    if not m(email[9], key[14], key[3], 23):
#        return False

    key[14] = l(email[9], key[3], 23)

#    if not m(email[10], key[15], key[10], 3):
#        return False

    key[15] = l(email[10], key[10], 3)

#    if not m(email[12], key[17], key[4], email.count("d")):
#        return False

    key[17] = l(email[12], key[4], oldEmail.count('d'))

#    if not m(email[20], key[23], key[17], 9):
#        return False

    key[23] = l(email[20], key[17], 9)

#    if not m(email[31], key[31], email[4], 7):
#        return False

    key[31] = l(email[31], email[4], 7)

#    if not m(email[13], key[18], key[7], email.count("a")):
#        return False

    key[18] = l(email[13], key[7], oldEmail.count('a'))

#    if not m(email[30], key[30], email[18], 4):
#        return False

    key[30] = l(email[30], email[18], 4)

#    if not m(email[28], email[29], key[29], 2):
#        return False

    key[29] = l(email[28], email[29], 2)

#    if not m(email[26], email[27], key[28], 7):
#        return False

    key[28] = l(email[26], email[27], 7)

#    if not m(email[3], key[11], key[12], 8):
#        return False

    key[11] = ord('Z') # idk
    key[12] = l(email[3], key[11], 8)

#    if not m(email[14], key[19], key[8], email.count("w")):
#        return False

    key[19] = l(email[14], key[8], oldEmail.count('w'))



#    if not m(email[15], key[20], key[1], oldEmail.count("g")):
#        return False

    key[20] = l(email[15], key[1], oldEmail.count('g'))

#    if not m(email[18], email[19], key[22], oldEmail.count("m")):
#        return False

    key[22] = l(email[18], email[19], oldEmail.count('m'))

#    if not m(email[22], key[25], key[10], 3):
#        return False

    key[25] = l(email[22], key[10], 3)

#    if not m(email[23], key[26], email[14], oldEmail.count("1")):
#        return False

    key[26] = l(email[23], email[14], oldEmail.count('1'))

#    if not m(email[24], email[25], key[27], oldEmail.count("*")):
#        return False

    key[27] = l(email[24], email[25], oldEmail.count('*'))

    s = ''
    for i in key: ## convert array to string
        s += chr(int(i))

    return "Your key is: " + s

def main():
    email = input("What email do you want to use? ")

    print(getLicense(email))

main()

## key has to be 32 characters in length.
## all characters in the email and key has to be in the ascii range 2a-7a
