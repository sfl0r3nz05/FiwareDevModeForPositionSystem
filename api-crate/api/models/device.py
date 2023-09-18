class Device:
    def __init__(self, idx, typex):
        self.idx = idx
        self.typex = typex

    def toJsonParsing(self):
        return{
                '_id': {
                'id': self.idx,
                'type': self.typex,
                'servicePath': "/"
            }}