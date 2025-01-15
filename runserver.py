import subprocess

if __name__ == "__main__":
    # Start the Uvicorn server with reload enabled
    try:
        subprocess.run(['uvicorn', 'search:app', '--reload'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Uvicorn server: {e}")
        exit(1)
