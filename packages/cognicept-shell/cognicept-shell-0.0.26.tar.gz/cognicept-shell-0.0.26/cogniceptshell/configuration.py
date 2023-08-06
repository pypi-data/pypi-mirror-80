# coding=utf8
# Copyright 2020 Cognicept Systems
# Author: Jakub Tomasek (jakub@cognicept.systems)
# --> Configuration class handles Cognicept configuration

from dotenv import dotenv_values
from pathlib import Path
from Crypto.PublicKey import RSA
import subprocess
import os
import sys
import re
import requests
import getpass
import jwt
import time



class Configuration:
    config_path = os.path.expanduser("~/.cognicept/")
    env_path = config_path + "runtime.env"
    _regex_key = r"^([_A-Z0-9]+)$"
    _config_loaded = False

    def load_config(object, path):
        object.config_path = os.path.expanduser(path)
        object.env_path = object.config_path + "runtime.env"
        file = Path(object.env_path)
        
        if ((not file.exists()) or (file.is_dir())):
            print("Configuration file `" + object.env_path + "` does not exist.")
            return False
        
        object.config = dotenv_values(file)

        if(len(object.config) == 0):
            print("Configuration file `" + object.env_path + "` is empty or could not be parsed.")
            return False

        object._config_loaded = True
        return True

    def configure(object, args):
        if(not object._config_loaded):
            return
        
        if (not os.access(object.env_path, os.W_OK)):
            print("Error: You don't have writing permissions for `" + object.env_path + "`. Run as `sudo` or change file permissions.")
            return
        if(args.read):
            for key, value in object.config.items():
                print(key + ': "' + value + '"')
        elif(args.add):
            new_key = ""
            while(new_key == ""):
                new_key = input("Config name: ")

                # if empty, exit
                if(new_key == ""):
                    return
                # check if matches key specs
                matches = re.match(object._regex_key, new_key)
                if matches is None:
                    print("Error: Key can be uppercase letters, digits, and the '_'. Try again.")
                    new_key = ""
            
            new_value = ""
            while(new_value == ""):
                new_value = input("Value: ")
                if(new_value == ""):
                    return
                matches = re.match(r"^.*[\"].*$", new_value)
                if matches is not None:
                    print("Error: Value cannot contain '\"'. Try again.")
                    new_value = ""

            object.config[new_key] = new_value
        elif(args.ssh):
            object.configure_ssh()
        else:
            for key, value in object.config.items():
                new_value = input(key + "[" + value + "]:")
                matches = re.match(r"^.*[\"].*$", new_value)
                if((new_value != "") and (matches == None)):
                    object.config[key] = new_value
        object.save_config()

    def save_config(object):
        try:
            with open(object.env_path, 'w') as file:
                for key, value in object.config.items():
                    file.write(key + '=' + value + '\n')
        except IOError:
            print("Could not write into `" + object.env_path + "`. Please check write permission or run with `sudo`.")
    
    def cognicept_login(object):
        print("Please enter your Cognicept credentials.")
        
        username = input("Username: ")
        try: 
            password = getpass.getpass() 
        except Exception as error: 
            print('Error when reading password.')
            return False
        
        try:
            resp = requests.post(object.get_cognicept_api_uri() + 'user/login', json = {"username": username, "password": password}, timeout = 5)
            if resp.status_code != 200:
                print('Login error: wrong credentials.')
                return False
            
            object.config["COGNICEPT_JWT"] = resp.json()["access_token"]            
        except requests.exceptions.Timeout:
            print("Cognicept REST API error: time out.")
            return
        except requests.exceptions.TooManyRedirects:
            print("Cognicept REST API error: Wrong endpoint.")
            return
        except:
            print("Cognicept REST API error")
            raise SystemExit()
        object.save_config()

        

        return True

    def get_cognicept_jwt(object):
        if "COGNICEPT_JWT" in object.config:
            # check expiration of the current token
            jwt_decoded = jwt.decode(object.config["COGNICEPT_JWT"], verify=False)
            if ( jwt_decoded["exp"] >  time.time()):
                # if not expired return token
                return object.config["COGNICEPT_JWT"]
            else:
                print("Cognicept login expired.")
        # try to login if token exists or expired
        if(object.cognicept_login()):
            return object.config["COGNICEPT_JWT"]
        else:
            # if all fails return empty string
            return ""

    def get_cognicept_api_uri(object):
        if "COGNICEPT_API_URI" in object.config:
            return object.config["COGNICEPT_API_URI"]
        else:
            return "https://dev.cognicept.systems/api/v1/"

    def interpret_bool_input(object,input_string):
        if(input_string == 'Y'):
            return True
        elif(input_string == 'n'):
            return False
        else:
            return None

    def configure_ssh(object):
        print('SSH is used to access the host machine from the isolated docker environment of `remote_intervention_agent`.')

        enable_ssh = None
        while(enable_ssh == None):
            enable_ssh = object.interpret_bool_input(input("Enable SSH access? (Y/n):"))

        if(not enable_ssh):
            object.config["COG_ENABLE_SSH"] = "False"
            object.config["COG_ENABLE_SSH_KEY_AUTH"] = "False"
            object.config["COG_ENABLE_AUTOMATIC_SSH"] = "False"
            object.save_config()
            return True
        else:
            object.config["COG_ENABLE_SSH"] = "True"

        ssh_authorized_keys_path = os.path.expanduser("~") + "/.ssh/authorized_keys" 
        print("\n \nSSH key needs to be used for hosts with disabled password login. "
        "It can also simplify access so you don't need to input the password each time.\n"
        "This process will generate ssh key locally and mount it to the docker container. "
        "The public key is copied to `" + ssh_authorized_keys_path + "` to give access.  Root access is needed and you will be prompted for password."
        "The ssh key is neither sent nor stored to the Cognicept server. "
        "If you choose not to, manual password ssh access can be still used.")

        enable_ssh_key = None
        while(enable_ssh_key == None):
            enable_ssh_key = object.interpret_bool_input(input("Generate SSH key and give access? (Y/n):"))

        if(not enable_ssh_key):
            object.config["COG_ENABLE_SSH_KEY_AUTH"] = "False"
            object.config["COG_ENABLE_AUTOMATIC_SSH"] = "False"
            object.save_config()
            return True
        else:
            object.config["COG_ENABLE_SSH_KEY_AUTH"] = "True"

        cognicet_ssh_directory = object.config_path + "ssh/"
        try:
            if not os.path.exists(cognicet_ssh_directory):
                os.makedirs(cognicet_ssh_directory)
        except:
            print("Failed. Don't have privileges to create files/directories within the ssh directory.")
            return False
        
        # generate the keys
        ssh_key = RSA.generate(2048)
        private_key_path = cognicet_ssh_directory + "id_rsa"
        public_key_path = cognicet_ssh_directory + "id_rsa.pub"
        config_file_path = cognicet_ssh_directory + "config"
        with open(private_key_path, 'wb') as content_file:
            os.chmod(private_key_path, 0o600)
            content_file.write(ssh_key.exportKey('PEM'))
        pub_key = ssh_key.publickey().exportKey('OpenSSH')
        with open(public_key_path, 'wb') as content_file:
            content_file.write(pub_key)
        # add new line at the end of the file
        with open(public_key_path, 'a') as content_file:
            content_file.write("\n")

        default_user = getpass.getuser()

        user_name = input("Name of the user to access ssh(if empty, defaults to `" + default_user + "`): ")
        if(user_name == ""):
            user_name = default_user
        object.config["COG_SSH_DEFAULT_USER"] = user_name

        authorized_keys_path = "/home/" + user_name + "/.ssh/authorized_keys"
        try:
            print('Root access is needed to modify `' + authorized_keys_path + '` and you will be prompted for password.')
            proc = subprocess.call(['sudo', 'sh', '-c', 'cat ' + public_key_path + ' >> ' + authorized_keys_path])
        except:
            print("Failed! Don't have access to " + authorized_keys_path)
            return


        enable_automatic_ssh = None
        while(enable_automatic_ssh == None):
            enable_automatic_ssh = object.interpret_bool_input(input("Enable automatic ssh access? (Y/n):"))
        
        if(not enable_automatic_ssh):
            object.config["COG_ENABLE_AUTOMATIC_SSH"] = "False"
        else:
            object.config["COG_ENABLE_AUTOMATIC_SSH"] = "True"
        
        object.save_config()
        print ('SSH config done. To apply changes restart agents using `cognicept restart`.')
        return True
