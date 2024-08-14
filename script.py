import json
import os
import shutil
import argparse

def resolve_ref(ref, definitions):
    """
    Resolves a $ref in the OpenAPI specification by returning the full definition.
    """
    ref_path = ref.split('/')[1:]  # Skip the initial '#'
    resolved = definitions
    for part in ref_path:
        resolved = resolved.get(part, {})
    return resolved

def resolve_schema(schema, definitions):
    """
    Recursively resolve all $ref in a schema and return the fully expanded schema.
    """
    if isinstance(schema, dict):
        if '$ref' in schema:
            resolved = resolve_ref(schema['$ref'], definitions)
            return resolve_schema(resolved, definitions)
        else:
            for key, value in schema.items():
                schema[key] = resolve_schema(value, definitions)
    elif isinstance(schema, list):
        schema = [resolve_schema(item, definitions) for item in schema]
    return schema

def generate_openapi_combinations(openapi_spec_str, output_dir):
    # Load the OpenAPI specification
    openapi_spec = json.loads(openapi_spec_str)
    
    # Extract definitions for easy access
    definitions = openapi_spec.get('definitions', {})
    
    # Iterate over paths in the spec
    for path, path_item in openapi_spec.get("paths", {}).items():
        # Create directory for the path
        path_dir = os.path.join(output_dir, path.strip('/').replace('/', '_'))
        os.makedirs(path_dir, exist_ok=True)
        
        # Iterate over methods in the path
        for method, operation in path_item.items():
            # Create directory for the method
            method_dir = os.path.join(path_dir, method.upper())
            os.makedirs(method_dir, exist_ok=True)
            
            # Iterate over response codes in the method
            for response_code, response in operation.get("responses", {}).items():
                # Resolve the response schema if it exists
                if 'schema' in response:
                    response['schema'] = resolve_schema(response['schema'], definitions)
                
                # Generate filename for the combination
                filename = f"{response_code}.json"
                file_path = os.path.join(method_dir, filename)
                
                # Create output content
                output_content = {
                    "path": path,
                    "method": method,
                    "response_code": response_code,
                    "response": response
                }
                
                # Write to file
                with open(file_path, 'w') as outfile:
                    json.dump(output_content, outfile, indent=2)
                
                print(f"Generated {file_path}")

def main():
    parser = argparse.ArgumentParser(description='Process OpenAPI spec and generate output files.')
    parser.add_argument('-json', required=True, help='Path to the OpenAPI JSON file.')
    parser.add_argument('-output', required=True, help='Directory to output the generated files.')

    args = parser.parse_args()

    # Read the OpenAPI spec file
    with open(args.json, 'r') as f:
        openapi_spec_str = f.read()

    # Recreate the output directory
    if os.path.exists(args.output):
        shutil.rmtree(args.output)
    os.makedirs(args.output)

    # Generate combinations
    generate_openapi_combinations(openapi_spec_str, args.output)

if __name__ == "__main__":
    main()