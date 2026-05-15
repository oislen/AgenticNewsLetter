import re
import os
import sys

# set file directories
base_dir = os.getcwd().split("AgenticNewsLetter")[0]
root_dir = os.path.join(base_dir, "AgenticNewsLetter")
newletter_dir = os.path.join(root_dir, "newletter")
# creds
creds_dir = os.path.join(root_dir, ".creds")
tavily_api_fpath = os.path.join(creds_dir, "tavily")
sender_email_username_fpath = os.path.join(creds_dir, "sender_email_username")
sender_email_password_fpath = os.path.join(creds_dir, "sender_email_pass")
receiver_email_username_fpath = os.path.join(creds_dir, "receiver_email_username")
# append file locations to path
for path in [base_dir, root_dir, newletter_dir, creds_dir]:
    sys.path.append(path)

# set test environment flag
localTestEnv = True

# set root file directories
root_dir_re_match = re.findall(string=os.getcwd(), pattern="^.+AgenticNewsLetter")
root_fdir = root_dir_re_match[0] if len(root_dir_re_match) > 0 else os.path.join(".", "AgenticNewsLetter")

creds_fdir = os.path.join(root_fdir, ".creds")
session_token_fpath = os.path.join(creds_fdir, 'sessionToken.json')