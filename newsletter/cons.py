import re
import os

# set root file directories
root_dir_re_match = re.findall(string=os.getcwd(), pattern="^.+AgenticNewsLetter")
root_fdir = root_dir_re_match[0] if len(root_dir_re_match) > 0 else os.path.join(".", "AgenticNewsLetter")

creds_fdir = os.path.join(root_fdir, ".creds")
session_token_fpath = os.path.join(creds_fdir, 'sessionToken.json')