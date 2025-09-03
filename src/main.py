import os
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw

IMAGE_DIR = "data/raw/"
ANNOTATION_DIR = "data/annotated/"
OUTPUT_DIR = "data/processed/"

def parse_voc_xml(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        boxes = []
        for obj in root.findall('object'):
            bbox = obj.find('bndbox')
            xmin = int(bbox.find('xmin').text)
            ymin = int(bbox.find('ymin').text)
            xmax = int(bbox.find('xmax').text)
            ymax = int(bbox.find('ymax').text)
            boxes.append({'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax})
        
        return boxes
    except FileNotFoundError:
        print(f"Error: XML file not found at {xml_file}")
        return None
    except Exception as e:
        print(f"Error parsing XML file {xml_file}: {e}")
        return None

def draw_boxes_on_image(image_path, boxes, output_path):
    try:
        image = Image.open(image_path).convert("RGB")
        draw = ImageDraw.Draw(image)
        for box in boxes:
            draw.rectangle([(box['xmin'], box['ymin']), (box['xmax'], box['ymax'])], outline="red", width=3)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image.save(output_path)
        print(f"Annotated image saved to: {output_path}")

    except Exception as e:
        print(f"Error processing image {image_path}: {e}")

if __name__ == "__main__":
    image_files = [f for f in os.listdir(IMAGE_DIR) if f.endswith('.jpg')]
    
    if image_files:
        print(f"Found {len(image_files)} images to process.")
        
        for image_file in image_files:
            image_path = os.path.join(IMAGE_DIR, image_file)
            
            annotation_file = os.path.splitext(image_file)[0] + '.xml'
            annotation_path = os.path.join(ANNOTATION_DIR, annotation_file)
            
            if os.path.exists(annotation_path):
                print(f"Processing {image_file}...")
                
                boxes = parse_voc_xml(annotation_path)
                
                if boxes is not None:
                    output_image_path = os.path.join(OUTPUT_DIR, f"annotated_{image_file}")
                    draw_boxes_on_image(image_path, boxes, output_image_path)
                else:
                    print(f"Skipping {image_file} due to parsing error.")
            else:
                print(f"Annotation file not found for {image_file} at {annotation_path}")
    else:
        print("No images found in the raw data directory.")
