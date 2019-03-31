from flask import Flask
from flask import *
import bd
import sqlite3
from flask import render_template


app = Flask(__name__)
HOST = '127.0.0.1'
PORT = 8080

mybd = sqlite3.connect('users.db', check_same_thread=False)
user = bd.UserModel(mybd)
user.init_table()
table_films = bd.FilmModel(mybd)
table_films.init_table()
table_comm = bd.CommentModel(mybd)
table_comm.init_table()
nic = ''


@app.route('/form_sample', methods=['POST', 'GET'])
def form_sample():
    if request.method == 'GET':
        return '''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport"
                            content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                            href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                            integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                            crossorigin="anonymous">
                            <title>Регистрация</title>
                          </head>
                          <body>
                            <h1>Вы не зарегистрированы в системе КиноКрит!</h1>
                            <form method="post">
                              <div class="form-group">
                                <div class="form-group col-md-5">
                                  <label for="inputEmail4">Email</label>
                                  <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                                </div>
                                <div class="form-group col-md-5">
                                  <label for="inputPassword4">Password</label>
                                  <input type="password" class="form-control" id="password" placeholder="Введите пароль" name="password">
                                </div>
                              </div>
                              <div class="form-group col-md-5">
                                <label for="nic">Nic</label>
                                <input type="text" class="form-control" id="nic" aria-describedby="emailHelp" placeholder="Введите Ваш ник" name="nic">
                              </div>
                              <div class="form-group">
                                <div class="form-group col-md-5">
                                    <label for="about">Немного о себе</label>
                                    <textarea class="form-control" id="about" rows="3" name="about"></textarea>
                                </div>
                                <div class="form-group col-md-4">
                                  <label for="classSelect">Возраст</label>
                                  <select id="classSelect" class="form-control">
                                    <option selected>Меньше 14</option>
                                    <option>14</option>
                                    <option>15</option>
                                    <option>16</option>
                                    <option>17</option>
                                    <option>18</option>
                                    <option>Больше 18</option>
                                  </select>
                                </div>
                              </div>
                              <div class="form-group col-md-5">
                                    <label for="form-check">Укажите пол</label>
                                    <div class="form-check">
                                      <input class="form-check-input" type="radio" name="sex" id="male" value="male" checked>
                                      <label class="form-check-label" for="male">
                                        Мужской
                                      </label>
                                    </div>
                                    <div class="form-check">
                                      <input class="form-check-input" type="radio" name="sex" id="female" value="female">
                                      <label class="form-check-label" for="female">
                                        Женский
                                      </label>
                                    </div>
                              </div>
                              <button type="submit" class="btn btn-outline-success col-md-2">Регистрация</button>
                            </form>
                            </form>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        global nic
        nic = request.form['nic']

        user.insert(request.form['nic'], request.form['password'],
                    request.form['class'], request.form['email'], request.form['sex'])

        return redirect('/profile/' + request.form['nic'])


@app.route('/auth', methods=['POST', 'GET'])
def auth():
    if request.method == 'GET':
        return '''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport"
                                content="width=device-width, initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                crossorigin="anonymous">
                                <title>Вход</title>
                              </head>
                              <body>
                                <h1>Вход в систему КиноКрит</h1>
                                <form method="post">
                                    <input type="text" class="form-control col-md-5" id="nic" placeholder="Введите ник" name="nic">
                                    <input type="text" class="form-control col-md-5" id="passwd" placeholder="Введите пароль" name="passwd">
                                    <button type="submit" class="btn btn-success" name = "Rgt" value = "a" >Войти</button>
                                    <button type="submit" class="btn btn-info" name = "Rgt" value = "b" >Зарегистрироваться</button>
                                </form>
                              </body>
                            </html>'''
    elif request.method == 'POST':
        global nic
        nic = request.form['nic']
        button = request.form["Rgt"]
        if button == "a":
            if user.exists(request.form['nic'], request.form['passwd'])[0] is True:
                return redirect('/profile/' + request.form['nic'])
            else:
                return redirect('/form_sample')
        else:
            return redirect('/form_sample')



@app.route('/error', methods=['POST', 'GET'])
def error():
    if request.method == 'GET':
        return '''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport"
                                content="width=device-width, initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                crossorigin="anonymous">
                                <title>Ошибка отзыва</title>
                              </head>
                              <body>
                                <h1>Извините, но вы уже отправляли отзыв на этот фильм.</h1>
                                <form method="post">
                                    <button type="submit" class="btn btn-warning">В профиль</button>
                                </form>
                              </body>
                            </html>'''
    elif request.method == 'POST':
        return redirect('/profile/' + nic)

@app.route('/error2', methods=['POST', 'GET'])
def error2():
    if request.method == 'GET':
        return '''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport"
                                content="width=device-width, initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                crossorigin="anonymous">
                                <title>Нет отзывов</title>
                              </head>
                              <body>
                                <h1>Извините, но на этот фильм нет отзывов.</h1>
                                <form method="post">
                                    <button type="submit" class="btn btn-warning">Назад</button>
                                </form>
                              </body>
                            </html>'''
    elif request.method == 'POST':
        return redirect('/comments')

@app.route('/error3', methods=['POST', 'GET'])
def error3():
    if request.method == 'GET':
        return '''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport"
                                content="width=device-width, initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                crossorigin="anonymous">
                                <title>Фильм уже есть</title>
                              </head>
                              <body>
                                <h1>Извините, но этот фильм уже добавлен.</h1>
                                <form method="post">
                                    <button type="submit" class="btn btn-warning">Назад</button>
                                </form>
                              </body>
                            </html>'''
    elif request.method == 'POST':
        return redirect('/comments')
@app.route('/error4', methods=['POST', 'GET'])
def error4():
    if request.method == 'GET':
        return '''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport"
                                content="width=device-width, initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                crossorigin="anonymous">
                                <title>Такого фильма нет</title>
                              </head>
                              <body>
                                <h1>Извините, но этот фильм не добавлен. Добавьте его пожалуйста!</h1>
                                <form method="post">
                                    <button type="submit" class="btn btn-warning">Назад</button>
                                </form>
                              </body>
                            </html>'''
    elif request.method == 'POST':
        return redirect('/addfilms')

@app.route('/error5', methods=['POST', 'GET'])
def error5():
    if request.method == 'GET':
        return '''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport"
                                content="width=device-width, initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                                crossorigin="anonymous">
                                <title>Такого фильма нет</title>
                              </head>
                              <body>
                                <h1>Извините, но пока фильмов с таким годом выпуска не добавлено.</h1>
                                <form method="post">
                                    <button type="submit" class="btn btn-warning">Назад</button>
                                </form>
                              </body>
                            </html>'''
    elif request.method == 'POST':
        return redirect('/seefilms')


@app.route('/profile/<username>', methods=['POST', 'GET'])
def profile(username):
    if request.method == 'GET':
        return '''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width,
                    initial-scale=1, shrink-to-fit=no">
                    <link rel="stylesheet"
                    href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                    crossorigin="anonymous">
                  </head>
                  <body>
                    <h1>Добро пожаловать на КиноКрит, {}</h1>
                    <form method="post">
                    <button type="submit" class="btn btn-success" name = "Rate" value = "a" >Добавить фильм</button>
                    <button type="submit" class="btn btn-info" name = "Rate" value = "b" >Прочитать отзывы</button>
                    <button type="submit" class="btn btn-danger" name = "Rate" value = "c" >Написать отзыв</button>
                    <button type="submit" class="btn btn-warning" name = "Rate" value = "d" >Библиотека фильмов</button>
                    </form>
                  </body>
                </html>'''.format(username)
    elif request.method == 'POST':
        button = request.form["Rate"]
        if button == "a":
            return redirect('/addfilms')
        elif button == "b":
            return redirect('/comments')
        elif button == "c":
            return redirect('/addcom')
        elif button == "d":
            return redirect('/seefilms')


@app.route('/addfilms', methods=['POST', 'GET'])
def films():
    if request.method == 'GET':
        return '''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width,
                    initial-scale=1, shrink-to-fit=no">
                    <link rel="stylesheet"
                    href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                    crossorigin="anonymous">
                  </head>
                  <body>
                    <h1>Добавьте фильм</h1>
                    <form method="post">
                    <div class="form-row">
                    <input type="text" class="form-control col-md-5" id="nf" placeholder="Введите название фильма" name="nf">
                    <input type="text" class="form-control col-md-5" id="genre" placeholder="Введите жанр фильма" name="genre">
                    </div>
                    <div class="form-group">
                        <label for="about">О фильме(краткое описание)</label>
                        <textarea class="form-control col-md-5" id="about" rows="2" name="about"></textarea>
                    </div>
                    <div class="form-group">
                     <input type="number" class="form-control col-md-5" id="yearf" placeholder="Введите год" name="yearf">
                    </div>
                    <button type="submit" class="btn btn-success" name = "Add" value = "a" >Добавить фильм</button>
                    <button type="submit" class="btn btn-danger" name = "Add" value = "b" >Отмена</button>
                    <form>
                  </body>
                </html>'''
    elif request.method == 'POST':
        button = request.form["Add"]
        if button == "a":
            if table_films.exists(request.form['nf'], request.form['yearf'])[0] is True:
                return redirect('/error3')
            else:
                table_films.insert(
                    request.form['nf'], request.form['genre'], request.form['about'], request.form['yearf'])
                return redirect('/profile/' + nic)
        else:
            return redirect('/profile/' + nic)


@app.route('/addcom', methods=['POST', 'GET'])
def addcom():
    if request.method == 'GET':
        return '''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width,
                    initial-scale=1, shrink-to-fit=no">
                    <link rel="stylesheet"
                    href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
                    crossorigin="anonymous">
                  </head>
                  <body>
                    <h1>Оцените фильм сами!!!</h1>
                    <form method="post">
                    <div class="form-row">
                    <input type="text" class="form-control col-md-5" id="nf" placeholder="Введите название фильма" name="nf">
                    <input type="number" class="form-control col-md-5" id="yearf" placeholder="Введите год" name="yearf">
                    </div>
                    <div class="form-group col-md-5">
                        <label for="about">   </label>
                        <label for="about">Мнение о фильме</label>
                        <textarea class="form-control" id="about" rows="3" name="about"></textarea>
                    </div>
                     <div class="form-group col-md-5">
                                    <label for="classSelect">Рейтинг</label>
                                    <select class="form-control" id="classSelect" name="class">
                                      <option>1</option>
                                      <option>2</option>
                                      <option>3</option>
                                      <option>4</option>
                                      <option>5</option>
                                    </select>
                                 </div>
                    <button type="submit" class="btn btn-success" name = "Add" value = "a" >Отправить отзыв</button>
                    <button type="submit" class="btn btn-danger" name = "Add" value = "b" >Отмена</button>
                    <form>
                  </body>
                </html>'''
    elif request.method == 'POST':
        button = request.form["Add"]
        if button == "a":
            iduser = user.get_id(nic)[0]
            if table_films.exists(request.form['nf'], request.form['yearf'])[0] is True:
                idfilm = table_films.get_id(request.form['nf'])[0]
            else:
                return redirect('/error4')


            print(iduser, idfilm)
            if table_comm.exists(idfilm, iduser )[0] is True:
                return redirect('/error')
            else:
                table_comm.insert(
                    idfilm, iduser, request.form['about'], request.form['class'])
                return redirect('/profile/' + nic)
        else:
            return redirect('/profile/' + nic)


@app.route('/comments', methods=['POST', 'GET'])
def comments():
    try:
        mas1=[]
        global rate
        rate = 0
        if table_films.exists(request.form['nf'], request.form['yearf'])[0] is True:
            idfilm = table_films.get_id(request.form['nf'])[0]
            mas1 = table_comm.get(idfilm)
            mas2 = list(table_comm.getRate(idfilm))
            print(mas2)
            sum = 0
            for i in range(len(mas2)):
                sum += mas2[i][0]
            rate = sum / len(mas2)
        mas_films = []
        for i in range(len(mas1)):

            mas_films.append({})
            mas_films[i]['nic'] = user.get(mas1[i][0])[0]
            mas_films[i]['description'] = mas1[i][1]
        for j in mas_films:
            if j['nic'] == '':
                j['nic'] = 'unknown user'
            else:
                pass
        if request.form["Go"] == "b":
                return redirect('/profile/'+nic)
        if bool(mas_films) is False:
            return redirect('/error2')

    except Exception as e:
        print(e)
        mas_films = [  # список выдуманных постов
            {
            }
        ]
    print(mas_films)
    return render_template('odd_even.html', rate = rate, films=mas_films)


@app.route('/seefilms', methods=['POST', 'GET'])
def seefilms():
    try:
        mas1=[]
        if request.form["yearf"] != "":
            mas1 = table_films.get_year(request.form["yearf"])
        else:
            mas1 = table_films.get_all()

        if request.form["Go"] == "b":
                return redirect('/profile/'+nic)
        if bool(mas1) is False:
            return redirect('/error5')
    except Exception as e:
        print(e)
    return render_template('odd_even2.html', films=mas1)



if __name__ == '__main__':
    app.run(port=PORT, host=HOST)
