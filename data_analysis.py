import pandas as pd
import matplotlib.pyplot as plt
from config import NATIONS

def analyze_population_data_subplots(data_folder, data_file, plot_name):
    try:
        data = pd.read_csv(f"{data_folder}/{data_file}")
    except FileNotFoundError:
        print(f"Error: {data_folder}/{data_file} not found. Please check the file path.")
        return

    print("Population Data Analysis:")
    print(data.describe())

    nations = [NATIONS[i]["name"] for i in range(len(NATIONS))]

    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    # --- axs[0,0]: Population by Nation (Çizgi Grafik) ---
    for nation in nations:
        axs[0, 0].plot(data["Day"], data[nation], label=nation, color=nation.lower())
    axs[0, 0].set_title("Population by Nation")
    axs[0, 0].set_xlabel("Day")
    axs[0, 0].set_ylabel("Population")
    axs[0, 0].grid(True)
    axs[0, 0].legend(loc="upper left")

    # --- axs[0,1]: Chunks by Nation (Son Günün Pasta Grafiği Dağılımı) ---
    nation_chunk_columns = [f"{nation}_chunks" for nation in nations]
    for nation, chunk_column in zip(nations, nation_chunk_columns):
        axs[0, 1].plot(data["Day"], data[chunk_column], label=nation, color=nation.lower())
    axs[0, 1].set_title("Chunks Distribution")
    axs[0, 1].set_xlabel("Day")
    axs[0, 1].set_ylabel("Chunk Count")
    axs[0, 1].grid(True)
    axs[0, 1].legend(loc="upper left")

    # --- axs[1,0]: Total Population Trend ---
    axs[1, 0].plot(data["Day"], data["Total"], label="Total", linestyle='--', color='gray')
    axs[1, 0].set_title("Total Population Trend")
    axs[1, 0].set_xlabel("Day")
    axs[1, 0].set_ylabel("Total Population")
    axs[1, 0].grid(True)
    axs[1, 0].legend(loc="upper left")

    # --- axs[1,1]: Birth and Death Trends ---
    axs[1, 1].plot(data["Day"], data["Birth"], label="Birth", color='green')
    axs[1, 1].plot(data["Day"], data["Death"], label="Death", color='red')
    axs[1, 1].set_title("Birth and Death Trends")
    axs[1, 1].set_xlabel("Day")
    axs[1, 1].set_ylabel("Count")
    axs[1, 1].grid(True)
    axs[1, 1].legend(loc="upper left")

    plt.tight_layout()
    plt.savefig(f"{data_folder}/{plot_name}")
    plt.show()

if __name__ == "__main__":
    data_folder = "data"
    data_file = "population_data.csv"
    plot_name = "population_trend.png"
    analyze_population_data_subplots(data_folder, data_file, plot_name)