import random
from matplotlib import pyplot as plt

def turn():
    d1 = random.randint(1,6)
    d2 = random.randint(1,6)
    return [d1, d2, d1+d2]

def main():
    dice = []
    for _ in range(100000):
        dice += turn()
    data = {i: dice.count(i)/1000 for i in set(dice)}

    # Extract keys and values
    labels = list(data.keys())
    heights = list(data.values())
    
    # Create the bar graph
    plt.bar(labels, heights)
    
    # Add a title and labels
    plt.title('Backgammon turn probability')
    plt.xlabel('Labels')
    plt.ylabel('Percentage')
    
    # Show the graph
    plt.show()



if __name__ == '__main__':
    main()

