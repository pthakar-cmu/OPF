from Chi_Square import Chi_2
import numpy as np
import pandas as pd


trainFile = "Panos_Data.csv"
def chi_2(info_gain, no_bins):
    return info_gain * (no_bins)

class Node:
    def __init__(self, data, depth=0):
        self.data = data  # type: <Data>.
        self.left = None  # type: <Node>.
        self.right = None  # type: <Node>
        self.depth = depth
        self.N = data.N
        self.M = data.M
        self.entropy = data.entropy

        self.split()

    def split(self):
        if self.N <= 1 or self.entropy == 0:
            return
        split_info, max_info_gain = self.data.get_split_info(bin_size)
        if split_info is None:
            return
        self.split_info = split_info
        split_on = split_info[0]
        split_value = split_info[1]

        go_left = self.data.X[:, split_on] < split_value
        go_right = self.data.X[:, split_on] >= split_value
        self.left = Node(Data(X=self.data.X[go_left, :], Y=self.data.Y[go_left]), depth=self.depth+1)
        self.right = Node(Data(X=self.data.X[go_right, :], Y=self.data.Y[go_right]), depth=self.depth+1)
        
    def print_tree(self, no, max_no):
        max_no_l = 0
        max_no_r = 0
        print("Father Node: {}  divides by Atribute{}<{}".format(no, self.split_info[0]+1, self.split_info[1]))
        print("Left  Child: {} includes {} elements.".format(max_no+1, self.left.N))
        print("\t\t\tZero Attributes {}")
        print(f"\t\t\t*** Rating = %.2f %% ***" % (sum([1 for i in self.left.data.Y if i=="TRUE"]) / self.left.N * 100))
        print("Right Child: {} includes {} elements.".format(max_no+2, self.right.N))
        print("\t\t\tZero Attributes {}")
        print(f"\t\t\t*** Rating = %.2f %% ***" % (sum([1 for i in self.right.data.Y if i=="TRUE"]) / self.right.N * 100))
        print("~~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~ ~~~\n")
        if self.left.left and self.left.right:
            max_no_l = self.left.print_tree(max_no+1, max(max_no_l, max_no_r, max_no+2))
        if self.right.left and self.right.right:
            max_no_r = self.right.print_tree(max_no+2, max(max_no_l, max_no_r, max_no+2))
        return max(max_no_l, max_no_r)

        
class Data:
    def __init__(self, file="", X=None, Y=None, header=None):
        if file:
            with open(trainFile, "r") as f:
                self.header = f.readline().split(",")[1:]

            self.X = np.loadtxt(trainFile, delimiter=",", skiprows=1, usecols=range(1,11))
            self.Y = np.loadtxt(trainFile, delimiter=",", skiprows=1, usecols=(11), dtype="U15")
        
        elif X is not None and Y is not None:
            self.header = header
            self.X = X
            self.Y = Y

        self.N, self.M = np.shape(self.X)
        self.entropy = self._entropy()

    def get_smallest_interval(self):
        intervals = []
        for j in range(self.M):
            interval = max(self.X[:,j]) - min(self.X[:,j])
            interval = interval if interval !=0 else np.inf
            intervals.append(interval)

        bin_size = min(intervals) / 50
        return bin_size
        # smallest_interval_gen = self.header[np.argmin(intervals)]

    def _no_bins(self, bin_size):
        self.no_bins = []
        for gen in range(self.M):
            self.no_bins.append(int((self.X[:,gen].max() - self.X[:,gen].min()) // bin_size))  

    def _entropy(self):
        _, counts = np.unique(self.Y, return_counts=True)
        if len(counts) == 0:
            return 0.0
        entropy = np.sum(
            [(-counts[i] / np.sum(counts)) * np.log2(counts[i] / np.sum(counts))
                for i in range(len(counts))])
        return entropy

    def get_info_gain(self, gen, split_value):
        go_left = self.X[:,gen] < split_value
        go_right = self.X[:,gen] >= split_value
        left = Data(X=self.X[go_left, :], Y=self.Y[go_left])
        right = Data(X=self.X[go_right, :], Y=self.Y[go_right])

        weighted_entropy = (left.N / self.N * left.entropy) + (right.N / self.N * right.entropy)
        info_gain = self.entropy - weighted_entropy
        return info_gain
    
    def get_split_info(self, bin_size):
        self._no_bins(bin_size)

        max_info_gain = -np.inf
        split_info = None
        for gen in range(self.M):
            no_bins = self.no_bins[gen]

            for bin_no in range(1, no_bins):
                split_value = bin_no * bin_size + self.X[:,gen].min()
                info_gain = self.get_info_gain(gen, split_value)

                chi2 = chi_2(info_gain, no_bins)
                if info_gain > max_info_gain and chi2 > 10.7168:
                    max_info_gain = info_gain
                    split_info = (gen, split_value)

        return split_info, max_info_gain


if __name__ == "__main__":
    trainData = Data(file=trainFile)
    bin_size = trainData.get_smallest_interval()

    rootNode = Node(trainData)
    rootNode.print_tree(0, 0)
    print("")
