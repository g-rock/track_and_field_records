from flask import Flask, render_template, request, make_response, flash
import StringIO
from helper_methods.track import update_records

app = Flask(__name__)
app.config.update(
        SECRET_KEY='poop'
)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('get.html')
    if request.method == 'POST' and len(request.files.keys()) == 2:
        tfrrs_file = request.files['tfrrs']
        record_file = request.files['record']
        df = update_records(tfrrs_file, record_file, request.form.get('linkCheckbox'), request.form.get('relayCheckbox'))
        resp = make_response(df.to_csv(header=False, index=False, line_terminator='\n'))
        resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp
    if request.method == 'POST' and len(request.files.keys()) < 2:
        flash("Make sure you upload the correct files.")
        return render_template('get.html')



if __name__ == '__main__':

    app.run()