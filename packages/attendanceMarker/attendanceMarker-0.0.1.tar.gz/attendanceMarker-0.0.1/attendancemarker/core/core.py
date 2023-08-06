import pandas as pd

def __read_excel_file(filepath: str) -> pd.DataFrame:
    return pd.read_excel(filepath, index_col=None, header=None)

def __remove_first_n_rows_from_df(df: pd.DataFrame, num_rows: int) -> pd.DataFrame:
    return df.iloc[num_rows:]

def __get_col(df: pd.DataFrame, colNum: int):
    return df.iloc[:,colNum]

def __lower(series: pd.Series) -> pd.Series:
    return series.str.lower()

def mark_attendance(rollcallfile: str, attendeefile: str, sessiondate: str):
    rollCallDf: pd.DataFrame = __remove_first_n_rows_from_df(__read_excel_file(rollcallfile), 3)
    attendeeDf: pd.DataFrame = __remove_first_n_rows_from_df(__read_excel_file(attendeefile), 5)
    roll_num_from_roll_call = __lower(__get_col(rollCallDf, 2))
    name_from_attendee_df = __lower(__get_col(attendeeDf, 1))
    email_from_attendee_df = __lower(__get_col(attendeeDf, 2))

    # If roll number exists either in name or email
    rollCallDf[sessiondate] = roll_num_from_roll_call.apply(lambda  s: name_from_attendee_df.str.contains(s).any()) | roll_num_from_roll_call.apply(lambda  s: email_from_attendee_df.str.contains(s).any())
    rollCallDf.to_csv(rollcallfile+"_results")