import os
import shutil
import glob

def remove_json_extensions():
    """Copy JSON files from Shuffled/Metadata to Shuffled/NoJson and remove .json extensions"""
    
    # Define paths
    source_folder = "./Shuffled/Metadata"
    destination_folder = "./Shuffled/NoJson"
    
    print("🗂️ Starting JSON extension removal...")
    print(f"Source folder: {source_folder}")
    print(f"Destination folder: {destination_folder}")
    
    # Check if source folder exists
    if not os.path.exists(source_folder):
        print(f"❌ Source folder not found: {source_folder}")
        return
    
    # Create destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)
    print(f"✅ Created/verified destination folder: {destination_folder}")
    
    # Get all JSON files from source folder
    json_files = glob.glob(os.path.join(source_folder, "*.json"))
    
    if not json_files:
        print(f"⚠️ No JSON files found in {source_folder}")
        return
    
    print(f"Found {len(json_files)} JSON files to process")
    
    success_count = 0
    error_count = 0
    
    # Process each JSON file
    for json_file_path in json_files:
        try:
            # Get original filename (e.g., "0.json", "1.json", etc.)
            original_filename = os.path.basename(json_file_path)
            
            # Remove .json extension (e.g., "0.json" -> "0")
            filename_without_extension = os.path.splitext(original_filename)[0]
            
            # Create destination path
            destination_path = os.path.join(destination_folder, filename_without_extension)
            
            # Copy file to destination without extension
            shutil.copy2(json_file_path, destination_path)
            
            print(f"✅ {original_filename} → {filename_without_extension}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Error processing {os.path.basename(json_file_path)}: {e}")
            error_count += 1
    
    print(f"\n🎉 JSON extension removal complete!")
    print(f"Successfully processed: {success_count} files")
    print(f"Errors: {error_count} files")
    print(f"Total files found: {len(json_files)} files")
    
    if success_count > 0:
        print(f"\n✅ Files copied to: {destination_folder}")
        print("📝 Files now have no extension (e.g., '0', '1', '2', etc.)")

def preview_operation():
    """Preview what files will be copied and renamed"""
    
    source_folder = "./Shuffled/Metadata"
    destination_folder = "./Shuffled/NoJson"
    
    print("👀 PREVIEW MODE - No files will be copied")
    print(f"Source: {source_folder}")
    print(f"Destination: {destination_folder}")
    
    # Get sample of JSON files
    json_files = glob.glob(os.path.join(source_folder, "*.json"))
    
    if not json_files:
        print(f"⚠️ No JSON files found in {source_folder}")
        return
    
    # Show first 10 files for preview
    sample_files = json_files[:10]
    
    print(f"\nSample operations (first 10 of {len(json_files)} files):")
    print("Source → Destination")
    print("===================")
    
    for json_file_path in sample_files:
        original_filename = os.path.basename(json_file_path)
        filename_without_extension = os.path.splitext(original_filename)[0]
        
        print(f"{original_filename} → {filename_without_extension}")
    
    if len(json_files) > 10:
        print(f"... and {len(json_files) - 10} more files")
    
    print(f"\nTotal files to process: {len(json_files)}")

def clear_destination():
    """Clear the NoJson folder before running"""
    
    destination_folder = "./Shuffled/NoJson"
    
    if os.path.exists(destination_folder):
        files = glob.glob(os.path.join(destination_folder, "*"))
        if files:
            print(f"🧹 Clearing {len(files)} files from {destination_folder}")
            for file in files:
                try:
                    os.remove(file)
                    print(f"🗑️ Removed: {os.path.basename(file)}")
                except Exception as e:
                    print(f"⚠️ Could not remove {file}: {e}")
            print("✅ Folder cleared")
        else:
            print(f"📁 {destination_folder} is already empty")
    else:
        print(f"📁 {destination_folder} does not exist (will be created when needed)")

def verify_files():
    """Verify that files were copied correctly"""
    
    source_folder = "./Shuffled/Metadata"
    destination_folder = "./Shuffled/NoJson"
    
    print("🔍 Verifying copied files...")
    
    if not os.path.exists(destination_folder):
        print(f"❌ Destination folder not found: {destination_folder}")
        return
    
    # Get source and destination files
    source_files = glob.glob(os.path.join(source_folder, "*.json"))
    destination_files = glob.glob(os.path.join(destination_folder, "*"))
    
    print(f"Source files: {len(source_files)}")
    print(f"Destination files: {len(destination_files)}")
    
    if len(source_files) == len(destination_files):
        print("✅ File count matches!")
    else:
        print("⚠️ File count mismatch!")
    
    # Check a few sample files
    sample_count = min(5, len(source_files))
    print(f"\nVerifying first {sample_count} files:")
    
    for i in range(sample_count):
        source_path = source_files[i]
        source_name = os.path.basename(source_path)
        expected_dest_name = os.path.splitext(source_name)[0]
        expected_dest_path = os.path.join(destination_folder, expected_dest_name)
        
        if os.path.exists(expected_dest_path):
            # Compare file sizes
            source_size = os.path.getsize(source_path)
            dest_size = os.path.getsize(expected_dest_path)
            
            if source_size == dest_size:
                print(f"✅ {source_name} → {expected_dest_name} (size: {source_size} bytes)")
            else:
                print(f"⚠️ {source_name} → {expected_dest_name} (size mismatch: {source_size} vs {dest_size})")
        else:
            print(f"❌ Missing: {expected_dest_name}")

if __name__ == "__main__":
    print("JSON Extension Remover")
    print("=====================")
    print()
    
    choice = input(
        "Choose option:\n"
        "1. Preview operation (recommended first)\n"
        "2. Clear destination folder\n"
        "3. Remove extensions and copy files\n"
        "4. Verify copied files\n"
        "\nEnter choice (1, 2, 3, or 4): "
    )
    
    if choice == "1":
        preview_operation()
    elif choice == "2":
        clear_destination()
    elif choice == "3":
        confirm = input(
            f"\n⚠️ This will copy all JSON files to Shuffled/NoJson without extensions. Continue? (yes/no): "
        )
        if confirm.lower() == "yes":
            remove_json_extensions()
        else:
            print("Operation cancelled.")
    elif choice == "4":
        verify_files()
    else:
        print("Invalid choice. Exiting.")
