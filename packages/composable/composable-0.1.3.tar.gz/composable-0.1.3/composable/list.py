from composable.pipeable import pipeable

@pipeable
def to_list(iter):
    ''' converts any iterable sequence into a list.

    Args:
        iter: an finite iterable sequence of items

    Returns:
        A list of the sequence iter, which maintains the original order
    '''
    return list(iter)

toList = to_list

built_in_slice = slice


@pipeable
def slice(from_, up_to, L):
    ''' Slices a list, equivalent to L[from_:up_to]

    Args:
        from_: starting index for the slice.
        up_to: final index

    Returns:
        A list that is a subsequence of L that starts at index `from_` 
        and includes all values up to, but not includeing `up_to`
    '''
    return L[built_in_slice(from_, up_to)]