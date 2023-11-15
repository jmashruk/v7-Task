import os
import json
import shutil
import random
from PIL import Image

def is_image_valid(image_path):
    try:
        with Image.open(image_path) as img:
            img.verify()
        return True
    except:
        return False

def filter_images_with_annotations(images, annotations):
    annotated_image_ids = set(ann['image_id'] for ann in annotations)
    return [img for img in images if img['id'] in annotated_image_ids]

# Filter annotations
def filter_annotations(annotations, max_class_id=79):
    return [ann for ann in annotations if ann['category_id'] <= max_class_id]

# Folder structure
os.makedirs('./coco', exist_ok=True)  
os.makedirs('./coco/images', exist_ok=True)
os.makedirs('./coco/annotations', exist_ok=True)
os.makedirs('./coco/labels', exist_ok=True)

os.mkdir('./coco/images/train2017')
os.mkdir('./coco/images/val2017')
os.mkdir('./coco/images/test2017')

# Load annotations
with open('./instances_val2017.json') as f:
  coco = json.load(f)

# Split data
num_images = len(coco['images'])
random.shuffle(coco['images'])

train_size = int(0.7 * num_images)
val_size = int(0.2 * num_images)
test_size = num_images - train_size - val_size

train_images = coco['images'][:train_size]
val_images = coco['images'][train_size:train_size+val_size]
test_images = coco['images'][train_size+val_size:]

# Check for corrupted images and remove them
for img in list(train_images + val_images + test_images):
    image_path = f'images/{img["file_name"]}'
    if not is_image_valid(image_path):
        print(f"Removing corrupted image: {img['file_name']}")
        train_images = [i for i in train_images if i['id'] != img['id']]
        val_images = [i for i in val_images if i['id'] != img['id']]
        test_images = [i for i in test_images if i['id'] != img['id']]

# Filter out images without annotations
train_images = filter_images_with_annotations(train_images, coco['annotations'])
val_images = filter_images_with_annotations(val_images, coco['annotations'])
test_images = filter_images_with_annotations(test_images, coco['annotations'])

# Filter annotations with class id <= 79
train_anns = filter_annotations([ann for ann in coco['annotations'] if ann['image_id'] in [img['id'] for img in train_images]])
val_anns = filter_annotations([ann for ann in coco['annotations'] if ann['image_id'] in [img['id'] for img in val_images]])
test_anns = filter_annotations([ann for ann in coco['annotations'] if ann['image_id'] in [img['id'] for img in test_images]])

# Save annotations
with open('coco/annotations/instances_train2017.json', 'w') as f:
  json.dump({"info": coco["info"], "licenses": coco["licenses"], "images": train_images, "annotations": train_anns}, f)
  
with open('coco/annotations/instances_val2017.json', 'w') as f:
  json.dump({"info": coco["info"], "licenses": coco["licenses"], "images": val_images, "annotations": val_anns}, f)
  
with open('coco/annotations/instances_test2017.json', 'w') as f:
  json.dump({"info": coco["info"], "licenses": coco["licenses"], "images": test_images, "annotations": test_anns}, f)

def annotations_to_labels(anns, images, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # Create a dictionary to map image IDs to their dimensions
    img_dims = {img['id']: (img['width'], img['height']) for img in images}

    for ann in anns:
        img_id = ann['image_id']
        img_width, img_height = img_dims[img_id]

        # Normalize bbox coordinates
        x, y, w, h = ann['bbox']
        x_center = x + w / 2
        y_center = y + h / 2
        x_center /= img_width
        y_center /= img_height
        w /= img_width
        h /= img_height

        class_id = ann['category_id']

        label = f"{class_id} {x_center} {y_center} {w} {h}\n"
        file_name = str(img_id).zfill(12)

        out_path = os.path.join(output_dir, f"{file_name}.txt")
        with open(out_path, 'a') as f:
            f.write(label)

# Call the function with images included
annotations_to_labels(train_anns, train_images, 'coco/labels/train2017')
annotations_to_labels(val_anns, val_images, 'coco/labels/val2017')
annotations_to_labels(test_anns, test_images, 'coco/labels/test2017')

def copy_images(image_list, src_folder, dest_folder, output_file):
    paths = []
    for img in image_list:
        filename = img['file_name']
        shutil.copy(os.path.join(src_folder, filename), os.path.join('coco/',dest_folder, filename))
        paths.append(f'{dest_folder}/{filename}')

    with open(output_file, 'w') as f:
        f.writelines('\n'.join(paths))

# Copy images to their respective directories and create text files with image paths
copy_images(train_images, 'images', './images/train2017', 'coco/train2017.txt')
copy_images(val_images, 'images', './images/val2017', 'coco/val2017.txt')
copy_images(test_images, 'images', './images/test2017', 'coco/test-dev2017.txt')

print('Dataset preparation is complete.')

# Save annotations
# ... [rest of your existing code to save annotations and create labels]

# Copy images
# ... [rest of your existing code to copy images]

print('Done!')
