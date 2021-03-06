class RLC_image:
    def encode(input_string):
        count = 1
        prev = -1
        lst = []
        for character in input_string:
            if character != prev:
                if prev != -1:
                    entry = (prev, count)
                    lst.append(entry)
                    # print lst
                count = 1
                prev = character
            else:
                count += 1
        else:
            try:
                entry = (character, count)
                lst.append(entry)
                return (lst, 0)
            except Exception as e:
                print("Exception encountered {e}".format(e=e))
                return (e, 1)

    def decode(lst):
        q = []
        for character, count in lst:
            while (count > 0):
                q.append(character)
                count -= 1
        return q
