def stringToNumber(originalString):
    if originalString is None:
        return None
    
    # Split the string from the right side using rsplit
    parts = originalString.rsplit(',', maxsplit=1)

    # Replace all occurrences of ',' with '' in the remaining parts
    remaining_parts = parts[0].replace(',', '') if parts else ''

    # Join the parts back with a period instead of the last comma
    if len(parts) > 1:
        modified_string = remaining_parts + '.' + parts[1]
    else:
        modified_string = remaining_parts

    return modified_string