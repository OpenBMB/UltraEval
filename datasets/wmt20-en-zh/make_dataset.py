import glob
import json
import os


def transform_entry(source_line, reference_line):
    return {
        "passage": "",
        "question": source_line.strip(),
        "target_scores": {},
        "answer": reference_line.strip(),
    }


def convert(sources_path, references_path, output_file_path):
    source_files = glob.glob(os.path.join(sources_path, "*enzh*"))

    reference_files = glob.glob(os.path.join(references_path, "*enzh*"))
    with open(output_file_path, "w", encoding="utf-8") as outfile:
        for source_file, reference_file in zip(source_files, reference_files):
            with open(source_file, "r", encoding="utf-8") as src, open(
                reference_file, "r", encoding="utf-8"
            ) as ref:
                for source_line, reference_line in zip(src, ref):
                    new_entry = transform_entry(source_line, reference_line)
                    outfile.write(json.dumps(new_entry, ensure_ascii=False) + "\n")


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    sources_path = "../../RawData/wmt-20/newstest2020/txt/sources"
    references_path = "../../RawData/wmt-20/newstest2020/txt/references"
    output_path = "./data/news.jsonl"
    sources_dir_path = os.path.join(script_dir, sources_path)
    references_dir_path = os.path.join(script_dir, references_path)
    output_file_path = os.path.join(script_dir, output_path)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    convert(sources_dir_path, references_dir_path, output_file_path)

    sources_path = "../../RawData/wmt-20/testsuites2020/txt/sources"
    references_path = "../../RawData/wmt-20/testsuites2020/txt/references"
    output_path = "./data/suites.jsonl"
    sources_dir_path = os.path.join(script_dir, sources_path)
    references_dir_path = os.path.join(script_dir, references_path)
    output_file_path = os.path.join(script_dir, output_path)
    convert(sources_dir_path, references_dir_path, output_file_path)


if __name__ == "__main__":
    main()
