import os
import json
import glob
import shutil
import random

def shuffle_files():
    """Randomly shuffle and rename all images and metadata files"""
    
    # Define paths
    source_images_folder = "./Final/Images"
    source_metadata_folder = "./Final/Metadata"
    output_images_folder = "./Shuffled/Images"
    output_metadata_folder = "./Shuffled/Metadata"
    
    print('🔀 Starting file shuffling...')
    print(f'Source images: {source_images_folder}')
    print(f'Source metadata: {source_metadata_folder}')
    print(f'Output images: {output_images_folder}')
    print(f'Output metadata: {output_metadata_folder}')
    
    # Check if source folders exist
    if not os.path.exists(source_images_folder):
        print(f'❌ Source images folder not found: {source_images_folder}')
        return
    
    if not os.path.exists(source_metadata_folder):
        print(f'❌ Source metadata folder not found: {source_metadata_folder}')
        return
    
    # Create output folders if they don't exist
    os.makedirs(output_images_folder, exist_ok=True)
    os.makedirs(output_metadata_folder, exist_ok=True)
    
    # Get all PNG files from source images folder
    image_files = glob.glob(os.path.join(source_images_folder, '*.png'))
    
    if not image_files:
        print(f'⚠️ No PNG files found in {source_images_folder}')
        return
    
    print(f'Found {len(image_files)} image files to shuffle')
    
    # Extract file numbers and create pairs
    file_pairs = []
    missing_metadata = []
    
    for image_path in image_files:
        # Get filename without extension (e.g., "0" from "0.png")
        image_filename = os.path.basename(image_path)
        file_number = os.path.splitext(image_filename)[0]
        
        # Check if corresponding metadata file exists
        metadata_filename = f'{file_number}.json'
        metadata_path = os.path.join(source_metadata_folder, metadata_filename)
        
        if os.path.exists(metadata_path):
            file_pairs.append({
                'number': file_number,
                'image_path': image_path,
                'metadata_path': metadata_path
            })
        else:
            missing_metadata.append(file_number)
    
    if missing_metadata:
        print(f'⚠️ Warning: {len(missing_metadata)} image files have no corresponding metadata:')
        for num in missing_metadata[:10]:  # Show first 10
            print(f'   - {num}.png (missing {num}.json)')
        if len(missing_metadata) > 10:
            print(f'   ... and {len(missing_metadata) - 10} more')
    
    print(f'Found {len(file_pairs)} complete image-metadata pairs')
    
    if len(file_pairs) == 0:
        print('❌ No complete pairs found. Cannot proceed.')
        return
    
    # Create shuffled order (0 to n-1)
    new_order = list(range(len(file_pairs)))
    random.shuffle(new_order)
    
    print('🔀 Shuffling files...')
    
    success_count = 0
    error_count = 0
    
    # Process each pair in the new shuffled order
    for new_index, old_pair in enumerate(file_pairs):
        try:
            # Get the shuffled position for this file
            shuffled_position = new_order[new_index]
            
            # New filenames
            new_image_filename = f'{shuffled_position}.png'
            new_metadata_filename = f'{shuffled_position}.json'
            
            # Output paths
            new_image_path = os.path.join(output_images_folder, new_image_filename)
            new_metadata_path = os.path.join(output_metadata_folder, new_metadata_filename)
            
            # Copy image file
            shutil.copy2(old_pair['image_path'], new_image_path)
            
            # Load, update, and save metadata file
            with open(old_pair['metadata_path'], 'r') as f:
                metadata = json.load(f)
            
            # Update metadata to reflect new number
            old_number = old_pair['number']
            metadata['name'] = f"HERO OF AFRICA #{shuffled_position}"
            
            # Update image URL if it exists and contains a number
            if 'image' in metadata:
                old_image_url = metadata['image']
                # Replace the old number with new number in the URL
                # Find the last occurrence of the old number followed by .png
                if f'/{old_number}.png' in old_image_url:
                    metadata['image'] = old_image_url.replace(f'/{old_number}.png', f'/{shuffled_position}.png')
            
            # Save updated metadata
            with open(new_metadata_path, 'w') as f:
                json.dump(metadata, f, indent=4)
            
            print(f'✅ {old_number} → {shuffled_position}')
            success_count += 1
            
        except Exception as e:
            print(f'❌ Error processing pair {old_pair["number"]}: {e}')
            error_count += 1
    
    print(f'\n🎉 Shuffling complete!')
    print(f'Successfully shuffled: {success_count} pairs')
    print(f'Errors: {error_count} pairs')
    print(f'Total files processed: {success_count * 2} files')  # images + metadata
    
    if success_count > 0:
        print(f'\n✅ Shuffled files saved to:')
        print(f'   Images: {output_images_folder}')
        print(f'   Metadata: {output_metadata_folder}')

def preview_shuffle():
    """Preview what the shuffle will look like without actually moving files"""
    
    source_images_folder = "./Final/Images"
    source_metadata_folder = "./Final/Metadata"
    
    print('👀 PREVIEW MODE - No files will be moved')
    
    # Get sample of files
    image_files = glob.glob(os.path.join(source_images_folder, '*.png'))
    
    if not image_files:
        print(f'⚠️ No PNG files found in {source_images_folder}')
        return
    
    # Take first 10 files for preview
    sample_files = image_files[:10]
    file_numbers = [os.path.splitext(os.path.basename(f))[0] for f in sample_files]
    
    # Create a sample shuffle
    shuffled_numbers = file_numbers.copy()
    random.shuffle(shuffled_numbers)
    
    print(f'\nSample shuffle (first 10 files):')
    print('Original → Shuffled')
    print('==================')
    
    for i, (original, shuffled) in enumerate(zip(file_numbers, shuffled_numbers)):
        print(f'{original}.png → {i}.png')
        print(f'{original}.json → {i}.json')
        print()
    
    print(f'Total files to shuffle: {len(image_files)}')

def clear_shuffled_folders():
    """Clear the shuffled folders before running"""
    
    folders_to_clear = ["./Shuffled/Images", "./Shuffled/Metadata"]
    
    for folder in folders_to_clear:
        if os.path.exists(folder):
            files = glob.glob(os.path.join(folder, '*'))
            if files:
                print(f'🧹 Clearing {len(files)} files from {folder}')
                for file in files:
                    try:
                        os.remove(file)
                    except Exception as e:
                        print(f'⚠️ Could not remove {file}: {e}')
            else:
                print(f'📁 {folder} is already empty')
        else:
            print(f'📁 {folder} does not exist (will be created)')

if __name__ == '__main__':
    print('File Order Shuffler')
    print('===================')
    print()
    
    choice = input('Choose option:\n1. Preview shuffle (recommended first)\n2. Clear shuffled folders\n3. Shuffle files\n\nEnter choice (1, 2, or 3): ')
    
    if choice == '1':
        preview_shuffle()
    elif choice == '2':
        clear_shuffled_folders()
    elif choice == '3':
        confirm = input('\n⚠️ This will copy and rename all files to Shuffled folders. Continue? (yes/no): ')
        if confirm.lower() == 'yes':
            shuffle_files()
        else:
            print('Operation cancelled.')
    else:
        print('Invalid choice. Exiting.')
