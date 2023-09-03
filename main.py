from line_parser import _process_line

def main():
    file_path = "./test.txt"
    
    symbols = [
        ('<->', '↔'),
        ('->', '→'),
        ('𝑎2', '@')
    ]
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    print(_process_line(lines[0]))
    # for line in lines:
    #     print(_process_line(line))

if __name__ == "__main__":
    main()