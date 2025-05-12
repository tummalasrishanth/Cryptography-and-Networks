def int_to_bits(n, w): return [int(b) for b in format(n, f'0{w}b')]
def bits_to_int(b): return int("".join(map(str, b)), 2)
def perm(b, p): return [b[i] for i in p]
def xor(a, b): return [i^j for i,j in zip(a,b)]
def lshift(b, n): return b[n:] + b[:n]

S0 = [[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,3,2]]
S1 = [[0,1,2,3],[2,0,1,3],[3,0,1,0],[2,1,0,3]]
P10, P8 = [2,4,1,6,3,9,0,8,7,5], [5,2,6,3,7,4,9,8]
IP, IP_INV, EP, P4 = [1,5,2,0,3,7,4,6], [3,0,2,4,6,1,7,5], [3,0,1,2,1,2,3,0], [1,3,2,0]

def gen_keys(k):
    k = perm(int_to_bits(k,10), P10)
    l,r = lshift(k[:5],1), lshift(k[5:],1)
    k1 = perm(l+r, P8)
    l2,r2 = lshift(l,2), lshift(r,2)
    k2 = perm(l2+r2, P8)
    return k1,k2

def sbox(bits, s): r = (bits[0]<<1)|bits[3]; c = (bits[1]<<1)|bits[2]; return int_to_bits(s[r][c], 2)
def fk(bits, k): L,R = bits[:4], bits[4:]; t = xor(perm(R, EP), k); return xor(L, perm(sbox(t[:4],S0)+sbox(t[4:],S1), P4)) + R

def sdes_block(b, k, decrypt=False):
    k1, k2 = gen_keys(k)
    if decrypt: k1,k2 = k2,k1
    b = perm(int_to_bits(b,8), IP)
    b = fk(b,k1)
    b = b[4:] + b[:4]
    b = fk(b,k2)
    return bits_to_int(perm(b, IP_INV))

def ctr_mode(blocks, key, ctr_start=0):
    return [b ^ sdes_block((ctr_start+i)%256, key) for i,b in enumerate(blocks)]

# Test
pt = [0b00000001, 0b00000010, 0b00000100]
key = int("0111111101", 2)
expected = [0b00111000, 0b01001111, 0b00110010]

ct = ctr_mode(pt, key, 0)
dt = ctr_mode(ct, key, 0)

print("Ciphertext: ", [f"{b:08b}" for b in ct])
print("Expected:   ", [f"{b:08b}" for b in expected])
print("Decrypted:  ", [f"{b:08b}" for b in dt])
