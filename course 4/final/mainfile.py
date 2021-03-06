from SearchSystems import BM25, DataSet, FastTextSearch, ElmoSearch, TfIdfSearch, Models
from configs import LOGGER
from flask import Flask
from flask import request, render_template


app = Flask(__name__)

elmo_path = 'elmo'
corpus = 'data/collection.csv'
model = 'fasttext/model.model'
models = Models(elmo_path, model, corpus=corpus)  

@app.route('/')
def index():
    return render_template('index.html'), request.args


@app.route('/result/')
def result():
    query = request.args['sentence']
    res = [(0,0,0)]
    mdls = ['Tf-Idf', 'BM25', 'FastText', 'Elmo']
    try:
        model_id = int(request.args['model']) - 1
    except:
        model_id = 0
        LOGGER.info('Пользователь не выбрал модель, устанавливаем Tf-Idf')
    LOGGER.info(f'Запрос: {query}; модель: {mdls[model_id]}')
    if model_id == 0:
        models.init_tfidf()
        res = models.tfidf.search(query)
    elif model_id == 1:
        models.init_bm25()
        res = models.bm25.search(query)
    elif model_id == 2:
        models.init_fasttext()
        res = models.fasttext.search(query)
    elif model_id == 3:
        models.init_elmo()
        res = models.elmosearch.search(query)
    LOGGER.info(f'Результаты запроса: {res}')
    return render_template('result.html', results=res, query=query)


if __name__ == '__main__':
    app.run(debug=True)
