import argparse
import subprocess
import os
''' A python sript to automate the generation of a variable encrypted by ansible-vault then generates ansible startup script and runs it '''
def encrypt_string(variable_name, original_pass, encryption_pass):
    # Ensure the output directories exist
    passwords_dir = os.path.join(os.getcwd(), "passwords")
    os.makedirs(passwords_dir, exist_ok=True)

    password_file_name = f"{passwords_dir}/{variable_name}.txt"

    with open(password_file_name, 'w') as file:
        file.write(encryption_pass)

    vault_command = [
            "ansible-vault", "encrypt_string",
            f"--vault-id", f"{variable_name}@{password_file_name}",
            original_pass,
            f"--name", variable_name
            ]

    result = subprocess.run(vault_command, capture_output=True, text=True)
    try:
        if result.returncode == 0:
            # Create output vars dir if it doesn't exist
            out_vars_dir = os.path.join(os.getcwd(), "vars")
            os.makedirs(out_vars_dir, exist_ok=True)
    
            # Append to main.yml in the output_vars_folder

            vars_file = os.path.join(out_vars_dir, "main.yml")
            with open(vars_file, 'a') as file:
                file.write(result.stdout)

            print(f"Encryption successful. Output written to {password_file_name} and appended to {vars_file}")
        else:
            raise Exception(f"Encryption err: {result.stderr}")

        # Generate startup script for ansible playbook
        inventory_verify_cmd = ["ansible-inventory", "-i", "/inventories/nginx.yml", "--list"]
        inventory_verification_result = subprocess.run(inventory_verify_cmd, capture_output=True, text=True)
        if inventory_verification_result.returncode != 0:
            raise Exception(f"Inventory file error: {inventory_verification_result.stderr}")
        
        playbook_exec_cmd = [
                "ANSIBLE_HOST_KEY_CHECKING=False",
                "ansible-playbook",
                "-i", "./inventories/nginx.yml",
                "./playbooks/ubuntu.yml", 
                "--vault-id", f"{variable_name}@{password_file_name}"
        ]
    
        with open("init.sh", "w") as file:
            file.write(" ".join(playbook_exec_cmd))

    except Exception as e:
        print("Something went wrong:")
        print(e)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encrypt a string using ansible-vault.")
    parser.add_argument("--var", required=True, help="The variable name.")
    parser.add_argument("--original-pass", required=True, help="The original password.")
    parser.add_argument("--encrypt-pass", required=True, help="The password used to encrypt/decrypt.")

    args = parser.parse_args()
    encrypt_string(args.var, args.original_pass, args.encrypt_pass)

