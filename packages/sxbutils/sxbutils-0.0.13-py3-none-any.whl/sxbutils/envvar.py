class envvar:
    def __init__(self, name, required, example, desc):
        self.name = name
        self.required = required
        self.example = example
        self.desc = desc

    def tostr(self):
        tostr="name="+self.name+" required="+str(self.required)+" example="+self.example
        print("name="+self.name)
        print("required="+str(self.required))
        print("example="+self.example)
        print("desc="+self.desc)
        return tostr

