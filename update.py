import sys
import os
import shutil
import subprocess


def del_if(file_path):
	try:
		if not os.path.isfile(file_path) or not os.path.islink(file_path): 
			print(f"File {file_path} does not exist.")
			return
			
		
		print(f"Deleted file: {file_path}")		
		os.remove(file_path)
	except Exception as e:
		print(f"Error deleting file {file_path}: {e}")
		
def rmdir_if(folder_path):
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} does not exist.")
        return
    
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
                print(f"Deleted file: {item_path}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Deleted folder: {item_path}")
        except Exception as e:
            print(f"Error deleting {item_path}: {e}")

def mkdir_if(folder_path):	
	if not os.path.exists(folder_path):
		os.makedirs(folder_path)

def clean_pio():
    pio_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".pio")
    pio_build_path = os.path.join(pio_path, "build")
    pio_libdeps_path = os.path.join(pio_path, "libdeps")
    rmdir_if(pio_build_path)      
    rmdir_if(pio_libdeps_path)
         
    mkdir_if(pio_build_path)
    mkdir_if(pio_libdeps_path)         
	
def clean_vscode():
	vscode = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".vscode")
	del_if(vscode+"\\c_cpp_properties.json")
	del_if(vscode+"\\launch.json")	


# MAJOR.MINOR.PATCH
def get_version():
	with open("VERSION-dev", "r") as version_file:
		version = version_file.read().strip()		
		if version.startswith('v'):					
			version = version[1:]
               
		parts = version.split('.')					
		return tuple(int(part) for part in parts)

def set_version(new_version):
    if isinstance(new_version, tuple):
        # Format patch (last part) with 4 digits
        new_version = '.'.join(str(part) if i < len(new_version)-1 else str(part).zfill(4) for i, part in enumerate(new_version))
    with open("VERSION-dev", "w") as version_file:
        version_file.write(f"v{new_version}\n")

def write_autoversion_h():
    version = get_version()
    hpp_content = f"""#ifndef __AUTOVERSION_H__
#define __AUTOVERSION_HPP__


#define FIRMWARE_MAJOR_VERSION {version[0]}
#define FIRMWARE_MINOR_VERSION {version[1]}
#define FIRMWARE_PATCH_VERSION {str(version[2]).zfill(4)}

#define FIRMWARE_VERSION "{version[0]}.{version[1]}.{str(version[2]).zfill(4)}"

#endif // __AUTOVERSION_H__

"""
    hpp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "include", "autoversion.h")
    with open(hpp_path, "w") as hpp_file:
        hpp_file.write(hpp_content)
    print(f"Version written to {hpp_path}")

def increment_version(type='patch'):    
	current_version = get_version()
	new_version = list(current_version)
	if type == 'major': 
		new_version[0] += 1	
		new_version[1] = 0
		new_version[2] = 0
	elif type == 'minor':
		new_version[1] += 1
		new_version[2] = 0
		new_version[3] = 0
		new_version[4] = 0
		new_version[5] = 0
	else:  # 'patch' or default
		new_version[-1] += 1	
            
	set_version(tuple(new_version))
	print(F"Version updated from: {tuple(current_version)}, to version: {tuple(new_version)}")
	  

# git helpers
def git_add():
    try:
        result = subprocess.run(["git", "add", "."], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("Git add failed")
            print(result.stderr)
    except Exception as e:
        print(f"Error during git add: {e}")

def git_commit(message): 
    try:
        result = subprocess.run(["git", "commit", "-m", message], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("Git commit failed")
            print(result.stderr)
		
    except Exception as e:
        print(f"Error during git commit: {e}")

def git_fetch():
    try:
        result = subprocess.run(["git", "fetch"], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(result.stderr)
    except Exception as e:
        print(f"Error during git fetch: {e}")

def git_pull():
    try:
        result = subprocess.run(["git", "pull", "origin", "dev-master"], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(result.stderr)
    except Exception as e:
        print(f"Error during git pull: {e}")

def git_status():
	try:
		result = subprocess.run(["git", "status"], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
		if result.returncode == 0:
			print(result.stdout)
		else:	
			print(result.stderr)			
	except Exception as e:
		print(f"Error during git status: {e}")

def git_push():    
    try:
        result = subprocess.run(["git", "push"], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        if result.returncode == 0:
            print("Git push successful")
            print(result.stdout)
        else:
            print("Git push failed")
            print(result.stderr)
    except Exception as e:
        print(f"Error during git push: {e}")


print("Cleaning '.pio' subfolder...")

clean_pio()
clean_vscode()

print("Version as tuple:", get_version())
print("Incrementing version...")

args = sys.argv[1:]
if len(args) > 0:
	m_type = args[0].lower()
	if m_type in ['major', 'minor', 'patch']:
		increment_version(type=m_type)
	else:
		print("Unknown version increment type. Use 'major', 'minor', or 'patch'. Defaulting to 'patch'.")	
else:
	increment_version()	
      

write_autoversion_h()

print("args:", args)
print("Version after increment:", get_version())



current_version = get_version()
commit_message = f"Update version to: v{'.'.join(str(p) if i < len(current_version)-1 else str(p).zfill(4) for i, p in enumerate(current_version))}"

# Step 1: Check Your Working Directory Status
#           git status
git_status()

# Step 2: Stage Your Changes
#           git add .
git_add()

# Step 3: Commit Your Changes
#           git commit -m "Your commit message here"
git_commit(commit_message)

# Step 4: Pull Latest Changes from the Remote Repository
#           git pull origin "<branch-name>"
git_pull()

# Step 5: Resolve Conflicts (If Any)
# Step 6: Push Your Changes
#           git push origin "<branch-name>"
git_push()


#sys.path.remove()