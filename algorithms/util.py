from PIL import Image
import numpy as np
import json

with open("test_cases.json", "r") as file:
    test_cases = json.loads(file.read())

with open("schema.json", "r") as file:
    schema = json.loads(file.read())


# for 2D -> IMG
def array_to_img(array):
    mod = np.array(array, dtype=np.uint8)
    return Image.fromarray(mod)


# for IMG -> 2D
def img_to_array(img):
    return np.asarray(img)

def find_question_in_schema(question):
    for grp in schema.values():
        if question in grp:
            return grp[question]

    raise Exception(f"{question} not found.")

def fetch_question_schema():
    pass


def fetch_test_cases(question):
    return test_cases[question]


def preheat(question):
    image = Image.open("sample.jpg").convert("L")
    img_data = img_to_array(image)
    metadata = find_question_in_schema(question)
    cases = fetch_test_cases(question)

    def wrapper(fn):
        for each in cases:
            result = fn(*[img_data, *each])

            if metadata['output'][0] == 'IMG':
                image = array_to_img(result)
                image.show()
            else:
                print(result)

    return wrapper
