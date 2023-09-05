from line_parser2 import _process_

def main():
    file_path = "./test.txt"
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    for line in lines:
        print("Original: ", line)
        print("\nResult: ", _process_(line), "\n")

if __name__ == "__main__":
    main()