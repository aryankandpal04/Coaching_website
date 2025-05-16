import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename, allowed_extensions):
    """
    Check if the file extension is allowed
    
    Args:
        filename (str): The name of the file
        allowed_extensions (set): Set of allowed file extensions
        
    Returns:
        bool: True if the file extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_file(file, upload_folder, allowed_extensions=None):
    """
    Save a file to the specified upload folder with a unique filename
    
    Args:
        file: The file to save
        upload_folder (str): The folder to save the file in
        allowed_extensions (set, optional): Set of allowed file extensions
        
    Returns:
        tuple: (success, filename or error message)
    """
    if not file:
        return False, "No file provided"
    
    if allowed_extensions and not allowed_file(file.filename, allowed_extensions):
        return False, "File type not allowed"
    
    # Create a unique filename
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    
    # Ensure the upload folder exists
    os.makedirs(upload_folder, exist_ok=True)
    
    # Save the file
    file_path = os.path.join(upload_folder, unique_filename)
    file.save(file_path)
    
    return True, unique_filename

def get_file_path(filename, upload_folder):
    """
    Get the full path of a file
    
    Args:
        filename (str): The name of the file
        upload_folder (str): The folder where the file is stored
        
    Returns:
        str: The full path of the file
    """
    return os.path.join(upload_folder, filename)

def delete_file(filename, upload_folder):
    """
    Delete a file from the specified upload folder
    
    Args:
        filename (str): The name of the file
        upload_folder (str): The folder where the file is stored
        
    Returns:
        bool: True if the file was deleted, False otherwise
    """
    try:
        file_path = get_file_path(filename, upload_folder)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        current_app.logger.error(f"Error deleting file: {str(e)}")
        return False 