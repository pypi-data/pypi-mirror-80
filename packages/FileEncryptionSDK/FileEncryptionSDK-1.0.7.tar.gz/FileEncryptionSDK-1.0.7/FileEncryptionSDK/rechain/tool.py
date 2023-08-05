import hashlib
import rechain.Base58

def generate_address(public_key):
    assert isinstance(public_key, bytes)

    #print('0x04 + x + y:', ''.join(['{:02X}'.format(i) for i in s]))
    hasher = hashlib.sha256()
    hasher.update(public_key)
    r = hasher.digest()
    #print('SHA256(0x04 + x + y):', ''.join(['{:02X}'.format(i) for i in r]))

    hasher = hashlib.new('ripemd160')
    hasher.update(r)
    r = hasher.digest()   
    #print('RIPEMD160(SHA256(0x04 + x + y)):', ''.join(['{:02X}'.format(i) for i in r]))
    
    # Since '1' is a zero byte, it won't be present in the output address
    return '1' + base58_check(r, version=0)

def base58_check(src, version=0):
    src = bytes([version]) + src
    
    hasher = hashlib.sha256()
    hasher.update(src)
    r = hasher.digest()
    #print('SHA256(0x00 + r):', ''.join(['{:02X}'.format(i) for i in r]))

    hasher = hashlib.sha256()
    hasher.update(r)
    r = hasher.digest()
    #print('SHA256(SHA256(0x00 + r)):', ''.join(['{:02X}'.format(i) for i in r]))
    
    checksum = r[:4]
    s = src + checksum
    #print('src + checksum:', ''.join(['{:02X}'.format(i) for i in s]))
    
    return Base58.encode(int.from_bytes(s, 'big'))