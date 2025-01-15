# Ansible Task

## Objective
Automate the setup of an Nginx web server using ansible.

## Requirements:
Write a playbook to:
1. Install Nginx on a target server.
2. Configure a virtual host
3. Deploy an index.html file to /var/www/html.
4. Enable and start the Nginx service.
5. Use roles to separate tasks.
6. Test with both an inventory file and dynamic inventory

## Implementation Steps:
1. Installed ansible on node.
2. Wrote an inventory and tested it.
3. Wrote a playbook with a ping task within.
4. Refactored the playbook by writing a role called `nginx` and using it in the playbook instead of hardcoding the task within the playbook.
5. used a shell script file within the ansible.builtin.script plugin but figured out there are problems with that such as that this is not the best pracice and it also doesn't terminat after successful execution and doesn't provide useful logs output.
6. Refactored the `install_nginx` task to be a list of separate tasks, each task is a shell command using the ansible.builtin.apt plugin or the ansible.builtin.shell plugin.
7. Used the become: true, become_method: sudo, and the ansible_become_password var to run escalated commands without waiting for user interaction.
8. Refactored the playbook and inventory to use an encrypted password by using ansible vault.
9. Configured nginx on remote host bu changing the default listening port from 80 as it was used my the tcp service on the remote host by default.
10. Refactored tasks by using variables and string interpolation
11. Refactored playbook and inventory to use vault to store sensitive passwords
12. Wrote a python script to automate the vault encryption process and prepare the startup command to make it easier for anyone testing this.


## How to start:
1. Clone this repository on the control node with ansible installed.
2. Get into the folder:
    ```sh 
        cd ansible_nginx
    ```
3. Execute the python automation script to prepare password
    ```sh
    python3 ./encrypt_by_vault.py --var sudo_password --original-pass <password_to_sudo_managed_node> --encrypt-pass <any_password>
    ```
    Note: The managed node currently is hardcoded into the `nginx.yml` inventory file, but this could be changed using a dynamic inventory.
4. Execute the generated shell script
    ```sh
    sh ./init.sh
    ```

## What's missing to practice:
1. Use a dynamic inventory
2. Access the web server by a local domain name instead of 0.0.0.0:8080
