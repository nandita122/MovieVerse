from flask import Flask, render_template, request, redirect, url_for, session
from db_config import get_connection

app = Flask(__name__)
app.secret_key = 'MovieVerse'

# ------------------ SELECT ROLE ------------------
@app.route('/select_role', methods=['GET', 'POST'])
def select_role():
    if request.method == 'POST':
        selected_role = request.form.get('role')
        session['role'] = selected_role
        return redirect(url_for('home'))
    return render_template('select_role.html')

# ------------------ REDIRECT ROOT TO SELECT ROLE ------------------
@app.route('/')
def index():
    return redirect(url_for('select_role'))

# ------------------ HOME ------------------
@app.route('/home')
def home():
    role = session.get('role')
    if role == 'admin':
        return render_template('admin_home.html')
    elif role == 'user':
        return render_template('user_home.html')
    else:
        return redirect(url_for('select_role'))

# ------------------ VIEW MOVIES ------------------
@app.route('/view_movies')
def view_movies():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view_movies.html', movies=movies)

# ------------------ ADD MOVIE ------------------
@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        duration = request.form['duration']
        rating = request.form['rating']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO movies (title, genre, duration, rating) VALUES (%s, %s, %s, %s)",
            (title, genre, duration, rating)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('view_movies'))

    return render_template('add_movie.html')

# ------------------ ADD THEATER ------------------
@app.route('/add_theater', methods=['GET', 'POST'])
def add_theater():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO theaters (name, location) VALUES (%s, %s)", (name, location))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('home'))

    return render_template('add_theater.html')

# ------------------ ADD SHOW ------------------
@app.route('/add_show', methods=['GET', 'POST'])
def add_show():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    cursor.execute("SELECT * FROM theaters")
    theaters = cursor.fetchall()

    if request.method == 'POST':
        movie_id = request.form['movie_id']
        theater_id = request.form['theater_id']
        show_time = request.form['show_time']

        cursor.execute(
            "INSERT INTO shows (movie_id, theater_id, show_time) VALUES (%s, %s, %s)",
            (movie_id, theater_id, show_time)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('home'))

    cursor.close()
    conn.close()
    return render_template('add_show.html', movies=movies, theaters=theaters)

# ------------------ VIEW SHOWS ------------------
@app.route('/shows')
def view_shows():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT s.show_id, m.title, t.name AS theater_name, s.show_time
        FROM shows s
        JOIN movies m ON s.movie_id = m.movie_id
        JOIN theaters t ON s.theater_id = t.theater_id
    """
    cursor.execute(query)
    shows = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('shows.html', shows=shows)



# ------------------ VIEW BOOKINGS ------------------
@app.route('/bookings')
def view_bookings():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT 
            b.booking_id, 
            c.name AS customer_name, 
            m.title AS movie_title,
            t.name AS theater_name,
            s.show_time,
            seat.seat_number,
            b.booking_time
        FROM bookings b
        LEFT JOIN customers c ON b.customer_id = c.customer_id
        LEFT JOIN shows s ON b.show_id = s.show_id
        LEFT JOIN movies m ON s.movie_id = m.movie_id
        LEFT JOIN theaters t ON s.theater_id = t.theater_id
        LEFT JOIN seats seat ON b.seat_id = seat.seat_id
        ORDER BY b.booking_time DESC
    """
    cursor.execute(query)
    bookings = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('bookings.html', bookings=bookings)

# ------------------ ABOUT US ------------------
@app.route('/about', endpoint='about_us')
def about_page():
    return render_template('about_us.html')


# ------------------ RUN APP ------------------
if __name__ == '__main__':
    app.run(debug=True)
