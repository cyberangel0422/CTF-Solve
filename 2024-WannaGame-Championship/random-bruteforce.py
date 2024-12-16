import random

chex="0203e2c0dd20182bea1d00f41b25ad314740c3b239a32755bab1b3ca1a98f0127f1a1aeefa15a418e9b03ad25b3a92a46c0f5a6f41cb580f7d8a3325c76e66b937baea"
ci=bytes.fromhex(chex)
l=len(ci)

for s in range(10001):
    random.seed(s)
    ks=bytearray([0]*l)
    for _ in range(1337):
        r=[random.randint(0, 255) for __ in range(l)]
        for i in range(l):
            ks[i]^=r[i]

    flag=bytes([c^k for c, k in zip(ci, ks)])
    if(flag.startswith(b"W1")):
        print(flag.decode("utf-8"))

#W1{maybe_the_seed_is_too_small..._b32fe938a402c22144b9d6497fd5a709}
