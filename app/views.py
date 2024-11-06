# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import jsonify, render_template, request, redirect, url_for, flash, session, Flask
from jinja2  import TemplateNotFound
from datetime import datetime
import os
import pandas as pd
import json
# import requests


# App modules
from app import app, cursor, conn
# from app.models import Profiles

# set a global variable for the userID
CURRENT_UID = "1234"
# MAKE A ROUTE TO CHANGE THIS VALUE ONCE THE LOGIN PAGE IS CREATED
@app.route('/successPage')
def successPage():
    return render_template('successPage.html')

@app.route('/')
def indexFunction():
    return render_template('studentLogin.html')

@app.route('/studentLogin', methods=['GET', 'POST'])

def studentLogin():

    if request.method == 'POST':

        email = request.form['email']

        password = request.form['password']

 

        try:

            # Query the database for the user with the provided email and password

            sql = "SELECT * FROM Student WHERE Email = ? AND Password = ?"

            cursor.execute(sql, (email, password))

            user = cursor.fetchone()

       

            if user:

                # Convert the Row object to a dictionary

                user_dict = {

                    'id': user[0],

                    'name': user[1],

                    'email': user[2],

                    'password': user[3]

                }

                # Store user information in session

                session['user'] = user_dict

                print("User session set:", session['user'])

                flash('Login successful!', 'success')

                return redirect(url_for('index'))

            else:

                flash('Incorrect email or password. Please try again.', 'error')

                return redirect(url_for('studentLogin'))

        except Exception as e:

            print(f"Error: {e}")

            flash('An error occurred: {}'.format(str(e)), 'error')

            return redirect(url_for('studentLogin'))

 

    return render_template('studentLogin.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/index')
def index():
    return render_template('index.html')

# @app.route('/test2/<string:beingEval>/<string:evaluatorName>')
# def test2(beingEval, evaluatorName):
#     return render_template('test2.html', beingEval=beingEval, evaluatorName=evaluatorName)
 
 
@app.route('/get_evaluations', methods = ['GET']) 
def get_evaluations():
    try:
        evaluatorName = request.args.get("evaluatorName")
        print(evaluatorName)
        # sql = "select SID_BeingEval, SID_Evaluating, Status, Due_Date from Scheduled_Eval where SID_Evaluating = ?"
        cursor.execute("select Student_Being_Evaluated_Name, Student_Evaluating_Name, Status, Due_Date from Scheduled_Eval where Student_Evaluating_Name = ?", evaluatorName)
        evaluations = cursor.fetchall()
        print(evaluations)
        evaluations = [
            {"Student_Being_Evaluated_Name": row.Student_Being_Evaluated_Name, "Student_Evaluating_Name": row.Student_Evaluating_Name, "Status": row.Status, "Due_Date": row.Due_Date}
            for row in evaluations
        ]
        print("i reach here")
        return jsonify(evaluations)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

# @app.route('/evaluation_form', methods = ['GET'])
# def evaluation_form():
#     firstName = request.args.get("firstName")
#     lastName = request.args.get("lastName")
#     print(firstName)
#     print(lastName)
#     return render_template('test2.html')

@app.route('/test_input_content', methods=('POST', 'GET'))
def test_input_content():
    inputContent = request.form.get("sampleInput")
    inputContentTwo = request.form.get("sampleInputTwo")
    print(inputContent)
    print(inputContentTwo)
    sql = """
CREATE TABLE LaasiIsGonnaSlayTechTut (
    ID INT,
    FName VARCHAR(100),
    LName VARCHAR(100)
);
"""
    cursor.execute(sql)
    # sql = "INSERT INTO test_table (inputContent1, inputContent2) VALUES (%s, %s)"
    # cursor.execute(sql, [inputContent, inputContentTwo])
    conn.commit()
    # print(sql)
    # print(inputContent)

    return "test completed!"

app.secret_key = 'your_secret_key'

 

# @app.route('/studentLogin', methods=['GET', 'POST'])

# def studentLogin():

#     if request.method == 'POST':
#         print("reached 1")
#         email = request.form['email']

#         password = request.form['password']
#         print("reached 2")
#         print(email)

       

#         try:

#             # Query the database for the user with the provided email and password

#             sql = "SELECT * FROM Student WHERE Email = %s AND Password = %s"

#             cursor.execute(sql, (email, password))

#             user = cursor.fetchone()
#             print("look here")
#             print(user['Student_Name'])

           

#             if user:

#                 # Store user information in session

#                 session['user'] = user

#                 print("User session set:", session['user'])

#                 flash('Login successful!', 'success')

#                 return redirect(url_for('test'))

#             else:

#                 flash('Incorrect email or password. Please try again.', 'error')

#                 return redirect(url_for('studentLogin'))

#         except Exception as e:

#             flash('An error occurred: {}'.format(str(e)), 'error')

#             return redirect(url_for('studentLogin'))

 

#     return render_template('studentLogin.html')
#     # return render_template('test.html', )

 

if __name__ == '__main__':

    app.run(debug=True)





@app.route('/form/<string:beingEval>/<string:evaluatorName>')
def form(beingEval, evaluatorName):
    try:
        # student_being_evaluated = request.args.get('beingEval')
        return render_template('form.html', student_name=beingEval, evaluator_name=evaluatorName)

    except Exception as e:

        print(f"Error: {e}")

        return "An error occurred", 500




@app.route('/submit_evaluation/<evaluator_name>', methods=['POST'])

def submit_evaluation(evaluator_name):

    if request.method == 'POST':

        try:

            # Fetch data from the form

            Team_Member_Name = request.form['Team_Member_Name']

            Group_Effort_Peer = int(request.form['topic1'])

            Completes_Tasks_On_Time_Peer = int(request.form['topic2'])

            Provides_Useful_Feedback_Peer = int(request.form['topic3'])

            Communicates_Effectively_Peer = int(request.form['topic4'])

            Accepts_Contribution_Peer = int(request.form['topic5'])

            Builds_Contributions_Peer = int(request.form['topic6'])

            Group_Role_Peer = int(request.form['topic7'])

            Clarifies_Goals_Peer = int(request.form['topic8'])

            Reports_To_Team_Peer = int(request.form['topic9'])

            Ensures_Consistency_Peer = int(request.form['topic10'])

            Positivity_Peer = int(request.form['topic11'])

            Appropriate_Assertiveness_Peer = int(request.form['topic12'])

            Appropriate_Contibution_Peer = int(request.form['topic13'])

            Manages_Conflict_Peer = int(request.form['topic14'])

            Overall_Score_Peer = int(request.form['topic15'])

 

            # cursor.execute('SELECT MAX(Eval_ID) FROM Evaluation')

            # max_eval_id = cursor.fetchone()[0]

            # if max_eval_id is None:

            #     max_eval_id = 0

            # new_eval_id = max_eval_id + 1

 

            # Print form data for debugging

            # print(f"Form Data: {new_eval_id}, {Team_Member_Name}, {Group_Effort_Peer}, {Completes_Tasks_On_Time_Peer}, {Provides_Useful_Feedback_Peer}, {Communicates_Effectively_Peer}, {Accepts_Contribution_Peer}, {Builds_Contributions_Peer}, {Group_Role_Peer}, {Clarifies_Goals_Peer}, {Reports_To_Team_Peer}, {Ensures_Consistency_Peer}, {Positivity_Peer}, {Appropriate_Assertiveness_Peer}, {Appropriate_Contibution_Peer}, {Manages_Conflict_Peer}, {Overall_Score_Peer}")
            print(f"Form Data: {Team_Member_Name}, {Group_Effort_Peer}, {Completes_Tasks_On_Time_Peer}, {Provides_Useful_Feedback_Peer}, {Communicates_Effectively_Peer}, {Accepts_Contribution_Peer}, {Builds_Contributions_Peer}, {Group_Role_Peer}, {Clarifies_Goals_Peer}, {Reports_To_Team_Peer}, {Ensures_Consistency_Peer}, {Positivity_Peer}, {Appropriate_Assertiveness_Peer}, {Appropriate_Contibution_Peer}, {Manages_Conflict_Peer}, {Overall_Score_Peer}")

 

            # Insert data into the Evaluation table

            sql = '''

                INSERT INTO Evaluation (Team_Member_Name, Group_Effort_Peer, Completes_Tasks_On_Time_Peer, Provides_Useful_Feedback_Peer, Communicates_Effectively_Peer, Accepts_Contribution_Peer, Builds_Contributions_Peer, Group_Role_Peer, Clarifies_Goals_Peer, Reports_To_Team_Peer, Ensures_Consistency_Peer, Positivity_Peer, Appropriate_Assertiveness_Peer, Appropriate_Contibution_Peer, Manages_Conflict_Peer, Overall_Score_Peer)

                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

            '''
            # sql = '''

            #     INSERT INTO Evaluation (Eval_ID, Team_Member_Name, Group_Effort_Peer, Completes_Tasks_On_Time_Peer, Provides_Useful_Feedback_Peer, Communicates_Effectively_Peer, Accepts_Contribution_Peer, Builds_Contributions_Peer, Group_Role_Peer, Clarifies_Goals_Peer, Reports_To_Team_Peer, Ensures_Consistency_Peer, Positivity_Peer, Appropriate_Assertiveness_Peer, Appropriate_Contibution_Peer, Manages_Conflict_Peer, Overall_Score_Peer)

            #     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

            # '''


            sql1 = '''
                UPDATE Scheduled_Eval
                SET Status = 'Complete'
                WHERE Student_Being_Evaluated_Name = ?
                AND Student_Evaluating_Name = ?;      
                '''
            cursor.execute(sql1, (Team_Member_Name, evaluator_name))

            # cursor.execute(sql, (new_eval_id, Team_Member_Name, Group_Effort_Peer, Completes_Tasks_On_Time_Peer, Provides_Useful_Feedback_Peer, Communicates_Effectively_Peer, Accepts_Contribution_Peer, Builds_Contributions_Peer, Group_Role_Peer, Clarifies_Goals_Peer, Reports_To_Team_Peer, Ensures_Consistency_Peer, Positivity_Peer, Appropriate_Assertiveness_Peer, Appropriate_Contibution_Peer, Manages_Conflict_Peer, Overall_Score_Peer))
            cursor.execute(sql, (Team_Member_Name, Group_Effort_Peer, Completes_Tasks_On_Time_Peer, Provides_Useful_Feedback_Peer, Communicates_Effectively_Peer, Accepts_Contribution_Peer, Builds_Contributions_Peer, Group_Role_Peer, Clarifies_Goals_Peer, Reports_To_Team_Peer, Ensures_Consistency_Peer, Positivity_Peer, Appropriate_Assertiveness_Peer, Appropriate_Contibution_Peer, Manages_Conflict_Peer, Overall_Score_Peer))

            conn.commit()

 

            flash('Evaluation submitted successfully!', 'success')
            return render_template('index.html')

            # return redirect(url_for('form', student_being_evaluated=Team_Member_Name))

        except Exception as e:

            conn.rollback()

            print(f"Error: {e}")

            flash(f"An error occurred: {e}", 'error')

            return f"An error occurred: {e}", 500

 

    # return render_template('success.html')


 