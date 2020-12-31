import argparse, json, os

def read_json_file(file_path):
    assert os.path.isfile(file_path), 'file이 존재하지 않음'
    f = open(file_path)
    json_data = json.load(f)
    f.close()

    return json_data

def read_ids(file_path):
    assert os.path.isfile(file_path), 'file이 존재하지 않음'
    ids = []

    with open(file_path) as f:
        for line in f:
            line = line.strip()
            ids.append(line)
    return ids

def get_dep_conll(datas):
    dp_conll_sentences = {}
    for document in datas['document']:
        for sentence in document['sentence']:
            dp_conll_sentences.setdefault(sentence['id'], "")
            comment = "# id: {}\n# text: {}".format(sentence['id'], sentence['form'])
            conll_sentence = [comment]

            for dp_rel in sentence['DP']:
                conll_sentence.append([dp_rel['word_id'], dp_rel['word_form'], dp_rel['head'], dp_rel['label']])

            dp_conll_sentences[sentence['id']] = conll_sentence

    return dp_conll_sentences

def get_merge_dep_morph_conll(dep_conll, datas):
    merge_conll_sentences = {}

    for document in datas['document']:
        for sentence in document['sentence']:
            if sentence['id'] in dep_conll:
                conll_format = "{}\t{}\t{}\t_\t{}\t_\t{}\t{}\t_\t_"
                match_dp_conll = dep_conll[sentence['id']]

                conll_sentence = [match_dp_conll[0]]

                tmp_conll_sentence = {}
                words = sentence['word']
                morphemes = sentence['morpheme']

                for word in words:
                    tmp_conll_sentence.setdefault(word['id'], [word['id'], word['form'], [], []])

                for morpheme in morphemes:
                    word_id = morpheme['word_id']
                    tmp_conll_sentence[word_id][2].append(morpheme['form'])
                    tmp_conll_sentence[word_id][3].append(morpheme['label'])

                for idx, token in sorted(tmp_conll_sentence.items(), key=lambda x: x[0]):
                    dp_info = match_dp_conll[idx]
                    if dp_info[2] == -1:
                        dp_info[2] = 0

                    conll_sentence.append(conll_format.format(dp_info[0], dp_info[1], " ".join(token[2]), "+".join(token[3]), dp_info[2], dp_info[3]))

                merge_conll_sentences.setdefault(sentence['id'], "\n".join(conll_sentence))

    return merge_conll_sentences

def write_file(output_file, conlls):
    with open(output_file, "w") as f:
        f.write("\n\n".join(conlls))


def main():
    parser = argparse.ArgumentParser(description="모두의 말뭉치 의존 구문 코퍼스 구축")
    parser.add_argument("--dependency_file", type=str, default="", help="의존 구문 분석 파일", required=True)
    parser.add_argument("--morphology_file", type=str, default="", help="형태 분석 파일", required=True)
    parser.add_argument("--train_ids", type=str, default="", help="학습 데이터 아이디", required=True)
    parser.add_argument("--valid_ids", type=str, default="", help="개발 데이터 아이디", required=True)
    parser.add_argument("--eval_ids", type=str, default="", help="평가 데이터 아이디", required=True)
    parser.add_argument("--output_path", type=str, default="", help="저장할 폴더 경", required=True)

    args = parser.parse_args()

    assert os.path.isdir(args.output_path), "폴더가 존재하지 않습니다."

    train_ids, valid_ids, eval_ids = read_ids(args.train_ids), read_ids(args.valid_ids), read_ids(args.eval_ids)
    print("Train / Validation / Evaluation ids file is loaded.")
    json_deps, json_morphs = read_json_file(args.dependency_file), read_json_file(args.morphology_file)
    print("Json file is loaded.")

    print("Merging..")
    dep_conlls = get_dep_conll(json_deps)
    merge_conlls = get_merge_dep_morph_conll(dep_conlls, json_morphs)

    train_conlls = [merge_conlls[x] for x in train_ids]
    valid_conlls = [merge_conlls[x] for x in valid_ids]
    eval_conlls = [merge_conlls[x] for x in eval_ids]

    print("Writing File")
    write_file(os.path.join(args.output_path, "train.conll"), train_conlls)
    write_file(os.path.join(args.output_path, "valid.conll"), valid_conlls)
    write_file(os.path.join(args.output_path, "eval.conll"), eval_conlls)

    print("Finished.")
    
main()





