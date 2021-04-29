import glob
import os.path
import argparse
from typing import Tuple
from WasuLib.xml_image import XMLImage
from WasuLib.trace import Trace

NO_CHANGE = 0
LOWER_CASE = 1
UPPER_CASE = 2
TITLE = 3


def correct_labels(directory: str, shape: Tuple[int, int], old_label: str, new_label: str, del_label: str,
                   change_type: int):
    if change_type == LOWER_CASE:
        change_function = str.lower
    elif change_type == UPPER_CASE:
        change_function = str.upper
    elif change_type == TITLE:
        change_function = str.title
    else:
        change_function = str

    switch_labels = bool(old_label) and bool(new_label)
    delete_label_flag = bool(del_label)
    any_change = switch_labels or (change_function is not str) or delete_label_flag

    if not any_change:
        Trace(f"\nNo change needed.\n", Trace.TRACE_INFO, __file__, correct_labels.__name__)
        return

    old_label = old_label.lower()
    del_label = del_label.lower()

    xml_paths = glob.glob(os.path.join(directory, '*.xml'))
    for xml_path in xml_paths:
        # Read
        xml_obj = XMLImage(xml_path=xml_path)
        # Edit
        index = -1
        for box in xml_obj.boxes_classes:
            index += 1
            # Delete label
            if delete_label_flag and box.label.lower() == del_label:
                xml_obj.boxes_classes.pop(index)
                continue

            # Switch label
            if switch_labels and box.label.lower() == old_label:
                box.label = new_label

            # Correct label
            box.label = change_function(box.label).strip()
            pass  # for box
        # Save
        xml_obj.save()
        pass  # for xml_path
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Correct xml files")
    parser.add_argument('-d', '--directory', type=str, required=True, help='Directory containing the images')

    parser.add_argument('-old', '--old', type=str, required=False, default="", help='Replaced class name')
    parser.add_argument('-new', '--new', type=str, required=False, default="", help='Inserted class name')

    parser.add_argument('-del', '--delete', type=str, required=False, default="", help='Delete class name')

    parser.add_argument('--shape', type=int, nargs=2, required=False, metavar=('width', 'height'),
                        default=(0, 0), help='Minimal bounding box dimensions')

    parser.add_argument('-lower_case', action='store_true', help='Change labels to lower case')
    parser.add_argument('-upper_case', action='store_true', help='Change labels to upper case')
    parser.add_argument('-title', action='store_true', help='Change labels to title')

    args = parser.parse_args()

    if args.lower_case:
        label_operation = LOWER_CASE
    elif args.upper_case:
        label_operation = UPPER_CASE
    elif args.title:
        label_operation = TITLE
    else:
        label_operation = NO_CHANGE

    print(f"Before:")
    command = f"python count_sizes.py -d {args.directory}"
    os.system(command)
    print(f" - " * 20)
    correct_labels(
        directory=args.directory,
        shape=args.shape,
        old_label=args.old,
        new_label=args.new,
        del_label=args.delete,
        change_type=label_operation
    )

    print(f"After:")
    command = f"python count_sizes.py -d {args.directory}"
    os.system(command)
    print(f" - " * 20)

    pass
