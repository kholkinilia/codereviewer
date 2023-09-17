import json
import os


def get_env(name: str):
    return os.environ[name]


output_dir = get_env("OUTPUT_DIR")

if not os.path.exists(output_dir):
    os.mkdir(output_dir)
input_file = os.path.join(output_dir, f"jetbrains_kotlin.jsonl")

with open(input_file, "r") as file:
    data = [json.loads(line) for line in file.readlines()]

first_comments = {comment['id'] for comment in data if comment['in_reply_to_id'] is None}
not_replied_comments = set()

for comment_id in first_comments:
    is_not_replied = True
    for comment in data:
        if comment['in_reply_to_id'] == comment_id:
            is_not_replied = False
            break
    if is_not_replied:
        not_replied_comments.add(comment_id)

valid_data = []

for comment in data:
    if comment['id'] not in not_replied_comments:
        continue
    cur_json = {
        "patch": comment['patch'],
        "msg": comment['msg'],
    }
    if len(comment['patch']) <= 1000:
        valid_data.append(json.dumps(cur_json))

output_dir = get_env("OUTPUT_DIR")

if not os.path.exists(output_dir):
    os.mkdir(output_dir)
output_file = os.path.join(output_dir, f"jetbrains_kotlin_pure.jsonl")

with open(output_file, "w") as file:
    file.write("\n".join(valid_data))
