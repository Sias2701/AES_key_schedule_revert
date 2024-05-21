from aes import *

key        = b'\xc3,\\\xa6\xb5\x80^\x0c\xdb\x8d\xa5z*\xb6\xfe\\'
ciphertext = b'\xd1O\x14j\xa4+O\xb6\xa1\xc4\x08B)\x8f\x12\xdd'
plaintext = b'crypto{MYAES128}'

def encrypt_with_status(key, plaintext):
    round_keys = expand_key(key)
    stateMat = bytes_to_matrix(plaintext)
    stateMat = add_round_key(stateMat, round_keys[0])

    interval = []
    interval.append(stateMat)
    for i in range(1, N_ROUNDS):
            stateMat = sub_bytes(stateMat, sbox=s_box)
            shift_rows(stateMat)
            mix_columns(stateMat)
            stateMat = add_round_key(stateMat, round_keys[i])
            interval.append(stateMat)

    stateMat = sub_bytes(stateMat, sbox=s_box)
    shift_rows(stateMat)
    stateMat = add_round_key(stateMat, round_keys[-1])
    interval.append(stateMat)
    return interval, round_keys

interval, round_keys = encrypt_with_status(key, plaintext)

## We assume output of round 8 and output of round 9 is known.

round_num = 9

val1 = interval[8]
val2 = interval[9]

print(val1)
print(val2)

val1 = sub_bytes(val1, sbox=s_box)
shift_rows(val1)
mix_columns(val1)

w = add_round_key(val1, val2)

for i in range(round_num):
    prev_w = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]
    prev_w[3] = [i ^ j for i, j in zip(w[2], w[3])]
    prev_w[2] = [i ^ j for i, j in zip(w[1], w[2])]
    prev_w[1] = [i ^ j for i, j in zip(w[0], w[1])]

    prev_w3 = prev_w[3].copy()
    prev_w3[0], prev_w3[1], prev_w3[2], prev_w3[3] = prev_w3[1], prev_w3[2], prev_w3[3], prev_w3[0]
    prev_w3 = [s_box[i] for i in prev_w3]
    prev_w3[0] ^= r_con[round_num - i]
    prev_w[0] = [i ^ j for i, j in zip(prev_w3, w[0])]

    w = prev_w

    print(w)
