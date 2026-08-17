class DependencyManager:

    def __init__(self):
        self.dependencies = []

    def add(self, mod):
        if mod not in self.dependencies:
            self.dependencies.append(mod)

    def remove(self, mod):
        if mod in self.dependencies:
            self.dependencies.remove(mod)

    def get_all(self):
        return self.dependencies

    def check(self, installed_mods):

        missing = []

        for dependency in self.dependencies:
            if dependency not in installed_mods:
                missing.append(dependency)

        return missing