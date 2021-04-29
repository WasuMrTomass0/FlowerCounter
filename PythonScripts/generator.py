import os
import argparse

SUBSTRING = '<class_text_to_int>'


def check_file(file_path):
    if not os.path.isfile(file_path):
        raise Exception(f"File {file_path} not found!")
    pass


def read_lines_from_file(file_path):
    with open(file_path, 'r') as token:
        return token.readlines()
    pass
    
    
def read_from_file(file_path):
    with open(file_path, 'r') as token:
        return token.read()
    pass


def main(classes_path, template_path, g_tfrecord_dir, l_map_dir):
    # Check if files exist
    check_file(classes_path)
    check_file(template_path)
    # Read files
    classes = read_lines_from_file(classes_path)
    template = read_from_file(template_path)
    # Strip each line
    classes = [line.strip() for line in classes if line.strip()]
    if not classes:
        raise Exception(f"Classes file is empty!")

    # Generate function definition
    foo = "def class_text_to_int(row_label):\n"
    foo += f"    if row_label == '{classes[0]}':\n        return 1\n"
    elifs = [f"    elif row_label == '{classes[i]}':\n        return {i+1}\n" for i in range(1, len(classes))]
    foo += ''.join(elifs)
    foo += "    else:\n        return None\n"
    
    # Create generate_tfrecord.py
    gt_path = 'generate_tfrecord.py' if not g_tfrecord_dir else os.path.join(g_tfrecord_dir, 'generate_tfrecord.py')
    # Insert function
    text = template.replace(SUBSTRING, foo)
    # Save file
    with open(gt_path, 'w') as token:
        token.write(text) 
    print(f"Done generating {gt_path}.")
    
    # Create label map
    items = ["item {\n    id: " + str(i+1) + "\n    name: '" + str(classes[i]) + "'\n}\n" for i in range(len(classes))]
    text = ''.join(items)
    # Save file
    l_map_dir = 'label_map.pbtxt' if not l_map_dir else os.path.join(l_map_dir, 'label_map.pbtxt')
    with open(l_map_dir, 'w') as token:
        token.write(text) 
    print(f"Done generating {l_map_dir}.")
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate files from classes.txt. Files: 'generate_tfrecord.py'")
    
    parser.add_argument('-c', '--classes_path', type=str, required=True, help='Path to classes file')
    parser.add_argument('-t', '--template_path', type=str, required=True, help='Path to template file')
    
    parser.add_argument('-gt', '--generate_tfrecord_save_dir', type=str, required=False,
                        help='Directory to save generate_tfrecord.py')
    parser.add_argument('-lm', '--label_map_save_dir', type=str, required=False,
                        help='Directory to save label_map.pbtxt')
    
    args = parser.parse_args()
    main(args.classes_path, args.template_path, args.generate_tfrecord_save_dir, args.label_map_save_dir)
    pass
