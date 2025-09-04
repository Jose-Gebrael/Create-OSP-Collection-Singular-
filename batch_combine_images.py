from PIL import Image, ImageDraw, ImageFont
import os
import glob
import json

def get_rarity_text(rarity_level):
    """Get the appropriate text for each rarity level"""
    rarity_texts = {
        '1_COMMON': ('HERO OF AFRICA', 'TURRET', 'MACHINE-GUNNER'),
        '2_RARE': ('HERO OF AFRICA', 'TURRET', 'MACHINE-GUNNER'),
        '3_LEGENDARY': ('HERO OF AFRICA', 'TURRET', 'MACHINE-GUNNER'),
        '4_EXOTIC': ('HERO OF AFRICA', 'TURRET', 'MACHINE-GUNNER'),
        '5_ULTRA-EXOTIC': ('HERO OF AFRICA', 'TURRET', 'MACHINE-GUNNER')
    }
    return rarity_texts.get(rarity_level, ('HERO OF AFRICA', 'TURRET', 'MACHINE-GUNNER'))

def get_folder_mapping():
    """Map rarity levels to border files and rarity names"""
    return {
        '1_COMMON': {
            'border': '1_common.png',
            'rarity': 'COMMON'
        },
        '2_RARE': {
            'border': '2_rare.png',
            'rarity': 'RARE'
        },
        '3_LEGENDARY': {
            'border': '3_legendary.png',
            'rarity': 'LEGENDARY'
        },
        '4_EXOTIC': {
            'border': '4_exotic.png',
            'rarity': 'EXOTIC'
        },
        '5_ULTRA-EXOTIC': {
            'border': '5_ultra-exotic.png',
            'rarity': 'ULTRA-EXOTIC'
        }
    }

def combine_single_image(character_path, border_path, output_path, font_path, texts):
    """Combine a single character image with border and text"""
    try:
        # Step 1: Load and resize character image to 850x850
        character_img = Image.open(character_path)
        character_resized = character_img.resize((850, 850), Image.Resampling.LANCZOS)
        
        # Step 2: Load border image
        border_img = Image.open(border_path)
        
        # Step 3: Create final image with proper layering
        canvas_size = 1024
        character_size = 850
        offset = (canvas_size - character_size) // 2  # 87px offset
        
        # Create transparent canvas
        final_img = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))
        
        # Paste character in center
        final_img.paste(character_resized, (offset, offset), character_resized if character_resized.mode == 'RGBA' else None)
        
        # Paste border on top
        final_img.paste(border_img, (0, 0), border_img if border_img.mode == 'RGBA' else None)
        
        # Step 4: Add text overlays
        draw = ImageDraw.Draw(final_img)
        text_color = 'white'
        
        # Text 1: "HERO OF AFRICA" - 34px, y=97
        font1 = ImageFont.truetype(font_path, 34)
        text1_bbox = draw.textbbox((0, 0), texts[0], font=font1)
        text1_width = text1_bbox[2] - text1_bbox[0]
        text1_height = text1_bbox[3] - text1_bbox[1]
        text1_x = (canvas_size - text1_width) // 2
        text1_y = 97 - text1_height // 2
        draw.text((text1_x, text1_y), texts[0], font=font1, fill=text_color)
        
        # Text 2: "TURRET" - 17px, y=857
        font2 = ImageFont.truetype(font_path, 17)
        text2_bbox = draw.textbbox((0, 0), texts[1], font=font2)
        text2_width = text2_bbox[2] - text2_bbox[0]
        text2_height = text2_bbox[3] - text2_bbox[1]
        text2_x = (canvas_size - text2_width) // 2
        text2_y = 857 - text2_height // 2
        draw.text((text2_x, text2_y), texts[1], font=font2, fill=text_color)
        
        # Text 3: "MACHINE-GUNNER" - 25px, y=915
        font3 = ImageFont.truetype(font_path, 25)
        text3_bbox = draw.textbbox((0, 0), texts[2], font=font3)
        text3_width = text3_bbox[2] - text3_bbox[0]
        text3_height = text3_bbox[3] - text3_bbox[1]
        text3_x = (canvas_size - text3_width) // 2
        text3_y = 915 - text3_height // 2
        draw.text((text3_x, text3_y), texts[2], font=font3, fill=text_color)
        
        # Step 5: Save the final image
        final_img.save(output_path, 'PNG')
        return True
        
    except Exception as e:
        print(f'❌ Error processing {os.path.basename(character_path)}: {e}')
        return False

def generate_metadata(template_path, token_id, rarity, metadata_output_path):
    """Generate metadata JSON file based on template"""
    try:
        # Load template
        with open(template_path, 'r') as f:
            template = json.load(f)
        
        # Update template with specific values
        template['name'] = f"HERO OF AFRICA #{token_id}"
        template['image'] = f"https://ipfs.io/ipfs/bafybeiehwh5dv3wnrn3te7h4sx7gmuzymsi5pzhmfapovyxb2laj2qxche/{token_id}.png"
        template['properties']['RARITY'] = rarity
        
        # Update attributes rarity
        for attr in template['attributes']:
            if attr['trait_type'] == 'RARITY':
                attr['value'] = rarity
        
        # Save metadata file
        with open(metadata_output_path, 'w') as f:
            json.dump(template, f, indent=4)
        
        return True
        
    except Exception as e:
        print(f'❌ Error generating metadata: {e}')
        return False

def batch_combine_images():
    """Process all images in IMAGES folders with corresponding borders"""
    try:
        # Define paths
        images_folder = './IMAGES'
        border_folder = './BORDER'
        output_images_folder = './Final/Images'
        output_metadata_folder = './Final/Metadata'
        font_path = './FONT/Generis.otf'
        template_path = './Template.json'
        
        print('🚀 Starting batch image processing...')
        print(f'Images source: {images_folder}')
        print(f'Borders source: {border_folder}')
        print(f'Output images: {output_images_folder}')
        print(f'Output metadata: {output_metadata_folder}')
        
        # Create output folders if they don't exist
        os.makedirs(output_images_folder, exist_ok=True)
        os.makedirs(output_metadata_folder, exist_ok=True)
        
        # Check if font exists
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font file not found: {font_path}")
        
        # Get folder mapping
        folder_mapping = get_folder_mapping()
        
        total_processed = 0
        total_success = 0
        global_counter = 0  # Global counter for sequential naming
        
        # Process each rarity level
        for rarity_level, config in folder_mapping.items():
            print(f'\n📁 Processing {rarity_level}...')
            
            # Define paths for this rarity level
            character_folder = os.path.join(images_folder, rarity_level)
            border_file = os.path.join(border_folder, config['border'])
            rarity_name = config['rarity']
            
            # Check if folders exist
            if not os.path.exists(character_folder):
                print(f'⚠️ Character folder not found: {character_folder}')
                continue
                
            if not os.path.exists(border_file):
                print(f'⚠️ Border file not found: {border_file}')
                continue
            
            # Get all PNG files in character folder
            character_files = glob.glob(os.path.join(character_folder, '*.png'))
            
            if not character_files:
                print(f'⚠️ No PNG files found in {character_folder}')
                continue
            
            print(f'Found {len(character_files)} images to process')
            
            # Get texts for this rarity level
            texts = get_rarity_text(rarity_level)
            
            # Process each character image
            success_count = 0
            for character_path in character_files:
                character_filename = os.path.basename(character_path)
                
                # Create sequential filename: 0.png, 1.png, 2.png, etc.
                image_filename = f'{global_counter}.png'
                metadata_filename = f'{global_counter}.json'
                
                image_output_path = os.path.join(output_images_folder, image_filename)
                metadata_output_path = os.path.join(output_metadata_folder, metadata_filename)
                
                print(f'Processing: {character_filename} → {global_counter} ({rarity_name})', end=' ... ')
                
                # Generate image
                image_success = combine_single_image(character_path, border_file, image_output_path, font_path, texts)
                
                # Generate metadata
                metadata_success = generate_metadata(template_path, global_counter, rarity_name, metadata_output_path)
                
                if image_success and metadata_success:
                    print('✅')
                    success_count += 1
                elif image_success and not metadata_success:
                    print('⚠️ (image ok, metadata failed)')
                    success_count += 1
                else:
                    print('❌')
                
                global_counter += 1  # Increment counter for next file
                total_processed += 1
            
            total_success += success_count
            print(f'✅ {rarity_level}: {success_count}/{len(character_files)} images processed successfully')
        
        print(f'\n🎉 Batch processing complete!')
        print(f'Total images processed: {total_processed}')
        print(f'Successfully processed: {total_success}')
        print(f'Failed: {total_processed - total_success}')
        
    except Exception as error:
        print(f'❌ Batch processing error: {error}')

if __name__ == '__main__':
    batch_combine_images()
