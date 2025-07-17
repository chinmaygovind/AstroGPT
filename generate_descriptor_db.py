import os
import cv2
import numpy as np
import json
from tqdm import tqdm

def get_image_paths(base_dir, limit=20):
    dso_dict = {}
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.bmp', '.gif')):
                rel_path = os.path.relpath(os.path.join(root, file), 'static')
                parts = rel_path.split(os.sep)
                if len(parts) >= 3:
                    dso_name = parts[1]
                else:
                    dso_name = 'misc'
                dso_dict.setdefault(dso_name, []).append(os.path.join('static', rel_path.replace('\\', '/')))
    # Only keep the first N images per DSO
    for k in dso_dict:
        dso_dict[k] = dso_dict[k][:limit]
    return dso_dict

def compute_orb_descriptors(image_path, max_dim=1024):
    # ORB only works on grayscale images, not color. We load color, but convert to grayscale for ORB.
    try:
        img_color = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if img_color is None:
            return None
        # No downsampling, use original size
        img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
        brisk = cv2.BRISK_create()
        kp, des = brisk.detectAndCompute(img_gray, None)
        if des is not None:
            return des.tolist()
        else:
            return None
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def build_dso_descriptor_db():
    images = get_image_paths('static/images')
    # Only process images, not graphs or queryimages
    skip_dsos = {'misc', 'master'}
    all_dsos = set(images.keys()) - skip_dsos
    dso_database = []
    for dso in tqdm(list(all_dsos), desc='Processing DSOs'):
        entry = {
            'name': dso,
            'images': []
        }
        # For each image, include the path and descriptors
        for img_path in tqdm(images.get(dso, []), desc=f'Images for {dso}', leave=False):
            des = compute_orb_descriptors(img_path)
            entry['images'].append({'path': img_path, 'descriptors': des})
        dso_database.append(entry)
    # Flatten the database for frontend use, each entry includes DSO name, type, path, and descriptors
    flat_db = []
    for entry in dso_database:
        dso_name = entry['name']
        for img in entry['images']:
            flat_db.append({'name': dso_name, 'type': 'image', 'path': img['path'], 'descriptors': img['descriptors']})
    return flat_db

if __name__ == '__main__':
    db = build_dso_descriptor_db()
    with open('static/dsoDescriptorDatabase.json', 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=1)
    print(f"Generated dsoDescriptorDatabase.json with {len(db)} entries.")