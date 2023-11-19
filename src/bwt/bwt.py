#NOT A WORKIG CODE

'''
from typing import List, Dict
 
 
def all_rotations(s: str) -> List[str]:
    if not isinstance(s, str):
        raise TypeError("The parameter s type must be str.")
 
    return [s[i:] + s[:i] for i in range(len(s))]
 
 
def bwt_transform(s: str) -> Dict:
    if not isinstance(s, str):
        raise TypeError("The parameter s type must be str.")
    if not s:
        raise ValueError("The parameter s must not be empty.")
 
    rotations = all_rotations(s)
    rotations.sort()  # sort the list of rotations in alphabetically order
    # make a string composed of the last char of each rotation
    return "".join([word[-1] for word in rotations]),rotations.index(s)
 
 
def reverse_bwt(bwt_string: str, idx_original_string: int) -> str:
    if not isinstance(bwt_string, str):
        raise TypeError("The parameter bwt_string type must be str.")
    if not bwt_string:
        raise ValueError("The parameter bwt_string must not be empty.")
    try:
        idx_original_string = int(idx_original_string)
    except ValueError:
        raise TypeError(
            "The parameter idx_original_string type must be int or passive"
            " of cast to int."
        )
    if idx_original_string < 0:
        raise ValueError("The parameter idx_original_string must not be lower than 0.")
    if idx_original_string >= len(bwt_string):
        raise ValueError(
            "The parameter idx_original_string must be lower than" " len(bwt_string)."
        )
 
    ordered_rotations = [""] * len(bwt_string)
    for x in range(len(bwt_string)):
        for i in range(len(bwt_string)):
            ordered_rotations[i] = bwt_string[i] + ordered_rotations[i]
        ordered_rotations.sort()
    return ordered_rotations[idx_original_string]
 
 
if __name__ == "__main__":
    data_file="../../data/data.txt"
    with open(data_file,"r") as file:
        data=file.read()
    result,idx = bwt_transform(data)
    print(result)
    original_string = reverse_bwt(result,idx)
    print(original_string)
'''