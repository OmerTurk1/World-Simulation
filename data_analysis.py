import pandas as pd
import matplotlib.pyplot as plt

def analyze_population_data(data_folder, data_file):
    try:
        data = pd.read_csv(f"{data_folder}/{data_file}")
    except FileNotFoundError:
        print(f"Error: {data_folder}/{data_file} not found. Please check the file path.")
        return

    print("Population Data Analysis:")
    print(data.describe())
    
    fig = plt.figure(figsize=(11, 9))
    
    gs = fig.add_gridspec(2, 2)
    
    ax0 = fig.add_subplot(gs[0, :])
    for nation in data.drop(columns=["Day", "Total", "Birth", "Death"], errors='ignore').columns:
        ax0.plot(data["Day"], data[nation], label=nation, color=nation.lower())
    ax0.set_title("Daily Population by Nation")
    ax0.set_xlabel("Day")
    ax0.set_ylabel("Population")
    ax0.grid(True)
    ax0.legend(loc="upper left")

    ax1 = fig.add_subplot(gs[1, 0])
    ax1.plot(data["Day"], data["Total"], label="Total", linestyle='--', color='gray')
    ax1.set_title("Total Population Trend")
    ax1.set_xlabel("Day")
    ax1.set_ylabel("Total Population")
    ax1.grid(True)
    ax1.legend(loc="upper left")

    ax2 = fig.add_subplot(gs[1, 1])
    ax2.plot(data["Day"], data["Birth"], label="Birth", color='green')
    ax2.plot(data["Day"], data["Death"], label="Death", color='red')
    ax2.set_title("Daily Births and Deaths")
    ax2.set_xlabel("Day")
    ax2.set_ylabel("Count")
    ax2.grid(True)
    ax2.legend(loc="upper left")

    plt.tight_layout()
    plt.savefig(f"{data_folder}/population_trend.png")
    plt.show()

if __name__ == "__main__":
    data_folder = "data"
    data_file = "population_data.csv"
    analyze_population_data(data_folder,data_file)