# SOAP RATP
# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Path file .env-----------------
path_origin = str(os.path.abspath(sys.argv[0]))[1:].split('/')
#print("path_origin = ", path_origin, type(path_origin))
path_base = '/' + '/'.join(path_origin[0:(path_origin.index('RATP') + 1)])
#print("path_base = ", path_base, type(path_base))

path_env = path_base + '/.env'
#print("path_env = ", path_env, type(path_env))
load_dotenv(dotenv_path=path_env)

path_import = path_base + '/class_python'
#print("path_import = ", path_import, type(path_import))
sys.path.insert(0, path_import)

from class_soap_ratp import soapRATP
# Config Soap--------------------------------
soap_config = {
    'wsdl': os.getenv("wsdl_file")
}

soap_ratp = soapRATP(soap_config, path_base)


if __name__ == "__main__":
    print('main')
