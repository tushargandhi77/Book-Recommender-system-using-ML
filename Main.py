import streamlit as st
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_socres.pkl','rb'))

def recommend(user_input):
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    return data

def main():
    st.title('Book Recommender System')

    menu = ['Home', 'Recommend']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Home':
        st.subheader('Top 50 Books')
        for index, row in popular_df.iterrows():
            st.write(row['Book-Title'], 'by', row['Book-Author'])
            st.image(row['Image-URL-M'])

    elif choice == 'Recommend':
        st.subheader('Recommend a Book')
        user_input = st.text_input('Enter a book title:')
        if st.button('Recommend'):
            if user_input:
                try:
                    recommended_books = recommend(user_input)
                    if recommended_books:
                        st.write("Recommended Books:")
                        for book in recommended_books:
                            st.write(book[0], 'by', book[1])
                            st.image(book[2])
                    else:
                        st.write("No recommendations found.")
                except IndexError:
                    st.write("Book not found.")
            else:
                st.write("Please enter a book title.")

if __name__ == '__main__':
    main()
