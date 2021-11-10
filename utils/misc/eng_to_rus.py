from data.data_for_bot import eng_to_rus_vocab

def replace_values_in_string(text):
    args_dict = eng_to_rus_vocab
    for key in args_dict.keys():
        text = text.replace(key, str(args_dict[key]))
    return text
