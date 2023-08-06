# py-rest-assured
rest-assured in python 

## core modules
### json path generator
### json diff 
### auto-request

## roadmap 
### v0.1
- jsonpath generator
- 2 json responses diff fully/partly according to the provided keymappings
- py-json-diff cli 
```shell script
# install py-json-diff from source
python setup.py install 
# then can use it to diff 2 responses in json
py-json-diff <new-api-resp> <old-api-resp>  <keymappings.yml>
```
- show differences in logs(log in file, or console)

### v0.2
- auto send request to target service in test
- introduce test management framework to generate test cases for validating each key in json response
- junit-like test report


## references
- [rest-assured](https://github.com/rest-assured/rest-assured)
- [jsonpath-ng](https://github.com/h2non/jsonpath-ng)