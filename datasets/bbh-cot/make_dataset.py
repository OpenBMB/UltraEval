import json
import os

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))

    fileanme1 = os.path.join(script_dir, "../../RawData/bbh")
    filename_cot = os.path.join(script_dir, "cot-prompts")
    output_dir = os.path.join(script_dir, "./data")

    os.makedirs(output_dir, exist_ok=True)

    for task in os.listdir(fileanme1):
        if not task.endswith(".json"):
            continue
        new_data = list()
        with open(os.path.join(fileanme1, task), "r", encoding="utf-8") as f:
            origin_data = json.load(f)
        
        with open(os.path.join(filename_cot, task.replace(".json", ".txt")), "r", encoding="utf-8") as f:
            cot_data = [line.strip() for line in f.readlines()[2:]]
        # new_data["cot"] = "\n".join(cot_data)
        for item in origin_data["examples"]:
            temp_data = {
            "cot": "",
            "input": "",
            "answer": []
            }
            temp_data["cot"] = "\n".join(cot_data)
            temp_data["input"] = item["input"]
            temp_data["answer"].append(item["target"].strip())
            if item["target"].strip().startswith("(") and item["target"].strip().endswith(")"):
                temp_data["answer"].append(item["target"].strip()[1:-1])
            
            new_data.append(temp_data)
        
        output_file = os.path.join(
            output_dir, task.replace(".json", ".jsonl").replace("_", "-")
        )
        with open(output_file, "w", encoding="utf-8") as outfile:
            for example in new_data:
                outfile.write(json.dumps(example, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
