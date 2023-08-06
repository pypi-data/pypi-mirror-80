class Switch:
    def __init__(self):
        self.switchList={}
    def AddToSwitch(self, Input, Outcome):
        self.switchList[Input]=Outcome
    def PrintSwitch(self):
        print(self.switchList)
    def LastSwitch(self, Input, Outcome, Bind, Else=''):
        self.switchList[Input]=Outcome
        Answer=self.switchList.get(Bind)
        try:
            exec(Answer)
        except TypeError:
            exec(Else)