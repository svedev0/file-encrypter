import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Generate encryption key
def generate_key():
	return os.urandom(32) # 256-bit key

# Encrypt file using AES encryption
def encrypt_file(key, in_filename, chunksize=64*1024):
	out_filename = in_filename + '.encrypted'

	iv = os.urandom(16)
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
	encryptor = cipher.encryptor()

	with open(in_filename, 'rb') as infile:
		with open(out_filename, 'wb') as outfile:
			outfile.write(iv)

			# Add padding to data before encryption
			padder = padding.PKCS7(algorithms.AES.block_size).padder()
			while True:
				chunk = infile.read(chunksize)
				if not chunk:
					break

				padded_chunk = padder.update(chunk)
				padded_chunk += padder.finalize()
				outfile.write(encryptor.update(padded_chunk))

			outfile.write(encryptor.finalize())

# Decrypt file using AES decryption
def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
	if not out_filename:
		out_filename = os.path.splitext(in_filename)[0]

	with open(in_filename, 'rb') as infile:
		iv = infile.read(16)
		cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
		decryptor = cipher.decryptor()

		with open(out_filename, 'wb') as outfile:
			# Remove padding from decrypted data
			unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
			while True:
				chunk = infile.read(chunksize)
				if not chunk:
					break

				unpadded_chunk = decryptor.update(chunk)
				unpadded_chunk += decryptor.finalize()
				unpadded_chunk = unpadder.update(unpadded_chunk)
				unpadded_chunk += unpadder.finalize()

				outfile.write(unpadded_chunk)

'''
To decrypt a file with an encryption key, replace the
decryption_key with your key and only run the decrypt_file()
function.
'''
encryption_key = generate_key()
print(f"Encryption Key: {encryption_key}")

'''
Only run either the encrypt_file() or decrypt_file() function
at any time. Save the encryption key is a secure place!
'''
encrypt_file(encryption_key, 'file.txt')
decrypt_file(encryption_key, 'file.txt.encrypted')
