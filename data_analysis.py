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
    fig, axs = plt.subplots(2, 1, figsize=(10, 8))
    for nation in data.drop(columns=["Day","Total"]).columns:
        axs[0].plot(data["Day"], data[nation], label=nation, color=nation.lower())
    axs[1].plot(data["Day"], data["Total"], label="Total", linestyle='--', color='gray')
    axs[0].set_title("Daily Population by Nation")
    axs[0].set_xlabel("Day")
    axs[0].set_ylabel("Population")
    axs[0].grid(True)
    axs[1].set_xlabel("Day")
    axs[1].set_ylabel("Population")
    axs[1].grid(True)
    axs[0].legend(loc="upper left")
    axs[1].legend(loc="upper left")
    plt.savefig(f"{data_folder}/population_trend.png")
    plt.show()

if __name__ == "__main__":
    data_folder = "data"
    data_file = "population_data.csv"
    analyze_population_data(data_folder,data_file)