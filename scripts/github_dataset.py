from github import Github
import os
import json
from tqdm import tqdm
from datetime import datetime

ACCESS_TOKEN_SECRET = "GITHUB_ACCESS_TOKEN"


def get_env(name: str):
    return os.environ[name]


access_token = get_env(ACCESS_TOKEN_SECRET)

g_client = Github(access_token)

repository_owner = "jetbrains"
repository_name = "kotlin"

repository = g_client.get_repo(f"{repository_owner}/{repository_name}")
timestamp_since = datetime.strptime("2020-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")

comments = repository.get_pulls_comments(since=timestamp_since)

output_dir = get_env("OUTPUT_DIR")

if not os.path.exists(output_dir):
    os.mkdir(output_dir)
output_file = os.path.join(output_dir, f"{repository_owner}_{repository_name}.jsonl")

results = []

for i, comment in tqdm(enumerate(comments), total=comments.totalCount):
    if not comment.path.endswith(".kt"):
        continue
    data = {
        "patch": comment.diff_hunk,
        "msg": comment.body,
        "id": comment.id,
        "in_reply_to_id": comment.in_reply_to_id,
    }
    results.append(json.dumps(data))
    if i % 300 == 0:
        with open(output_file, "a") as file:
            file.write("\n".join(results))
            file.write("\n")
        results = []


with open(output_file, "a") as file:
    file.write("\n".join(results))
results = []
