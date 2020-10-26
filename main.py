from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
import json
import os
app = Flask(__name__)
app.secret_key = 'abrakadabra'

@app.route("/")
def index():
    print(session.keys())
    return render_template("index.html", codes=session.keys())


@app.route("/your-url", methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)
                session[request.form['code']] = True
        if request.form['code'] in urls.keys():
            flash('Такое короткое имя уже существует. Введите другое')
            return redirect(url_for('index'))

        urls[request.form['code']] = {'url': request.form['url']}
        print(urls)
        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)

        return render_template("your_url.html", code=request.form['code'])
    else:
        return redirect(url_for('index'))


@app.route("/<string:code>")
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
    return abort(404)


@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))


@app.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404