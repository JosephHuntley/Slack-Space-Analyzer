import json
import re

def clean_hex_string(hex_string, file_desc):
    # Strip spaces and remove invalid hex characters (non 0-9, A-F)
    clean_string = re.sub(r'[^0-9A-Fa-f]', '', hex_string)
    
    # Log warning if the cleaned hex string is not an even length (invalid hex)
    if len(clean_string) % 2 != 0:
        print(f"Warning: Hex string for {file_desc} is not valid: {hex_string}")
    return clean_string

def load_signatures_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        signatures = data.get('filesigs', [])
        
        signature_dict = {}
        for sig in signatures:
            file_desc = sig.get("File description")
            header_hex = sig.get("Header (hex)", "")
            file_ext = sig.get("File extension")
            
            # Clean the hex string before conversion
            clean_header_hex = clean_hex_string(header_hex, file_desc)

            try:
                if clean_header_hex and file_ext:
                    # Convert cleaned hex string to bytes
                    header_bytes = bytes.fromhex(clean_header_hex)
                    signature_dict[file_ext] = {
                        'header': header_bytes,
                        'description': file_desc
                    }
            except ValueError as e:
                # Log the error for invalid hex conversion
                print(f"Error converting hex for {file_desc}: {e}")
                
        return signature_dict

def check_file_signature(file_header, signatures_dict):
    for file_ext, sig_info in signatures_dict.items():
        header = sig_info['header']
        if file_header.startswith(header):
            return file_ext, sig_info['description']
    return "Unknown", "No description available"

# Load the file signatures
signatures_dict = load_signatures_from_json('file_sigs.json')

