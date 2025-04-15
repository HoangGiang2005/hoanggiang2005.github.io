#HỨA HOÀNG GIANG-2321050055

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

movies_data = pd.read_csv("https://raw.githubusercontent.com/nv-thang/Data-Visualization-Course/main/Dataset%20for%20Practice/movies.csv")
movies_data.info()
movies_data.dropna(inplace=True)

st.title("Movie Analysis")
#SIDEBAR
st.sidebar.title("SideBar")
st.sidebar.subheader("Lọc phim theo tiêu chí") 
rating = st.sidebar.multiselect("Chọn mức độ phù hợp về độ tuổi", options=movies_data["rating"].value_counts().index)
genre = st.sidebar.multiselect("Chọn thể loại", options=movies_data["genre"].value_counts().index)
year = st.sidebar.multiselect("Chọn năm", options=movies_data["year"].value_counts().sort_index().index)
st.sidebar.subheader("Phân bố điểm số của phim")
score = st.sidebar.slider("Chọn điểm số", 0.0, 10.0,None,0.1)
#Danh sách phim đã lọc theo điều kiện
if not rating and not genre and not year:
    st.subheader("Danh sách phim sau khi lọc:")
    empty_df = movies_data.loc[[], ["name", "genre", "rating", "year", "gross"]]
    st.dataframe(empty_df)  # Hiển thị bảng trống với các cột
else:
    filtered_data = movies_data
    if rating:
        filtered_data = filtered_data[filtered_data["rating"].isin(rating)]

    if genre:
        filtered_data = filtered_data[filtered_data["genre"].isin(genre)]

    if year:
        filtered_data = filtered_data[filtered_data["year"].isin(year)]

    st.subheader("Danh sách phim sau khi lọc:")
    st.dataframe(filtered_data[["name", "genre", "year", "rating", "gross"]])


st.markdown("Số lượng phim theo năm")
year_counts = movies_data["year"].value_counts().sort_index()
st.line_chart(year_counts)

avg_vote = movies_data.groupby("genre")["votes"].mean().round(2)
st.markdown("Biểu đồ thể hiện mức độ phổ biến của các thể loại phim")
st.bar_chart(avg_vote)


filtered_score = movies_data[movies_data['score'] >= score]
#BIỂU ĐỒ TẦN SUẤT
st.markdown("Biểu đồ phân bố điểm số của phim")
plt.hist(filtered_score['score'], bins=25, edgecolor='black')
plt.xlabel('Điểm số')
plt.ylabel('Số lượng phim')
plt.grid(ls="--")
st.pyplot(plt)


st.markdown("Biểu đồ phân bố doanh thu theo ngân sách")
plt.scatter(movies_data['budget'], movies_data['gross'])
plt.xlabel('Ngân sách')
plt.ylabel('Doanh thu')
st.pyplot(plt)
