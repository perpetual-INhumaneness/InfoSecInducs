import os
import zipfile

def identify_file_type_by_magic_bytes(file_path):
    """
    Identify the file type based on magic bytes, including differentiating ZIP and Office files.
    """
    MAGIC_BYTES = {
        b"\xFF\xD8\xFF": "JPEG Image",
        b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A": "PNG Image",
        b"\x25\x50\x44\x46": "PDF Document",
        b"\x50\x4B\x03\x04": "ZIP Archive",
        b"\x47\x49\x46\x38": "GIF Image",
        b"\x42\x4D": "BMP Image",
        b"\x49\x49\x2A\x00": "TIFF Image (Little Endian)",
        b"\x4D\x4D\x00\x2A": "TIFF Image (Big Endian)",
        b"\x1F\x8B": "GZIP Archive",
    }

    try:
        with open(file_path, "rb") as file:
            file_header = file.read(16)  # Read the first 16 bytes

            # Match against known magic byte signatures
            for signature, file_type in MAGIC_BYTES.items():
                if file_header.startswith(signature):
                    # Special case: Check ZIP archives for specific file types
                    if file_type == "ZIP Archive":
                        with zipfile.ZipFile(file_path, "r") as zip_file:
                            # Check for specific internal structure for Office files
                            if "[Content_Types].xml" in zip_file.namelist():
                                if any(name.startswith("ppt/") for name in zip_file.namelist()):
                                    return "PowerPoint Presentation (PPTX)"
                                elif any(name.startswith("word/") for name in zip_file.namelist()):
                                    return "Word Document (DOCX)"
                                elif any(name.startswith("xl/") for name in zip_file.namelist()):
                                    return "Excel Spreadsheet (XLSX)"
                        return "ZIP Archive"  # Default if no Office structure found
                    return file_type

        # Attempt to check if the file is a plain text file
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            content = file.read(1024)  # Read the first 1 KB of the file
            if all(c.isprintable() or c in '\r\n\t' for c in content):
                return "Plain Text File"

        return "Unknown file type (Magic bytes not matched)"
    except Exception as e:
        return f"Error reading file: {str(e)}"

def analyze_files_in_folder(folder_path):
    """
    Analyze all files in the folder and identify their types.
    """
    if not os.path.isdir(folder_path):
        return "Invalid folder path."

    file_types = {}
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):  # Only process files
            file_type = identify_file_type_by_magic_bytes(file_path)
            file_types[file_name] = file_type

    return file_types

def hex_dump(file_path, num_bytes=64):
    """
    Generate a HEX dump of the file's content.
    :param file_path: Path to the file
    :param num_bytes: Number of bytes to preview
    :return: HEX dump as a string
    """
    print(f"Previewing file: {file_path}")
    print("\n--- HEX Dump (First 64 Bytes) ---")

    try:
        with open(file_path, "rb") as file:
            content = file.read(num_bytes)  # Read the specified number of bytes
        hex_lines = []
        for i in range(0, len(content), 16):  # Process 16 bytes per line
            chunk = content[i:i + 16]
            hex_part = " ".join(f"{byte:02X}" for byte in chunk)
            ascii_part = "".join(chr(byte) if 32 <= byte <= 126 else "." for byte in chunk)
            hex_lines.append(f"{i:08X}  {hex_part:<48}  {ascii_part}")
        return "\n".join(hex_lines)
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"Error: {str(e)}"

def preview_and_analyze_file(folder_path):
    """
    Generate a preview (HEX dump) and analyze the file header.
    :param file_path: Path to the file
    """
    
    if not os.path.isdir(folder_path):
        print("Invalid folder path.")
        return
    
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        print(hex_dump(file_path, num_bytes=64))
    
    return

def extract_unicode_text(folder_path):
    """
    Extracts readable Unicode text from a file.
    Includes basic multilingual plane (BMP) characters.
    """
    if not os.path.isdir(folder_path):
        print("Invalid folder path.")
        return
    
    readable_text = []
    try:
        with open(folder_path, 'rb') as file:
            chunk_size = 1024
            while chunk := file.read(chunk_size):
                print("working")
                
                for byte in chunk:
                    try:
                        char = chr(byte)
                        # Retain characters in the printable range and BMP Unicode range
                        if char.isprintable():
                            readable_text.append(char)
                    except ValueError:
                        continue  # Skip invalid byte sequences
        
        return ''.join(readable_text)

    except Exception as e:
        return f"Error while reading the file: {e}"
    

def generate_report(folder_path, output_path):

    if not os.path.isdir(folder_path):
        print("Invalid folder path.")
        return
        
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):  # Only process files
            file_type = identify_file_type_by_magic_bytes(file_path)
        with open(output_path, "a") as report_file:
            report_file.write(" \n")
            report_file.write(f"***********************\n")
            report_file.write(f"File: {file_path}\n")
            report_file.write(f"File Type: {file_type}\n")
            report_file.write(f"Extracted text: {folder_path}\n")
            report_file.write("Analysis Results:\n")
            report_file.write(f"{hex_dump(file_path, num_bytes=64)}\n")
            report_file.write("\nEnd of Report")
    return

