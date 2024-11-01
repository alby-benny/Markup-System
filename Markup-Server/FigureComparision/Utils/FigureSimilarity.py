import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#nltk.download('stopwords')
#nltk.download('punkt')

# Sample paragraphs
def preprocess(paragraph):
    stop_words = set(stopwords.words('english'))
    words = nltk.word_tokenize(paragraph.lower())
    words = [word for word in words if word.isalnum() and word not in stop_words]
    return ' '.join(words)

def similarity(fd_pdf,fd_ans):
    ans_keys=list(fd_ans.keys())
    pdf_keys=list(fd_pdf.keys())
    fd_sim={}
    for i in ans_keys:
        paragraph1=fd_ans[i]
        paragraph2=fd_pdf[i]



        preprocessed_paragraph1 = preprocess(paragraph1)
        preprocessed_paragraph2 = preprocess(paragraph2)
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([preprocessed_paragraph1, preprocessed_paragraph2])

        # Compute cosine similarity
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

        fd_sim[i]=cosine_sim[0][0]
    return fd_sim