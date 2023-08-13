from zipfile import ZipFile

def create_zip():
    """
    A simple tool that creates a zip file from a file
    """
    # Path to the XML file
    xml_file_path = 'outputs/output.xml'
    
    # Path to the zip archive
    zip_file_path = 'output.zip'

    # Create a zip archive
    with ZipFile(f"outputs/{zip_file_path}", 'w') as zip_file:
        # Add the XML file to the archive
        zip_file.write(xml_file_path, arcname='output.xml')