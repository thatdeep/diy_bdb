import argparse
import json
import os
from cryptography.fernet import Fernet
from git import Repo

def load_key(file_path):
    with open(file_path, 'rb') as f:
        key = f.read()
    return key

def load_data(file_path, key):
    if not os.path.exists(file_path):
        return []

    cipher_suite = Fernet(key)
    with open(file_path, 'rb') as f:
        encrypted_data = f.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    data = json.loads(decrypted_data)
    return data

def save_data(file_path, data, key):
    cipher_suite = Fernet(key)
    data_str = json.dumps(data)
    encrypted_data = cipher_suite.encrypt(data_str.encode())
    with open(file_path, 'wb') as f:
        f.write(encrypted_data)

def commit_changes(repo_path, file_path, commit_message):
    repo = Repo(repo_path)
    repo.index.add([file_path])
    repo.index.commit(commit_message)
    origin = repo.remote(name='origin')
    origin.push()

# Parsing command-line arguments
#parser = argparse.ArgumentParser()
#parser.add_argument('key_file', type=str, help='Path to the file containing the encryption key')
#args = parser.parse_args()

# Load the key from the file
#key = load_key(args.key_file)

# Usage:
#data = load_data('workouts.json', key)

# Suppose you've collected new data for the day
#new_data = {
#    "date": "2023-08-01",
#    "workout": "Running",
#    "distance": 5,
#    "time": 30
#}

#data.append(new_data)  # append the new data to the existing data

#save_data('workouts.jsonc', data, key)
#commit_changes('/path/to/your/repo', 'workouts.json', 'Updated workout data')
