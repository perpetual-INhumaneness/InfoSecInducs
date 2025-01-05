import fileOperations

#folder_path = input("Enter the folder path: ")
#Select and enter the number of the function you want to perform
#1- file type
#2- hexdump
#3- report generation
#4- text extraction
option = int(input('Enter a number: '))
folder_path = r"C:\Users\keert\OneDrive\Desktop\FileAnalysisTool\data"
output_path =r"C:\Users\keert\OneDrive\Desktop\FileAnalysisTool\reports\report.txt"

if option == 1:
    file_types = fileOperations.analyze_files_in_folder(folder_path)
    if isinstance(file_types, dict):
        for file_name, file_type in file_types.items():
            print(f"{file_name}: {file_type}")
    else:
        print(file_types)
elif option == 2:
    fileOperations.preview_and_analyze_file(folder_path)

elif option == 3:
    fileOperations.generate_report(folder_path, output_path)

elif option == 4:
    fileOperations.extract_unicode_text(folder_path)

else:
    print("Invalid Option") 
