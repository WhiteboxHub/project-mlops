from data_loading import db_training_data_loadin
from data_loading.clean_data import clean_data

from data_loading import get_s3_csv_data,ready_data_for_training,db_data_loading

def main():
    df = get_s3_csv_data.get_s3_csv_data()
    df1 = clean_data(df)
    df2 = ready_data_for_training.ready_data_for_training(df1)
    db_data_loading.main(df1)
    db_training_data_loadin.main(df2)
    return


if __name__ == "__main__":
    main()
