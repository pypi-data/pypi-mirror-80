def dict_extract(dic, fields, *args):
    from .zfunction import list_or_args
    fields = list_or_args(fields, args)
    new_dic = {}
    for k, v in dic.items():
        if k in fields:
            new_dic[k] = v
    return new_dic
