from Crypto.PublicKey import RSA
from Crypto.Util.number import isPrime, long_to_bytes

class LCG:
    lcg_m = 99470802153294399618017402366955844921383026244330401927153381788409087864090915476376417542092444282980114205684938728578475547514901286372129860608477
    lcg_c = 3910539794193409979886870049869456815685040868312878537393070815966881265118275755165613835833103526090552456472867019296386475520134783987251699999776365
    lcg_n = 8311271273016946265169120092240227882013893131681882078655426814178920681968884651437107918874328518499850252591810409558783335118823692585959490215446923

    def __init__(self, lcg_s):
        self.state = lcg_s

    def next(self):
        self.state = (self.state * self.lcg_m + self.lcg_c) % self.lcg_n
        return self.state

if __name__ == '__main__':

    # Find prime value of specified bits a specified amount of times
    seed = 211286818345627549183608678726370412218029639873054513839005340650674982169404937862395980568550063504804783328450267566224937880641772833325018028629959635
    lcg = LCG(seed)
    primes_arr = []
    
    dump = True
    items = 0
    # dump_file = open("dump.txt", "w")

    primes_n = 1
    while True:
        for i in range(8):
            while True:
                prime_candidate = lcg.next()
                if dump:
                    # dump_file.write(str(prime_candidate) + '\n')
                    items += 1
                    if items == 6:
                        dump = False
                        # dump_file.close()
                if not isPrime(prime_candidate):
                    continue
                elif prime_candidate.bit_length() != 512:
                    continue
                else:
                    primes_n *= prime_candidate
                    primes_arr.append(prime_candidate)
                    break
        
        # Check bit length
        if primes_n.bit_length() > 4096:
            print("bit length", primes_n.bit_length())
            primes_arr.clear()
            primes_n = 1
            continue
        else:
            break
    print(primes_arr)
    # Create public key 'n'
    n = 1
    for j in primes_arr:
        n *= j
    print("[+] Public Key: ", n)
    print("[+] size: ", n.bit_length(), "bits")

    # Calculate totient 'Phi(n)'
    phi = 1
    for k in primes_arr:
        phi *= (k - 1)

    # Calculate private key 'd'
    d = pow(0x010001, -1, phi)
    with open ("flag.txt", "rb") as flag_file:
        _enc = flag_file.read()
        _enc = int.from_bytes(_enc, "little")
        _dec = pow(_enc, d, n)
        print(long_to_bytes(_dec))
        # flag_file.write(_enc.to_bytes(n.bit_length(), "little"))


    # Generate Flag
    # assert config.flag.startswith(b"CTF{")
    # assert config.flag.endswith(b"}")
    # enc_flag = bytes_to_long(config.flag)
    # assert enc_flag < n

    # Encrypt Flag
    # _enc = pow(enc_flag, 0x010001, n)

    # with open ("flag.txt", "wb") as flag_file:
    #     flag_file.write(_enc.to_bytes(n.bit_length(), "little"))

    # # Export RSA Key
    # rsa = RSA.construct((n, 0x010001))
    # with open ("public.pem", "w") as pub_file:
    #     pub_file.write(rsa.exportKey().decode())