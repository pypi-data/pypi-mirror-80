
def convert_to_human_readable(size, use_exact_size=False):
    try:
        size=int(size)
        if use_exact_size:
            if size > 1099511627776:
                return "{} TB".format(int(round(size / 1099511627776)))
            elif size > 1073741824:
                return "{} GB".format(int(round(size / 1073741824)))
            elif size > 1048576:
                return "{} MB".format(int(round(size / 1048576)))
            elif size > 1024:
                return "{} KB".format(int(round(size / 1024)))
            else:
                return "{} B".format(int(size))
        else:
            if size >  1000000000000:
                return "{} TB".format(int(round(size/1000000000000)))
            elif size > 1000000000:
                return "{} GB".format(int(round(size / 1000000000)))
            elif size > 1000000:
                return "{} MB".format(round(int(size / 1000000)))
            elif size > 1000:
                return "{} KB".format(round(int(size / 1000)))
            else:
                return "{} B".format(round(int(size)))
    except Exception as e:
        return None