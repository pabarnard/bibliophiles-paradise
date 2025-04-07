"""
Source: https://www.oreilly.com/library/view/regular-expressions-cookbook/9781449327453/ch04s13.html
Regular Expressions Cookbook, 2nd Edition by Jan Goyvaerts, Steven Levithan

This method validates the ISBN of a book.  This works regardless of including spaces, dashes, "ISBN-", etc. in the right spots.
"""
import re

def validate_isbn(raw_data):
    # Checks for ISBN-10 or ISBN-13 format
    regex = re.compile("^(?:ISBN(?:-1[03])?:? )?(?=[0-9X]{10}$|(?=(?:[0-9]+[- ]){3})[- 0-9X]{13}$|97[89][0-9]{10}$|(?=(?:[0-9]+[- ]){4})[- 0-9]{17}$)(?:97[89][- ]?)?[0-9]{1,5}[- ]?[0-9]+[- ]?[0-9]+[- ]?[0-9X]$")
    if regex.search(raw_data):
        # Remove non ISBN digits, then split into a list
        chars = list(re.sub("[- ]|^ISBN(?:-1[03])?:?", "", raw_data))
        # Remove the final ISBN digit from `chars`, and assign it to `last`
        last = chars.pop()
        if len(chars) == 9:
            # Compute the ISBN-10 check digit
            val = sum((x + 2) * int(y) for x,y in enumerate(reversed(chars)))
            check = 11 - (val % 11)
            if check == 10:
                check = "X"
            elif check == 11:
                check = "0"
        else:
            # Compute the ISBN-13 check digit
            val = sum((x % 2 * 2 + 1) * int(y) for x,y in enumerate(chars))
            check = 10 - (val % 10)
            if check == 10:
                check = "0"
        if str(check) == last:
            return True
        else:
            return False
    else:
        return False