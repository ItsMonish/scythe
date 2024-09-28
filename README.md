# Scythe
Scythe is a post-exploitation RAT that uses a Github repository as Command and Control (C2 / CNC). It is packed with capabilities such as keylogging, grabbing screenshots, opening reverse shells to remote IPs etc. It's capabilities can be further expanded as it can pull code from the C2 Github repository and execute them. The communications can also be obfuscated using base64, AES or any other custom methods to evade detection in basic ways. 

**Disclaimer**: This tool was created to learn about how malwares work and can be constructed. This is not intended to be used for malicious purposes. 
**Note**:  Executable created using this tool would easily be flagged by any Antivirus with Heuristics-based analysis. 

## Installation:
- `setup.sh` and `setup.ps1`will check for Python and pip installations, install dependencies required from `requirements.txt` and will prompt for a Github Personal Access Token that will be used to access the repository intended to use as C2.
- **Note**: It is advisable to use fine tuned tokens as you can limit the access it has to a single repository.

## Usage:
- Once dependencies are installed, the parameters in `params.py` can be optionally filled. If the parameters are filled, executables can be executed without passing any positional parameters. Else parameters must be specified for every execution. However, you may still override the parameters given in `params.py` by giving positional parameters.
- Execute `pyinstaller main.py` to create executable.
- **Note**: Pyinstaller can only create executable targeting the same operating system as the one it is run on. So to make an executable for Linux, it must be built on Linux and the same goes for Windows.
- The final built executable can be found under `dist/main/` as `main`.

## Working:
- Once executed, the tool will extract information on the host and create a folder in the repository with an UID and push the information into the file `00_info`
-  The tool will push updates in regular intervals which is specified as a parameter in `params.py` or it defaults to 300 seconds.
- This will also create another file in the same folder called `00_commands` which is a JSON file that takes commands. The key of the function that is mapped in the code is put against parameters to be passed to it. The parameters must be in the same order as the function argument list.  An example is shown below:
	```json
	[
		{
			"shell": ["127.0.0.1", 12345]
		},
		{
			"screenshot": [10]
		},
		{
			"testing": []
		}
	]
	```
- If a key-function is not available in the code, it checks for files in the same name under `modules/` in the C2 repository. It can pull code either in clear or obfuscated versions of them if available as \<function_name\>.\<obfuscation\> like `testing.base64`. If obfuscated versions are not available it will default to code in the clear.
- Code under `modules/` must be a single callable function with all dependencies imported inside the function. Example:
	```py
	def showPwned():
	    from time import strftime
	    message: str = strftime("%Y-%m-%d %H:%M")
	    with open("here.txt","w") as f:
	        f.write("I was here at {}".format(message))
	```
- The tool does not make any arrangements for persistence.
## C2 Helper:
- There is also a helper script `c2helper.py` to pull obfuscated content from the repository and aggregate multiple updates into respective files in clear text.
- The same script also packs a listener mode that can listen to the reverse shell. Since the contents of the reverse shell might be obfuscated, traditional listeners like NetCat might be hard to use.
- **Note**: The script is quite hacky, and works in very strict way. Feel free to modify it.