import os

total_string = ""

for file in os.listdir():
    if not os.path.isfile(file):
        continue

    if not file.endswith(".html"):
        continue

    total_string += (
        str(file).split(".")[0].capitalize()
        + " = "
        + f'str(Path(__file__).parent.absolute()) + "/{file}"\n'
    )

print(total_string)
