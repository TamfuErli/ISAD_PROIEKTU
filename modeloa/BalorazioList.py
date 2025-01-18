from modeloa import Balorazioa

class BalorazioList:
    def __init__(self):
        self.balorazioa = []

    def add_balorazioa(self, balorazioa):
        if isinstance(balorazioa, Balorazioa):
            self.balorazioak.append(balorazioa)

    def remove_balorazioa(self, balorazioa):
        if balorazioa in self.balorazioak:
            self.balorazioak.remove(balorazioa)

    def get_balorazioak(self):
        return self.balorazioak