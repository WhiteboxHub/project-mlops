from data_loading import clean_data

from data_loading import get_s3_csv_data,ready_data_for_training,s3_upload_traing

def main():
    df = get_s3_csv_data.get_s3_csv_data()
    df1 = clean_data.clean_data(df)
    df2 = ready_data_for_training.ready_data_for_training(df1)
    s3_upload_traing.main(df2)
    return


if __name__ == "__main__":
    main()
