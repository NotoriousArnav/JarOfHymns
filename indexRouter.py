from flask import render_template
router_BaseURL='/'

def Index():
    return render_template('index.jinja')
