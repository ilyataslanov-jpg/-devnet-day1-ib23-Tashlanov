import json
import yaml
import csv
import hashlib
import os
from xml.etree.ElementTree import Element, tostring

INPUT = "artifacts/day1/response.json"
OUTDIR = "artifacts/day2"

os.makedirs(OUTDIR, exist_ok=True)

token = os.getenv("STUDENT_TOKEN")
name = os.getenv("STUDENT_NAME")
group = os.getenv("STUDENT_GROUP")

token_hash8 = hashlib.sha256(token.encode()).hexdigest()[:8]

with open(INPUT) as f:
    data = json.load(f)

title = data["title"]

normalized = {
    "student": {
        "name": name,
        "group": group,
        "token": token,
        "token_hash8": token_hash8
    },
    "todo": {
        "userId": data["userId"],
        "id": data["id"],
        "title": title,
        "completed": data["completed"],
        "title_len": len(title)
    }
}

# JSON
with open(f"{OUTDIR}/normalized.json", "w") as f:
    json.dump(normalized, f, indent=2)

# YAML
with open(f"{OUTDIR}/normalized.yaml", "w") as f:
    yaml.dump(normalized, f)

# CSV
with open(f"{OUTDIR}/normalized.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["token","token_hash8","title"])
    writer.writerow([token, token_hash8, title])

# XML
root = Element("data")

student = Element("student")
student.text = name
root.append(student)

todo = Element("title")
todo.text = title
root.append(todo)

xml = tostring(root)

with open(f"{OUTDIR}/normalized.xml","wb") as f:
    f.write(xml)

summary = {
    "student": {
        "token": token,
        "token_hash8": token_hash8
    },
    "generated_files": [
        "normalized.json",
        "normalized.yaml",
        "normalized.xml",
        "normalized.csv"
    ]
}

with open(f"{OUTDIR}/summary.json","w") as f:
    json.dump(summary,f,indent=2)

print("Day2 files generated")
