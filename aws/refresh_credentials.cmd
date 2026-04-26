:: user settings
set user_dir=C:\Users\OisinLeonard\Documents\DSProjects\AgenticNewsLetter\.creds
set ubuntu_dir=/home/config
set session_fname=sessionToken.json

:: generate session token
call aws sts get-session-token > %user_dir%\%session_fname%