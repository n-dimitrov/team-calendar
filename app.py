import pandas as pd
import streamlit as st

from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col], format='%Y-%m-%d %H:%M:%S')
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            # Treat columns with < 10 unique values as categorical
            if isinstance(df[column], pd.CategoricalDtype) or df[column].nunique() < 30:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    # default=list(df[column].unique())
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    _min,
                    _max,
                    (_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].str.contains(user_text_input, case=False, na=False)]

    return df


st.title("Team calendar")

df = pd.read_csv('team.csv', sep=';', encoding='utf-8') 
df['Name'] = df['Name'].apply(lambda x: x[:-1] if isinstance(x, str) else x)

f_df = filter_dataframe(df)
frame = st.data_editor(
            f_df,
            hide_index=True,
            disabled=[],
            column_order=('Name', 'Month', 'Status', 'From', 'To', 'Days', 'Duration', 'Absence', 'Description'),
)
total_days = f_df['Days'].sum()
unique_names = f_df['Name'].unique()

vc_df = f_df[f_df['Absence'] == 'Vacation']
vacations_count = vc_df['Days'].sum()

ic_df = f_df[f_df['Absence'] == 'Illness at entry']
illness_count = ic_df['Days'].sum()

mc_df = f_df[f_df['Absence'] == 'Maternity leave']
maternity_count = mc_df['Days'].sum()

with st.container(border=True):
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Employees", len(unique_names))
    col2.metric("Non working", total_days)
    col3.metric("Vacation", vacations_count)
    col4.metric("Sickleave", illness_count)
    col5.metric("Maternity", maternity_count)

# group by Month and sum Days
unique_names_count = len(unique_names)
monthly_df = f_df.groupby('Month')['Days'].sum().reset_index()

# offical working days per month
days_per_month_dict = {
    1: 22, 2: 21, 3: 20, 4: 22, 
    5: 19, 6: 20, 7: 23, 8: 22, 
    9: 19, 10: 23, 11: 21, 12: 19
    }

# Adding the new column to the dataframe based on the predefined dictionary
monthly_df['DPM'] = monthly_df['Month'].map(days_per_month_dict)
monthly_df['DPM'] = monthly_df['DPM'] * unique_names_count
monthly_df['Working'] = monthly_df['DPM'] - monthly_df['Days']
monthly_df['Working %'] = monthly_df['Working'] / monthly_df['DPM'] * 100

monthly_non_working_days = monthly_df['Days'].sum()
monthly_total_days = monthly_df['DPM'].sum()
monthly_working_days = monthly_total_days - monthly_non_working_days
monthly_working_days_per = monthly_working_days / monthly_total_days * 100

st.subheader("Group by Month")
st.data_editor(
            monthly_df,
            column_config={
                'Month': st.column_config.NumberColumn(label="Month"),
                'Days': st.column_config.NumberColumn(label="Non-Working"),
                'Working': st.column_config.NumberColumn(label="Working"),
                'DPM': st.column_config.NumberColumn(label="Total"),
                'Working %': st.column_config.NumberColumn(label="Working %", format="%.2f"),
            },
            hide_index=True,
            column_order=('Month', 'DPM', 'Working', 'Days', 'Working %'),
)

with st.container(border=True):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total", monthly_total_days)
    col2.metric("Working", monthly_working_days)
    col3.metric("Non working", monthly_non_working_days)
    col4.metric("Working %", value=f"{monthly_working_days_per:.2f}%")

# group by Name and sum Days

vacation_days = {
    'Bunis, Nikola': 25,
    'Dimitrov, Nikolay': 30,
    'Gligov, Iliyan': 25,
    'Gochev, Blagovest': 25,
    'Grigorov, Ladislav': 25,
    'Kalinov, Chavdar': 25,
    'Marinova, Pavlina': 25,
    'Obretenov, Borislav': 25,
    'Sholev, Radoslav': 25,
    'Vasilev, Ivan': 25,
    'Baruh, Ognian': 25,
    'Kostadinov, Zhivko': 25,
    'Yoncheva, Gabriela': 25,
    'Mihaylov, Zlatimir': 25,
    'Manchev, Martin': 25,
    'Lyapova, Mariya': 25,
    'Georgieva, Diyana': 25,
}

st.subheader("Group by Name")
names_df = f_df.groupby('Name')['Days'].sum().reset_index()
names_df['Vacation'] = names_df['Name'].map(vacation_days)
st.data_editor(
            names_df,
            hide_index=True,
)

# group by Name and Month and sum Days

df_grouped = f_df.groupby(['Name', 'Month'])['Days'].sum().reset_index()
months = f_df['Month'].unique()
names = df['Name'].unique()
index = pd.MultiIndex.from_product([months, names], names=['Month', 'Name'])
df_complete = df_grouped.set_index(['Month', 'Name']).reindex(index, fill_value=0).reset_index()
st.subheader("Group by Name and Month")
st.data_editor(
            df_complete,
            hide_index=True,
)