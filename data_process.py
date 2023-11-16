import os
import shutil
import subprocess

def generate_data(datasets_dir):
    for subdir in os.listdir(datasets_dir):
        subdir_path = os.path.join(datasets_dir, subdir)

        if os.path.isdir(subdir_path):
            script_path = os.path.join(subdir_path, 'make_dataset.py')

            if os.path.isfile(script_path):

                try:
                    subprocess.run(['python', script_path], check=True)
                    print(f"Success make_dataset.py in {subdir_path}")
                except:
                    print(f"Fail make_dataset.py in {subdir_path}")
            else:
                print(f"*******No make_dataset.py in {subdir_path}*******")



if __name__=="__main__":
    datasets_dir = 'datasets'
    generate_data(datasets_dir)