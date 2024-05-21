from aes import *


excepted_key = bytes.fromhex('c32c5ca6b5805e0cdb8da57a2ab6fe5c')

# see poc.py
layer1 = bytes.fromhex('45d4137c30e2004b38ca8655cb2a506a')

layer2 = bytes.fromhex('2de529faa9425d83ecd5cbd9389f7daf')
round_num = 9

val1 = bytes_to_matrix(layer1)
val2 = bytes_to_matrix(layer2)

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
print(matrix_to_bytes(w).hex())
print(excepted_key.hex())