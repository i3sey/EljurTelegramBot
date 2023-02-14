def cleanup(dictionary):
    return '\n'.join([f'<b>{key.capitalize() if isinstance(key, str) else " "}:</b> {value.capitalize() if isinstance(value, str) else " "}' for key, value in dictionary.items()])


def hwcleanup(dictionary):
    return '\n'.join([f'<b>{value["name"].capitalize()}:</b> {value["hometask"]}\n' for key, value in dictionary.items() if value["hometask"] is not None])


def dailyCleanup(dictionary):
    return '\n'.join([f'<b>{key.capitalize()}.</b> {value["name"].capitalize()}' for key, value in dictionary.items()])


# Defines a function to loop through a list and yield a result or -2 
def magicLoop(ist, page):
    # Initializes an empty list
    result = []

    # Iterates through the list argument "ist" and uses enumerate() to add a counter to it
    for key, i in enumerate(ist):
    
        # Extends the list "result" by adding a number and incrementing by 1 for each element
        # that is equal to an element in the second argument "page"
        result.extend(key + 1 for l in page if i == l and ist[key + 1].isnumeric())
    # Returns the result, or if the list is empty, returns -2
    return result or -2



def merge(ist, Letter):
    e = []
    count = multiply(ist, Letter)
    for key, value in count.items():
        e.extend(ist[key + i] for i in range(value))
    return e


def multiply(ist, Letter):
    count = {}
    for e in Letter:
        count[e] = 1
        for _ in ist:
            try:
                test = ist[e + count[e]]
            except IndexError:
                break
            if f'{test}'.isdigit():
                count[e] += 1
            else:
                break
    return count
