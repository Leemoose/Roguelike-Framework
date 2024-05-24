class ID():
    """
    All unique entities (monsters and items) are tagged with an ID and put into dictionary.
    IDs are generally used in arrays and other places and then the ID can be used to get actual object
    """

    def __init__(self):
        self.subjects = {}
        self.ID_count = 0

    def __str__(self):
        allrows = ""
        for entity in self.all_entities():
            allrows += ' '.join("Entity: {}, ID: {} \n".format(entity, entity.id_tag))
        return allrows

    def tag_subject(self, subject):
        self.ID_count += 1
        subject.gain_ID(self.ID_count)
        self.add_subject(subject)

    def get_subject(self, key):
        if key in self.subjects:
            return self.subjects[key]
        elif key == -1:
            raise Exception("You should not be getting a negative subject (id = {})".format(key))
        else:
            raise Exception("You should not be passing a id not in the subjects (id = {}).".format(key))

    def remove_subject(self, key):
        print("Item Dictionary:")
        print("You are trying to remove key {} from item dictionary".format(key))
        if key in self.subjects:
            return self.subjects.pop(key)
        elif key == -1:
            raise Exception("You should not be removing a negative subject")
        else:
            raise Exception("You should not be removing an id not in the subjects.")

    def add_subject(self, subject):
        self.subjects[subject.id_tag] = subject

    def all_entities(self):
        return list(self.subjects.values())

    def num_entities(self):
        return len(self.subjects)