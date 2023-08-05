class Dipole:
    BUCKET_SIZE = 20
    DIV = (38*8, 57*8, 76*8, 96*8)
    IDEAL = (0x30*8, 0x42*8, 0x56*8)

    def __init__(self):
        self.scaling = [1]*self.BUCKET_SIZE

    def classify(self, dur):
        """Translate a pulse duration in to S, M, L or X."""
        if dur is None:
            return 'X'

        scaled_dur = dur * (sum(self.scaling) / self.BUCKET_SIZE)

        if scaled_dur < self.DIV[0] or scaled_dur > self.DIV[3]:
            return 'X'

        if scaled_dur < self.DIV[1]:
            # short
            ret = 'S'
            ideal = self.IDEAL[0]
        elif scaled_dur < self.DIV[2]:
            # medium
            ret = 'M'
            ideal = self.IDEAL[1]
        else:
            # long
            ret = 'L'
            ideal = self.IDEAL[2]

        self.scaling.pop(0)
        val = max(min(ideal/dur, 1.1), 0.9)
        self.scaling.append(val)

        return ret
