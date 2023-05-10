import json
import pathlib


def load_secrets():
    # vaultfile located src/secrets
    secretsfile=pathlib.Path(__file__).absolute().parent.joinpath("secrets.json")
    with open(secretsfile,'r') as f:
        secrets=json.load(f)
    return secrets   

