import argparse
from .parser import generate_project_yaml

def main():
    parser = argparse.ArgumentParser(description="Generate a project.yaml file for OpenFn workflows.")
    parser.add_argument("project_name", type=str, help="The name of the project.")
    parser.add_argument("description", type=str, help="The description of the project.")
    parser.add_argument("workflow_name", type=str, help="The name of the workflow.")
    parser.add_argument("steps", type=str, nargs="+", help="List of steps for the workflow, each step in the format 'Step Description with adaptor'.")
    
    args = parser.parse_args()
    
    generate_project_yaml(args.project_name, args.description, args.workflow_name, args.steps)
    print("project.yaml file has been generated.")

if __name__ == "__main__":
    main()
