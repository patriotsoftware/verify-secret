# verify-secret-action
A GitHub Action for verifying that the secrets listed in a json file exist in an aws environment. 
It searches for the keyword 'secret' in the json key.

# Example Usage
```- uses: patriotsoftware/verify-secret@v1```
# Inputs
```
json-file:
  Pass in the file to parse
```

# Testing the action locally
Make sure that aws credentials are installed and have access to Get-Secret-Value.