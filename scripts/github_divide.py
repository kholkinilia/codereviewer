from sklearn.model_selection import train_test_split

with open("../dataset/github/jetbrains_kotlin_pure.jsonl", "r") as file:
    lines = [line.strip() for line in file.readlines()]

train_lines, test_lines = train_test_split(lines, train_size=0.8, random_state=42)

with open("../dataset/fine_tuning/train.jsonl", "w") as file:
    file.write("\n".join(train_lines))

with open("../dataset/fine_tuning/test.jsonl", "w") as file:
    file.writelines("\n".join(test_lines))
