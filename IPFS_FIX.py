import os
import json
import glob


def update_ipfs_cid():
    """Update IPFS CID in all JSON metadata files"""

    # ⚠️ CHANGE THIS TO YOUR NEW IPFS CID ⚠️ (there is another place you also need to change below)
    NEW_CID = "bafybeicsminwcuv2wptbwsgxpdbe5zpd3xgoh6ozdq5gvxrvf2m67tido4"  # Replace with your actual CID

    # Define paths
    metadata_folder = "./Shuffled/Metadata"

    print("🚀 Starting IPFS CID update...")
    print(f"Metadata folder: {metadata_folder}")
    print(f"New CID: {NEW_CID}")

    # Check if metadata folder exists
    if not os.path.exists(metadata_folder):
        print(f"❌ Metadata folder not found: {metadata_folder}")
        return

    # Get all JSON files in metadata folder
    json_files = glob.glob(os.path.join(metadata_folder, "*.json"))

    if not json_files:
        print(f"⚠️ No JSON files found in {metadata_folder}")
        return

    print(f"Found {len(json_files)} JSON files to update")

    success_count = 0
    error_count = 0

    # Process each JSON file
    for json_file_path in json_files:
        filename = os.path.basename(json_file_path)

        try:
            # Load JSON file
            with open(json_file_path, "r") as f:
                metadata = json.load(f)

            # Check if image field exists
            if "image" not in metadata:
                print(f"⚠️ No image field in {filename}")
                continue

            # Extract the current image URL
            current_image_url = metadata["image"]

            # Check if it's an IPFS URL
            if "ipfs.io/ipfs/" not in current_image_url:
                print(f"⚠️ Not an IPFS URL in {filename}: {current_image_url}")
                continue

            # Extract the filename part (e.g., "0.png", "1.png", etc.)
            # Split by '/' and get the last part
            url_parts = current_image_url.split("/")
            image_filename = url_parts[-1]  # Gets "0.png", "1.png", etc.

            # Create new URL with new CID
            new_image_url = f"https://ipfs.io/ipfs/{NEW_CID}/{image_filename}"

            # Update the metadata
            old_url = metadata["image"]
            metadata["image"] = new_image_url

            # Save the updated JSON file
            with open(json_file_path, "w") as f:
                json.dump(metadata, f, indent=4)

            print(f"✅ Updated {filename}: {image_filename}")
            success_count += 1

        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error in {filename}: {e}")
            error_count += 1
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
            error_count += 1

    print(f"\n🎉 IPFS CID update complete!")
    print(f"Successfully updated: {success_count} files")
    print(f"Errors: {error_count} files")
    print(f"Total processed: {len(json_files)} files")

    if success_count > 0:
        print(f"\n✅ All image URLs now use CID: {NEW_CID}")


def preview_changes():
    """Preview what changes will be made without actually updating files"""

    # ⚠️ CHANGE THIS TO YOUR NEW IPFS CID ⚠️
    NEW_CID = "bafybeicsminwcuv2wptbwsgxpdbe5zpd3xgoh6ozdq5gvxrvf2m67tido4"  # Replace with your actual CID

    metadata_folder = "./Shuffled/Metadata"

    print("👀 PREVIEW MODE - No files will be changed")
    print(f"New CID: {NEW_CID}")

    # Get first few JSON files for preview
    json_files = glob.glob(os.path.join(metadata_folder, "*.json"))[
        :5
    ]  # Show first 5 files

    for json_file_path in json_files:
        filename = os.path.basename(json_file_path)

        try:
            with open(json_file_path, "r") as f:
                metadata = json.load(f)

            if "image" in metadata:
                current_url = metadata["image"]
                url_parts = current_url.split("/")
                image_filename = url_parts[-1]
                new_url = f"https://ipfs.io/ipfs/{NEW_CID}/{image_filename}"

                print(f"\n📄 {filename}:")
                print(f"  OLD: {current_url}")
                print(f"  NEW: {new_url}")

        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")


if __name__ == "__main__":
    print("IPFS CID Updater")
    print("================")
    print()
    print("⚠️ IMPORTANT: Update the NEW_CID variable in this script before running!")
    print()

    choice = input(
        "Choose option:\n1. Preview changes (recommended first)\n2. Update all files\n\nEnter choice (1 or 2): "
    )

    if choice == "1":
        preview_changes()
    elif choice == "2":
        confirm = input("\n⚠️ This will modify all JSON files. Are you sure? (yes/no): ")
        if confirm.lower() == "yes":
            update_ipfs_cid()
        else:
            print("Operation cancelled.")
    else:
        print("Invalid choice. Exiting.")
