import random

class Lattice:
    # start_label: a label which indicates the location to start growing the cluster from
    # should_add: a function which takes in a label and returns True or False. If should_add
    # returns true, then it adds the label to the cluster and then recursively attempts
    # to add its neighbors to the cluster.
    # This function returns a set of labels which make up the cluster
    def get_cluster(self, start_label, should_add):
        cluster = set()
        cluster.add(start_label)
        labels_to_check = [start_label]
        while len(labels_to_check) != 0:
            label = labels_to_check.pop()
            nbrs = self.get_neighbors(label)
            for neighbor in nbrs:
                if (neighbor not in cluster) and should_add(neighbor):
                    cluster.add(neighbor)
                    labels_to_check.append(neighbor)
        return cluster

    # Returns a random numeric spin
    def random_spin(self):
        return random.choice([-1,1])

    # SUBCLASS FUNCTIONS ARE BELOW:
    # All subclasses of lattice should implement these methods

    # Given a label, returns a list of neighbors of this label.
    def get_neighbors(self, label):
        pass

    # Given a label, returns the value stored at that label
    def get(self, label):
        pass

    # Stores a value at the given label
    def set(self, label, value):
        pass

    # Gives a random label in the lattice
    def get_random_label(self):
        pass

    # Exports the internal state of the lattice
    def export(self):
        pass
