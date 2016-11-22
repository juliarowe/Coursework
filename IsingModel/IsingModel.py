class IsingModel:
    def __init__(self, lattice, temp, j, flip_interval):
        self.lattice = lattice
        self.temp = temp
        self.j = j
        self.frames = []
        self.flip_interval = flip_interval
        self.flip_i = 0
        self.num_flips = 0

    def get_num_flips(self):
        return self.num_flips

    def export(self):
        return {'temperature': self.temp, 'j': self.j, 'frames': list(self.frames), 'flip_interval': self.flip_interval}

    # Adds the amount of flips to the internal counter, in addition to possibly saving
    # a snapshot of the lattice. This method is called by subclasses of IsingModel
    def add_flips(self, amount):
        self.num_flips += amount
        if self.flip_i == 0:
            self.frames.append(self.lattice.export())
        self.flip_i = (self.flip_i + amount) % self.flip_interval

    # SUBCLASS FUNCTIONS ARE BELOW:
    # All subclasses of lattice should implement these methods

    def step(self):
        pass