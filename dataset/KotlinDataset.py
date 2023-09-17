import json
from torch.utils.data import Dataset

def _add_special_tokens(diff_hunk: str):
    diff_lines = diff_hunk.split("\n")[1:]        # remove start @@
    diff_lines = [line for line in diff_lines if len(line.strip()) > 0]
    map_dic = {"-": 0, "+": 1, " ": 2}
    def f(s):
        if s in map_dic:
            return map_dic[s]
        else:
            return 2
    labels = [f(line[0]) for line in diff_lines]
    diff_lines = [line[1:].strip() for line in diff_lines]
    input_str = ""
    for label, line in zip(labels, diff_lines):
        if label == 1:
            input_str += "<add>" + line
        elif label == 0:
            input_str += "<del>" + line
        else:
            input_str += "<keep>" + line
    return input_str


class KotlinDataset(Dataset):
    def __init__(self, tokenizer, path, max_source_length=512, max_target_length=128):
        self.tokenizer = tokenizer
        self.max_source_length = max_source_length
        self.max_target_length = max_target_length

        self.examples = self._read_and_tokenize(path)

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        example = self.examples[idx]
        return example

    def _read_and_tokenize(self, path):
        examples = []

        with open(path, "r") as file:
            lines = file.readlines()

            for line in lines:
                data = json.loads(line)
                source_tokens = self.tokenizer(
                    _add_special_tokens(data['patch']),
                    max_length=self.max_source_length,
                    padding="max_length",
                    truncation=True,
                    return_tensors="pt",
                )

                target_tokens = self.tokenizer(
                    "<msg>" + data['msg'],
                    max_length=self.max_target_length,
                    padding="max_length",
                    truncation=True,
                    return_tensors="pt",
                )

                examples.append(
                    {
                        "input_ids": source_tokens["input_ids"].squeeze(),
                        "attention_mask": source_tokens["attention_mask"].squeeze(),
                        "labels": target_tokens["input_ids"].squeeze(),
                    }
                )

        return examples
