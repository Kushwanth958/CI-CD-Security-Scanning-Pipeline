"""Small dependency-free application used as the pipeline scan target."""
import json


def health():
    return {"status": "ok", "service": "security-pipeline-demo"}


if __name__ == "__main__":
    print(json.dumps(health()))
