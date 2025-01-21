import PyPDF2

def pdf_anslag(pdf_path, startside, slutside):
    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)

            text= ""

            # indlæser sidetalet
            for page_number in range(startside - 1, slutside):
                if page_number < len(reader.pages):
                    text += reader.pages[page_number].extract_text() or ""
                else:
                    print(f"Advarsel: Sidetallet {page_number + 1} findes ikk i PDF")
            
            # 
            character_count = len(text)

            return character_count
    
    except Exception as e:
        print(f" Der er sket en fejl: {e}")
        return None
    

if __name__ == "__main__":
    pdf_path = r""
    try: 
        startside = int(input("indtast startside: "))
        slutside = int(input("indtast slutside: "))

        character_count = pdf_anslag(pdf_path, startside, slutside)

        if character_count is not None:
            print("-------------------------------------------------------------------")
            print(f"Antal anslag i Pdf fra side {startside} til {slutside} er: {character_count}")
            print("-------------------------------------------------------------------")
    except ValueError:
        print(f"indtast korrekte sidetal")
