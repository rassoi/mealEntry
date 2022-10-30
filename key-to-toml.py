import toml

output_file = ".streamlit/secrets.toml"

with open("rassoi-767af-google_storage.json") as json_file:
    json_text = json_file.read()

config = {"textkey": json_text}
toml_config = toml.dumps(config)

with open(output_file, "a") as target:
    target.write(toml_config)
