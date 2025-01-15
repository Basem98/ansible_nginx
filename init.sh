ansible-inventory -i ./inventories/nginx.yml --list
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i ./inventories/nginx.yml ./playbooks/ubuntu.yml --vault-id sudo_password@passwords/sudo_enc_pass.txt 
