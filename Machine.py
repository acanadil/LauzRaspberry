class Machine:

    def __init__(self, id):
        self.jobs = []
        self.totalOutput = 0
        self.speed = 0
        self.id = id
        self.jobStarted = False
        self.processStarted = False