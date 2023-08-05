import sys
import os
import comtypes.client
import click
from pyfiglet import Figlet
from PyInquirer import prompt, Separator
from ppt2pdf.utils import createCheckBoxes
from ppt2pdf.main import convert

@click.group()
def cli():
    """
    Convert the PPT files to PDF 
    """
    f = Figlet(font='cybermedium')
    click.echo(click.style(f.renderText('PPT => PDF'), fg="red"))


@cli.command(name="file")
@click.argument("input_file", required=True,type=click.Path(exists=True, resolve_path=True),nargs=1)
@click.option("-o","--output", "output", type=click.Path(resolve_path=True))
def convertfile(input_file,output):
    """
    To convert a single PPT or PPTX file
    """
    click.echo("Your Input file is at:")
    click.echo(input_file)
    convert(input_file,output)
    click.echo("Done !!!");


@cli.command(name="dir")
@click.argument("input_folder", required=True,type=click.Path(exists=True, resolve_path=True), nargs=1)
@click.option("-o","--output","output",type=click.Path(dir_okay=True, resolve_path=True), nargs=1, help="Output Folder default current folder")
@click.option("-s","--select",is_flag=True, help="Recursively Select Files")
def converdir(input_folder,output,select):
    """
    To convert multiple files in a directory 
    """
    input_folder += "\\"
    if(not output):
        output=input_folder
    else:
        output += "\\"
    #%% Get files in input folder
    input_file_paths = os.listdir(input_folder)
    filtered_files = []

    for file in input_file_paths:
        # Skip if file does not contain a power point extension
        if  file.lower().endswith((".ppt", ".pptx")):
            filtered_files.append(file)

    if(select):
        user_choices = [
            {
                'type': 'checkbox',
                'qmark': '?',
                'message': 'Select the files you want to Convert',
                'name': 'convert',
                'choices':createCheckBoxes(filtered_files)
            }
        ]
        selected_files = prompt(user_choices)
        convert_files = selected_files['convert']
    else:
        convert_files = filtered_files
    #%% Convert each file
    with click.progressbar(convert_files,label="Status", show_pos=True) as bar:
        for input_file_name in bar:
            # # Create input file path
            input_file_path = os.path.join(input_folder, input_file_name)
            file_name = os.path.splitext(input_file_name)[0]
            output_file_path = os.path.join(output, file_name + ".pdf")
            convert(input_file_path,output_file_path)
    click.echo("Done !!!")
