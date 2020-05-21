import re
import sys
from numpy import arange
import matplotlib.pyplot as plt


def parse_result(result_file_path):
    loss = []
    with open(result_file_path, 'r') as result_file:
        for line in result_file.readlines():
            if line[:5] != "Epoch":
                continue
            loss.append(float(re.search("loss ([0-9]+\.[0-9]+)", line).group(1)))
    return loss


def display_loss(result_file_path):
    loss = parse_result(result_file_path)
    plt.plot(arange(0, 5 * len(loss), 5), loss)
    plt.savefig(result_file_path + '.png')
    plt.show()


def main(loss_file):
    display_loss(loss_file)


if __name__ == '__main__':
    main(sys.argv[1])
