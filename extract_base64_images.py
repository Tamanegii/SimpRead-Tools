import os
import re
import base64
from pathlib import Path

def clean_markdown_file(md_file_path):
    # Read the content of the markdown file
    with open(md_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Remove large blocks of empty lines before the last line
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)

    # Remove empty lines at the end of the file
    content = re.sub(r'\n\s*\n\s*$', '\n', content)

    # Write the cleaned content back to the markdown file
    with open(md_file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def extract_base64_images(md_file_path, output_folder):
    specific_folder = os.path.join(output_folder, Path(md_file_path).stem)
    os.makedirs(specific_folder, exist_ok=True)
    # Read the content of the markdown file
    with open(md_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Find all base64 encoded images in the markdown content
    base64_images = re.findall(r'\[img-(\d+)\]:data:image/(png|jpeg|jpg|webp|gif);base64,([A-Za-z0-9+/=]+)', content)

    # Replace base64 references with image file paths
    for index, (img_index, image_type, base64_str) in enumerate(base64_images):
        try:
            # Decode the base64 string
            image_data = base64.b64decode(base64_str)
            # Determine the correct extension based on the image type
            if image_type == "jpeg" or image_type == "jpg":
                extension = "jpg"
            elif image_type == "gif":
                extension = "gif"
            elif image_type == "png":
                extension = "png"
            elif image_type == "webp":
                extension = "webp"
            else:
                extension = "img"  # Fallback if an unknown type is encountered

            # Create an output file path
            output_file_name = f'{Path(md_file_path).stem}-{img_index}.{extension}'
            output_file_path = os.path.join(specific_folder, output_file_name)

            # Save the image data to the output file
            with open(output_file_path, 'wb') as image_file:
                image_file.write(image_data)
            
            print(f'Image saved to {output_file_path}')

            # Update markdown content references
            content = re.sub(r'\[img-' + img_index + r'\]:data:image/(png|jpeg|jpg|webp|gif);base64,[A-Za-z0-9+/=]+', '', content)
            replacement_path = f'![[{output_file_name}]]'
            content = re.sub(r'!\[\]\[img-' + img_index + r'\]', replacement_path, content)

        except Exception as e:
            print(f"Failed to process image {img_index} in {md_file_path}: {e}")

    # Write the updated content back to the markdown file
    with open(md_file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def process_markdown_files(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through all markdown files in the input folder
    for md_file in Path(input_folder).rglob('*.md'):
        extract_base64_images(md_file, output_folder)
        clean_markdown_file(md_file)

if __name__ == '__main__':
    input_folder = ''  # Replace with the path to your input folder
    output_folder = ''  # Replace with the path to your output folder
    process_markdown_files(input_folder, output_folder)
