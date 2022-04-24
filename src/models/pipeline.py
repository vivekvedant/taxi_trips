from prepare_data import prepare_data
from train_model import train_model


def main():

    raw_data_path = "data/raw/"
    process_data_path = "data/processed/data.parquet"

    print("===========================")
    print("Data Preprocessing")
    print("===========================")
    prepare_data(raw_data_path,process_data_path)

    # print("===========================")
    # print("Model Training")
    # print("===========================")
    # train_model(process_data_path)



if __name__ == '__main__':
    main()