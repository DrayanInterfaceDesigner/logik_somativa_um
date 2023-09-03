from line_parser2 import _process_

def main():
    file_path = "./test.txt"
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    for line in lines:
        print("Original: ", line)
        print("Result: ", _process_(line))

if __name__ == "__main__":
    main()