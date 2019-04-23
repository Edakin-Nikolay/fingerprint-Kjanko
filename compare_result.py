
class Compare_result:
    def __init__(self, true_positive=0, false_positive=0, false_negative=0, true_negative=0):
        self.true_positive = true_positive
        self.false_positive = false_positive
        self.true_negative = true_negative
        self.false_negative = false_negative

    def to_string(self):
        return "".join(["truePositive: ", str(self.true_positive), " falsePositive: ", str(self.false_positive),
                       " trueNegative: ", str(self.true_negative), " falseNegative: ", str(self.false_negative)])

    def modify_tp(self):
        self.true_positive = self.true_positive + 1
        print("tp", self.to_string())
        return self

    def modify_fp(self):
        self.false_positive = self.false_positive + 1
        print("fp", self.to_string())
        return self

    def modify_tn(self):
        self.true_negative = self.true_negative + 1
        print("tn", self.to_string())
        return self

    def modify_fn(self):
        self.false_negative = self.false_negative + 1
        print("fn", self.to_string())
        return self

