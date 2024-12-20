import re


txt = ["love","velo"]
pathern = "lo"

#output = re.search(pathern, txt)
output = re.findall(pathern, txt)
print(output)