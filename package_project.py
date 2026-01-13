import zipfile
import os

def package_project():
    output_filename = "spotify-playlist-creator.zip"
    
    # Files and directories to include
    include_files = [
        "app.py",
        "requirements.txt",
        "README.md",
        ".env.example",
        ".gitignore"
    ]
    
    include_dirs = [
        "execution"
    ]
    
    print(f"Creating {output_filename}...")
    
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add individual files
        for file in include_files:
            if os.path.exists(file):
                print(f"Adding {file}")
                zipf.write(file, arcname=file)
            else:
                print(f"Warning: {file} not found")
                
        # Add directories
        for directory in include_dirs:
            if os.path.exists(directory):
                print(f"Adding directory {directory}")
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        if not file.endswith('.pyc') and '__pycache__' not in root:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, '.')
                            print(f"  Adding {file_path}")
                            zipf.write(file_path, arcname=arcname)
    
    print("Done!")

if __name__ == "__main__":
    package_project()
