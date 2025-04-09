"""
Módulo para extrair entradas únicas de 'context' de arquivos .jsonl em um diretório.
Salva os contextos únicos em novos arquivos JSON para cada entrada processada.
"""

import os
import json
import glob
import argparse


def log_json_error(filename, line_number, error):
    print(f"JSON decoding error in file {filename} at line {line_number}: {error}")


def log_file_error(filename, error):
    print(f"Erro ao processar o arquivo {filename}: {error}")


def extract_unique_contexts(input_directory, output_directory):
    """
    Lê arquivos .jsonl no diretório de entrada, extrai contextos únicos e salva em JSON.
    """
    os.makedirs(output_directory, exist_ok=True)
    jsonl_files = glob.glob(os.path.join(input_directory, "*.jsonl"))
    print(f"Found {len(jsonl_files)} JSONL files.")

    for file_path in jsonl_files:
        filename = os.path.basename(file_path)
        name, _ = os.path.splitext(filename)
        output_filename = f"{name}_unique_contexts.json"
        output_path = os.path.join(output_directory, output_filename)

        unique_contexts_dict = {}
        print(f"Processing file: {filename}")

        try:
            with open(file_path, "r", encoding="utf-8") as infile:
                for line_number, line in enumerate(infile, start=1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        json_obj = json.loads(line)
                        context = json_obj.get("context")
                        if context and context not in unique_contexts_dict:
                            unique_contexts_dict[context] = None
                    except json.JSONDecodeError as e:
                        log_json_error(filename, line_number, e)

        except (FileNotFoundError, OSError) as e:
            log_file_error(filename, e)
            continue

        unique_contexts_list = list(unique_contexts_dict.keys())
        print(f"{len(unique_contexts_list)} unique `context` entries found in {filename}.")

        try:
            with open(output_path, "w", encoding="utf-8") as outfile:
                json.dump(unique_contexts_list, outfile, ensure_ascii=False, indent=4)
            print(f"Saved to: {output_filename}")
        except (IOError, OSError) as e:
            log_file_error(output_filename, e)

    print("All files have been processed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrai contextos únicos de arquivos .jsonl.")
    parser.add_argument("-i", "--input_dir", type=str, default="../datasets")
    parser.add_argument("-o", "--output_dir", type=str, default="../datasets/unique_contexts")
    args = parser.parse_args()

    extract_unique_contexts(args.input_dir, args.output_dir)
