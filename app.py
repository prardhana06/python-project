from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Predefined goals and resources
GOALS = {
    'Software Engineer': {
        'fields': [
            {'name': 'Programming Languages', 'desc': 'Core knowledge for software roles.'},
            {'name': 'Data Structures & Algorithms', 'desc': 'Foundation for technical interviews.'},
        ],
        'material': {
            'videos': [
                {'title': 'Python Crash Course', 'url': 'https://youtu.be/rfscVS0vtbw'},
                {'title': 'C++ Full Course', 'url': 'https://youtu.be/8PopR3x-VMY'}
            ],
            'ppt': [{'title': 'Python Basics PPT', 'url': '/assets/ppt/python_basics.ppt'}],
            'motivation': 'Success comes to those who never give up.',
            'interview': [
                {'q': 'What is OOP?', 'a': 'Object-oriented programming is a paradigm based on objects and classes.'},
                {'q': 'How do you manage memory in Python?', 'a': 'Python uses an automatic garbage collector.'}
            ]
        }
    },
    'Teacher': {
        'fields': [
            {'name': 'Teaching Methodologies', 'desc': 'Various approaches for effective teaching.'},
            {'name': 'Education Certifications', 'desc': 'Exams like Praxis, CSET, FTCE needed for teachers.'},
            {'name': 'Classroom Management', 'desc': 'Tips for maintaining classroom discipline and learning.'},
        ],
        'material': {
            'videos': [
                {'title': 'Teacher Training Interview', 'url': 'https://www.youtube.com/watch?v=SD7y8NE1UFo'},
                {'title': 'How to Prepare for a Teacher Interview', 'url': 'https://www.youtube.com/watch?v=c3jly1QDRbc'}
            ],
            'ppt': [{'title': 'Free Online Study Guides', 'url': 'https://www.teacherstestprep.com/free-online-study-guides'}],
            'motivation': 'Teaching is the one profession that creates all other professions.',
            'interview': [
                {'q': 'Why do you want to teach?', 'a': 'I want to inspire students and help them achieve their potential.'},
                {'q': 'How do you manage classroom discipline?', 'a': 'By setting clear expectations and enforcing them fairly.'}
            ]
        }
    },
    'Doctor': {
        'fields': [
            {'name': 'Medical Entrance Exams', 'desc': 'Details and prep for NEET, MCAT, etc.'},
            {'name': 'Clinical Skills', 'desc': 'Practice-based medical training.'},
            {'name': 'Medical Ethics', 'desc': 'Guidance for professional conduct.'},
        ],
        'material': {
            'videos': [
                {'title': 'NEET Preparation Tips', 'url': 'https://youtu.be/uXwama5k6uQ'},
            ],
            'ppt': [{'title': 'First Aid MCAT Basics', 'url': '/assets/ppt/first_aid_mcat.ppt'}],
            'motivation': 'Medicine is a science of uncertainty and an art of probability.',
            'interview': [
                {'q': 'Why do you want to become a doctor?', 'a': 'To serve people and make a difference in health outcomes.'},
            ]
        }
    },
    'Civil Services': {
        'fields': [
            {'name': 'General Studies', 'desc': 'Wide reading required for prelims and mains.'},
            {'name': 'Current Affairs', 'desc': 'Stay updated with national and international news.'},
        ],
        'material': {
            'videos': [
                {'title': 'UPSC Preparation Guidance', 'url': 'https://youtu.be/TODwFAY5A7Q'},
            ],
            'ppt': [{'title': 'UPSC Mains Strategy', 'url': '/assets/ppt/upsc_strategy.ppt'}],
            'motivation': 'Be the change you wish to see in the world.',
            'interview': [
                {'q': 'Why do you want to join civil services?', 'a': 'To serve my country and contribute to public good.'},
            ]
        }
    },
    'Data Scientist': {
        'fields': [
            {'name': 'Machine Learning', 'desc': 'Core ML algorithms and theory.'},
            {'name': 'Statistics', 'desc': 'Probability, inference, and predictive modelling.'},
            {'name': 'Data Visualization', 'desc': 'Effective representation of data insights.'},
        ],
        'material': {
            'videos': [
                {'title': 'Data Science for Beginners', 'url': 'https://youtu.be/X3paOmcrTjQ'},
            ],
            'ppt': [{'title': 'Data Science Overview', 'url': '/assets/ppt/data_science_intro.ppt'}],
            'motivation': 'Data is the new oil.',
            'interview': [
                {'q': 'What is supervised learning?', 'a': 'It is a type of ML with labeled data.'}
            ]
        }
    },
    'Mechanical Engineer': {
        'fields': [
            {'name': 'Thermodynamics', 'desc': 'Principles of heat, energy, and work.'},
            {'name': 'Design & Manufacturing', 'desc': 'Product design and fabrication techniques.'},
        ],
        'material': {
            'videos': [
                {'title': 'Thermodynamics Course', 'url': 'https://youtu.be/1nzrTV1q6hw'},
            ],
            'ppt': [{'title': 'Engineering Drawing', 'url': '/assets/ppt/engg_drawing.ppt'}],
            'motivation': 'Engineering is the art of directing great sources of power for the use and convenience of man.',
            'interview': [
                {'q': 'What is entropy?', 'a': 'Entropy measures system disorder.'}
            ]
        }
    },
    'Entrepreneur': {
        'fields': [
            {'name': 'Business Planning', 'desc': 'How to write a business plan.'},
            {'name': 'Startup Funding', 'desc': 'Pitching and raising funds.'},
        ],
        'material': {
            'videos': [
                {'title': 'How to Start a Startup', 'url': 'https://youtu.be/CBYhVcO4WgI'},
            ],
            'ppt': [{'title': 'Business Model Canvas', 'url': '/assets/ppt/business_model_canvas.ppt'}],
            'motivation': 'Dream big. Start small. Act now.',
            'interview': [
                {'q': 'What is an MVP?', 'a': 'A Minimum Viable Product is the simplest version of a product.'}
            ]
        }
    },
}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('goal'))
        else:
            return "Invalid Login"
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/goal', methods=['GET', 'POST'])
def goal():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        goal = request.form['goal']
        duration = request.form['duration']
        if goal not in GOALS:
            return f"This goal is not supported yet. Supported: {', '.join(GOALS.keys())}"
        conn = get_db_connection()
        conn.execute('INSERT INTO goals (user_id, goal, duration) VALUES (?, ?, ?)', (session['user_id'], goal, duration))
        conn.commit()
        conn.close()
        session['goal'] = goal
        return redirect(url_for('fields'))
    return render_template('goal.html', goals=GOALS.keys())

@app.route('/fields')
def fields():
    if 'goal' not in session or session['goal'] not in GOALS:
        return redirect(url_for('goal'))
    return render_template('fields.html', fields=GOALS[session['goal']]['fields'])

@app.route('/materials')
def materials():
    field_name = request.args.get('field')
    user_goal = session.get('goal')
    if user_goal not in GOALS:
        return redirect(url_for('goal'))
    material = GOALS[user_goal]['material']
    return render_template('materials.html', material=material)

@app.route('/assets/<path:filename>')
def assets(filename):
    from flask import send_from_directory
    return send_from_directory('../frontend/assets', filename)

if __name__ == '__main__':
    app.run(debug=True)
