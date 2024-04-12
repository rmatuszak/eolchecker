def generate_mixed_eol_file() -> None:
    with open("mixed_eols", "wb+") as file:
        for i in range(1,10):
            if i % 2 != 0:
                print("LF line ending!")
                file.write(b"LF line ending!\n")
            else:
                print("CRLF line ending!")
                file.write(b"CRLF line ending!\r\n")
        file.close()

def generate_exact_eols(eol: str) -> None:
    with open(f"{eol}_eols", "wb+") as file:
        for _ in range(1,10):
            print(f"{eol} line ending!")
            file.write(b"Line to save with LF!\n") if eol == "lf" else file.write(b"Line to save with CRLF!\r\n")
        file.close()

def view_eol_file(filename: str) -> None:
    with open(filename,"rb+") as file:
        for idx,l in enumerate(file.readlines()):
            print(f"{idx}: {l}")


# print("MIXED EOL GENERATION")
# generate_mixed_eol_file()

# print("EXACT EOL GENERATION - crlf")
# generate_exact_eols("crlf")

# eol="lf"
# print("EXACT EOL GENERATION - lf")
# generate_exact_eols("lf")

print("TESTING MIXED")
view_eol_file('mixed_eols')

# print("TESTING EXACT - crlf")
# view_eol_file("crlf_eols")

# print("TESTING EXACT - lf")
# view_eol_file("lf_eols")
