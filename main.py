from flask import Flask, render_template, request, redirect, url_for
app=Flask(__name__)
yourMessage=[]
yourMessage.append("")

@app.route('/')
def home():
    return render_template('index.html',yourMessage=yourMessage)
@app.route('/createMessage',methods=['post'])
def createMessage():
    message=request.form.get('message')
    yourMessage[0]=message
    return redirect(url_for('home'))
@app.route('/delete')
def delete():
    yourMessage[0]=""
    return redirect(url_for('home'))

if __name__=='__main__':
    app.run(debug=True)