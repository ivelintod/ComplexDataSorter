from numbers import Number
from collections import OrderedDict


def list_tuple_ind_sorter(data):
    '''sorting function for lists of tuples/lists
       that returns the index from which to sort'''
    zipped = zip(*data)
    index_from_which_to_sort = 0
    for zipped_elems in zipped:
        if not all(x == zipped_elems[0] for x in zipped_elems):
            return index_from_which_to_sort
        index_from_which_to_sort += 1
    return 0


def dict_sorter(data):
    '''sorting function for lists of dicts;
       check if dicts can be sorted by keys;
       if the sorting can't be done based on keys,
       because they are all the same, sort by values'''
    all_keys = [list(d.keys()) for d in data]
    if all(x == all_keys[0] for x in all_keys):
        for key in all_keys[0]:
            values_for_this_key = [d[key] for d in data]
            sorted_values_for_this_key = \
                different_type_sorter(values_for_this_key)
            if values_for_this_key != sorted_values_for_this_key:
                data.sort(key=lambda x: x[key])
                break
    else:
        ind = list_tuple_ind_sorter(all_keys)
        data.sort(key=lambda x: list(x.keys())[ind])
    return data


def different_type_sorter(input_data):
    '''main function that uses the above two as helpers;
       idea is that every type that should be categorized,
       is appended to a list which is then sorted internally;
       in the end the original data is constructed from these
       lists, which are now sorted'''
    nones = []
    numbers = []
    strings = []
    tuples = []
    lists = []
    dicts = []

    if isinstance(input_data, list) or isinstance(input_data, tuple):
        for ind, el in enumerate(input_data):
            if el is None:
                nones.append(el)
            elif isinstance(el, Number):
                numbers.append(el)
            elif isinstance(el, str):
                strings.append(el)
            elif isinstance(el, tuple):
                tuples.append(different_type_sorter(el))
            elif isinstance(el, list):
                lists.append(different_type_sorter(el))
            elif isinstance(el, dict):
                dicts.append(different_type_sorter(el))

        numbers.sort()
        strings.sort()

        if tuples:
            ind = list_tuple_ind_sorter(tuples)
            tuples.sort(key=lambda x: x[ind])
        if lists:
            ind = list_tuple_ind_sorter(lists)
            lists.sort(key=lambda x: x[ind])
        if dicts:
            dict_sorter(dicts)

        output_data = []

        for l in (nones, numbers, strings, tuples, lists, dicts):
            output_data.extend(l)

        if isinstance(input_data, tuple):
            return tuple(output_data)
        return output_data

    elif isinstance(input_data, dict):
        ordered_dict = OrderedDict()
        sorted_keys = different_type_sorter(list(input_data.keys()))
        for key in sorted_keys:
            if any(isinstance(input_data[key], obj)
                   for obj in (tuple, list, dict)):
                ordered_dict[key] = different_type_sorter(input_data[key])
            else:
                ordered_dict[key] = input_data[key]
        return ordered_dict

    #return input_data


INPUT_1 = [1, '0', [{1: [2, 1]}, {2: {'z': 0, 'y': [2, 1]}}, 0], 0, '1']

INPUT_2 = {
    'journeys': [
        {'id': 1, 'passengers': [1, 2], 'price': 100},
        {'id': 3, 'passengers': [2, 1], 'price': 200},
        {'id': 2, 'passengers': [4, 3], 'price': 150},
        None
    ]
}

if __name__ == '__main__':
    print(different_type_sorter(INPUT_1))
    print(different_type_sorter(INPUT_2))


#    PS: probably the dict sorter function is overcomplicated, but
#    I was not 100% sure how to proceed with dict sorting.
#    Based on the examples I see that the dict should be sorted
#    firstly through keys and only then, should comparisons by values
#    be done.
