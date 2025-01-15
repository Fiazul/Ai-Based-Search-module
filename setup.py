import subprocess


def run_script(script_name):
    try:
        subprocess.run(['python', script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
        exit(1)


if __name__ == "__main__":

    run_script('search.py')

    run_script('extract_image.py')

    run_script('extract_knowledgebase.py')

    run_script('embeddings.py')
