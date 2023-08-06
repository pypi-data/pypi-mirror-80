import json
class Resource():
    def __len__(self):
        return len(self.data)

    def __setattr__(self, name, value):
        self.data[name] = value

    def __getattr__(self, item):
        try:
            return self.data[item]
        except:
            pass
        return self.data[item[0].upper() + item[1:]]

    def pretty(self, sort=False):
        return json.dumps(self.data, indent=4, sort_keys=sort)
