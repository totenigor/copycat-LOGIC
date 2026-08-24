from backend.security import encrypt_data, decrypt_data

slowo = "konwuj123"

cicho = encrypt_data(slowo)
print(f"cicho: {cicho}")

print(f"glosno: {decrypt_data(cicho)}")

