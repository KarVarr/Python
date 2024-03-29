import easyocr
import re

def text_recognition(file_path):
    reader = easyocr.Reader(['en'])
    text = reader.readtext(file_path, detail=0,paragraph=True, allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", blocklist="/|")
    text_string = '\n'.join(text)
    print("Считанный текст:", text_string)
    pattern = r"([A-Z]{2})(\d{7})(\d{3})(\w{3})"
    matches = re.findall(pattern, text_string)
    # combined_string = ''.join(matches[0])

    # cleaned_string = ''.join(filter(str.isdigit, combined_string))
    # cleaned_string = cleaned_string[:10 ]
    # return cleaned_string
    if matches and len(matches) > 0:  
        combined_string = ''.join(matches[0])
        cleaned_string = ''.join(filter(str.isdigit, combined_string))
        cleaned_string = cleaned_string[:10]
        return cleaned_string
    else:
        return "Штрихкод не распознан!" 

def main():
    file_path = input("Enter a file path: ")
    print(text_recognition(file_path=file_path))

if __name__ == "__main__":
    main()


