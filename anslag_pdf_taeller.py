import PyPDF2

# script til at tælle anslag i en pdf-fil
def pdf_anslag(pdf_path, startside, slutside):
    """
    Denne funktion tager tre argumenter:
    pdf_path = stien til pdf filen
    startside = den side du gerne vil starte fra
    slutside = den side du gerne vil slutte med at tælle.
    """
    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file) # læser pdf

            text= ""

            # indlæser sidetalet
            for page_number in range(startside - 1, slutside):
                if page_number < len(reader.pages):
                    page_text = ""

                    try:
                        page_text = reader.pages[page_number].extract_text() or ""
                        if page_text.strip():
                            text += page_text
                        else:
                            print(f"Side {page_number + 1} indeholder ikke tekst")
                    except Exception as e:
                        print(f"Kunne ikke læse side {page_number + 1}. Fejl {e}")
                else: 
                    print(f"Sidetall {page_number + 1} findes ikke")
            
            character_count = len(text)

            return character_count
    
    except FileNotFoundError:
        print(f"Fejl: pdf-fil ikke fundet på denne sti")
        return None
    except Exception as e:
        print(f"Der er sket en fejl: {e}")
        return None

if __name__ == "__main__":
    pdf_path = r"C:\Users\joha4\OneDrive\Skrivebord_LapTop\Bachelorprojekt\Python\Rapport_til_geolab.pdf"
    try:
        startside = int(input("Indtast startside: ")) # brugerindtastning
        slutside = int(input("Indtast slutside: ")) # brugerindtastning

        if startside <= 0 or slutside <= 0:
            print(f"Startside og slutside skal være større end 0")
        elif startside > slutside:
            print("Startsiden skal være  mindre el lig md slutside")
        else:
            character_count = pdf_anslag(pdf_path, startside, slutside)

            if character_count is not None:
                antal_sider = character_count / 2400
                print("-------------------------------------------------------------------")
                print(f"Antal anslag i PDF fra side {startside} til {slutside} er: {character_count}")
                print(f"Antallet af sider (afrundet): {antal_sider:.2f} normalsider")
                print("-------------------------------------------------------------------")
    except ValueError:
        print("Fejl: Indtast gyldige heltal for start- og slutsider.")

                
