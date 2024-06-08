import yaml
import argparse
import spacy
from spacy.tokens import Doc

# Load spaCy model
nlp = spacy.load("en_core_web_sm") 

# Define the adaptors
ADAPTORS = {
    "primero": "@openfn/language-primero@latest",
    "telerivet": "@openfn/language-telerivet@latest",
    "dhis2": "@openfn/language-dhis2@latest",
    "http": "@openfn/language-http@latest",
    "asana" : " @openfn/language-asana@latest",
    "azure-storage" : "@openfn/language-azure-storage@latest",
    "beyonic" : "@openfn/language-beyonic@latest",
    "bigquery" : "@openfn/language-bigquery@latest",
    "cartodb" : "@openfn/language-cartodb@latest",
    "commcare" : "@openfn/language-commcare@latest",
    "common": "@openfn/language-common@latest",
    "dynamics": "@openfn/language-dynamics@latest",
    "facebook" : "@openfn/language-facebook@latest",
    "fhir": "@openfn/language-fhir@latest",
    "godata": "@openfn/language-godata@latest",
    "googlehealthcare": "@openfn/language-googlehealthcare@latest",
    "googlesheets": "@openfn/language-googlesheets@latest",
    "hive": "@openfn/language-hive@latest",
    "khanacademy": "@openfn/language-khanacademy@latest",
    "kobotoolbox": "@openfn/language-kobotoolbox@latest",
    "magpi": "@openfn/language-magpi@latest",
    "mailchimp": "@openfn/language-mailchimp@latest",
    "mailgun": "@openfn/language-mailgun@latest",
    "maximo": "@openfn/language-maximo@latest",
    "medicmobile": "@openfn/language-medicmobile@latest",
    "mogli": "@openfn/language-mogli@latest",
    "mongodb": "@openfn/language-mongodb@latest",
    "msgraph": "@openfn/language-msgraph@latest",
    "mssql": "@openfn/language-mssql@latest",
    "mysql": "@openfn/language-mysql@latest",
    "nexmo": "@openfn/language-nexmo@latest",
    "ocl": "@openfn/language-ocl@latest",
    "openfn": "@openfn/language-openfn@latest",
    "openhim": "@openfn/language-openhim@latest",
    "openimis": "@openfn/language-openimis@latest",
    "openmrs": "@openfn/language-openmrs@latest",
    "openspp": "@openfn/language-openspp@latest",
    "postgresql": "@openfn/language-postgresql@latest",
    "progress": "@openfn/language-progress@latest",
    "rapidpro": "@openfn/language-rapidpro@latest",
    "resourcemap": "@openfn/language-resourcemap@latest",
    "salesforce": "@openfn/language-salesforce@latest",
    "satusehat": "@openfn/language-satusehat@latest",
    "sftp": "@openfn/language-sftp@latest",
    "smpp": "@openfn/language-smpp@latest",
    "surveycto": "@openfn/language-surveycto@latest",
    "telerivet": "@openfn/language-telerivet@latest",
    "template": "@openfn/language-template@latest",
    "twilio": "@openfn/language-twilio@latest",
    "vtiger": "@openfn/language-vtiger@latest",
    "zoho": "@openfn/language-zoho@latest"
}

# Define conditions for edges
EDGE_CONDITIONS = {
    "always": "always",
    "success": "on_job_success",
    "failure": "on_job_failure"
}

# Add custom extension to Doc object
Doc.set_extension("openfn_action", default=None, force = True)
Doc.set_extension("openfn_adaptor", default=None, force = True)


def parse_steps(steps):
    parsed_steps = []
    edges = []

    for i, step in enumerate(steps):
        doc = nlp(step)
        action = None
        adaptor = None

        # Use NER to find ADAPTERS
        for ent in doc.ents:
            if ent.label_ == "ADAPTER":
                adaptor = ADAPTORS.get(ent.text.lower())
                break  # Assume only one adaptor per step for now

        # If not found by NER, use action verbs to guess the adaptor
        if adaptor is None:
            for token in doc:
                if token.pos_ == "VERB":
                    action = token.lemma_.lower()  # Use lemma for normalized verb
                    adaptor = ADAPTORS.get(action, None)
                    if adaptor is not None:
                        break

        if action is None:
            raise ValueError(f"Could not determine action or adaptor for step: '{step}'")

        step_name = action.replace(" ", "-") + (f"-{adaptor.split('@')[0][1:]}" if adaptor else "")
        step_type = adaptor or "@openfn/language-common@latest"

        parsed_steps.append(
            {
                "name": step_name,
                "adaptor": step_type,
                "enabled": True,
                "body": "fn(state => state);",
            }
        )

        # Create edges with default conditions
        edge_condition = EDGE_CONDITIONS["success"] if i > 0 else EDGE_CONDITIONS["always"]
        edge = {
            "source_job": parsed_steps[i - 1]["name"] if i > 0 else "webhook",
            "target_job": step_name,
            "condition": edge_condition,
        }
        edges.append(edge)
    return parsed_steps, edges

def generate_project_yaml(project_name, description, workflow_name, steps):
    parsed_steps, edges = parse_steps(steps)

    jobs = {step["name"]: step for step in parsed_steps}

    edge_dict = {}
    for edge in edges:
        edge_key = f'{edge["source_job"]}->{edge["target_job"]}'
        edge_dict[edge_key] = edge

    project_structure = {
        "name": project_name,
        "description": description,
        "workflows": {
            workflow_name: {
                "name": workflow_name,
                "jobs": jobs,
                "triggers": {
                    "webhook": {
                        "type": "webhook"
                    }
                },
                "edges": edge_dict
            }
        }
    }

    with open("project1.yaml", "w") as file:
        yaml.dump(project_structure, file, sort_keys=False)

project_name = "test-project"
description = "Some sample test description"
workflow_name = "Sammple-Workflow"
steps = ["Fetch submissions from KoboCollect with language-kobotoolbox@latest",
"Push the data to the a postgresSQL database with language-postgresql@latest",
"Send text message to an admin using language-twilio@0.3.4 with status of sent message"]


generate_project_yaml(project_name, description, workflow_name, steps)
print("project.yaml file has been generated.")
