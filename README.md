# Extract from OpenAPI

This repository serves as an example of how to extract combinations of path/method/response from an OpenAPI (Swagger) JSON.

The purpose of this action is to build a full hierarchy of the data definitions that would be returned from an API, by recursively retrieving the referenced definitions in the OpenAPI.

## How to use

### Use Python `script.py`

```
python3 script.py -json input/swagger.json -output output
```

Parameters:

- `-json` is path to the input JSON file
- `-output` is path to the output directory

### Execute Shell `run.sh`

```
chmod +x run.sh
```

```
./run.sh
```