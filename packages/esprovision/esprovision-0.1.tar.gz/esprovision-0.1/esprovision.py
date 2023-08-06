#!/usr/bin/python3

import click
from jinja2 import Template
from pathlib import Path
import os
import glob
import time
from shutil import copyfile


@click.command()
@click.argument('start', type=int)
@click.argument('instances', type=int)
@click.argument('yaml_template', type=click.Path(exists=True))
@click.argument('tuya_files_dir', type=click.Path(exists=True))
@click.argument('secrets', type=click.Path(exists=True))
def provision(secrets, start, instances, yaml_template, tuya_files_dir):
    """
    Device Start No. | No. Devices Desired | Template Path | Tuya 'Files' Directory

    This script requires esphome and tuya-convert to be installed.

    EXPECTS: Jinja Template using '{{device_number}}'

    ----------------------------------------------------------

    This tool Uses a Jinja2 ('.j2') file that is a direct copy of 
    a esphome yaml file to generate multiple iterated files. It 
    then copies the binaries to tuya-convert for flashing.


    """

    # Load yaml template file as jinja2 template
    with open(yaml_template) as file:
        template = Template(file.read())

    # Set instance counters
    gen_instances = instances
    flash_instances = instances

    # Creating output directory in template parent directory
    parent, template_name = Path(
        yaml_template).parent, Path(yaml_template).stem
    output_dir = f'{parent}/{template_name}_output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    os.system(f'cp {secrets} {output_dir}/secrets.yaml')

    # Loop through all required instances, generating all required yaml files, compile
    for device_number in range(start, start+instances):
        # Create data dict
        data = {
            "device_number": f'{device_number}',
        }
        with open(f'{output_dir}/output.yaml', 'w') as file:
            file.write(template.render(data))

        os.system(f'esphome {output_dir}/output.yaml compile')

    # Loop Copy firmware.bin to tuya files directory and run tuya-convert, then delete bin
    # file from Tuya files directory
    for device_number in range(start, start+instances):
        # Copy file to tuya files directory
        targfn = glob.glob(
            f'{output_dir}/*_{device_number}/.pioenvs/*/firmware.bin')[0]
        dest = f'{tuya_files_dir}/output_{device_number}.bin'
        copyfile(targfn, dest)

        # Run Tuya-convert
        flash_script = f'.{Path(tuya_files_dir).parent}/start_flash.sh'
        os.system(flash_script)

        # Proceed through tuya-convert as normal, using the output_#.bin file on the
        # Desired device

        # Cleanup
        os.system(f'{tuya_files_dir}/output_{device_number}.bin')
        print(f'Make sure to mark device with Device: {device_number}')
        time.sleep(3)


if __name__ == '__main__':
    provision()
