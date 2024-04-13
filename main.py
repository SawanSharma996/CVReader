import zipfile

# Specify the path to the ZIP file
zip_file_path = '/Users/sawansharma/Desktop/code/CVReader/CVReader/input.zip'

# Create a ZipFile object
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    # Get a list of all file names in the ZIP file
    file_list = zip_ref.namelist()

    
    
        