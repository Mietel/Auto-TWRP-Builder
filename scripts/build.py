from twrpdtgen.device_tree import DeviceTree
import argparse
import os
from pathlib import Path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Auto-Twrp-Builder")
    parser.add_argument('-i', '--input', required=True, help='Recovery/Boot Image')
    parser.add_argument('-o', '--output', required=True, help='Output path')
    args = parser.parse_args()
    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()
    if not input_path.is_file():
        parser.error(f'input image does not exist: {input_path}')
    output_path.mkdir(parents=True, exist_ok=True)
    device_tree = DeviceTree(input_path)
    if os.getenv('GITHUB_OUTPUT', ''):
        with open(os.getenv('GITHUB_OUTPUT', ''), 'w') as f:
            f.write(f'DEVICE_NAME={device_tree.device_info.manufacturer}\n')
            f.write(f'PRODUCT_NAME={device_tree.device_info.codename}\n')
            f.write(f'MAKEFILE_NAME=twrp_{device_tree.device_info.codename}\n')
            f.write(
                f'DEVICE_PATH={os.path.basename(args.output) + os.sep + device_tree.device_info.manufacturer + os.sep + device_tree.device_info.codename}\n')
    device_tree.dump_to_folder(output_path)
    generated_bp = output_path / device_tree.device_info.manufacturer / device_tree.device_info.codename / 'Android.bp'
    if not generated_bp.is_file():
        raise FileNotFoundError(f'twrpdtgen did not generate {generated_bp}')
    with generated_bp.open('r') as f:
        print(f.read())
