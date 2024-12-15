import argparse
import struct

def extract_strings(file_path, min_length=4):
    """
    Extract readable strings from a binary file.
    :param file_path: Path to the binary file
    :param min_length: Minimum length of strings to extract
    :return: List of readable strings
    """
    readable_chars = (
        b"".join([bytes([i]) for i in range(32, 127)]) + b"\n"
    )  # Printable ASCII + newline
    result = []

    with open(file_path, "rb") as file:
        current_string = b""
        while byte := file.read(1):
            if byte in readable_chars:
                current_string += byte
                if len(current_string) >= min_length:
                    result.append(current_string.decode("utf-8", errors="ignore"))
            else:
                current_string = b""
    return result

def parse_binary_file(file_path, struct_format):
    """
    Parse structured binary data from a file.
    :param file_path: Path to the binary file
    :param struct_format: Struct format string (e.g., "2I" for two unsigned integers)
    :return: List of parsed tuples
    """
    results = []
    struct_size = struct.calcsize(struct_format)

    with open(file_path, "rb") as file:
        while chunk := file.read(struct_size):
            if len(chunk) < struct_size:
                break  # Ignore incomplete chunks
            results.append(struct.unpack(struct_format, chunk))
    return results

def main():
    parser = argparse.ArgumentParser(description="Analyze .dat files for readable text and structured binary data.")
    parser.add_argument("file", help="Path to the .dat file")
    parser.add_argument("-s", "--strings", action="store_true", help="Extract readable strings")
    parser.add_argument("-b", "--binary", type=str, help="Parse binary file with struct format (e.g., '2I')")
    parser.add_argument("-l", "--length", type=int, default=4, help="Minimum string length (default: 4)")
    args = parser.parse_args()

    if args.strings:
        print("[*] Extracting readable strings...")
        strings = extract_strings(args.file, args.length)
        for string in strings:
            print(string)

    if args.binary:
        print(f"[*] Parsing binary file with struct format: {args.binary}")
        try:
            parsed_data = parse_binary_file(args.file, args.binary)
            for data in parsed_data:
                print(data)
        except struct.error as e:
            print(f"[!] Error parsing binary file: {e}")

    if not args.strings and not args.binary:
        print("[!] No analysis mode selected. Use --strings or --binary.")

if __name__ == "__main__":
    main()
