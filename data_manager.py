import connection
import hashing_utility


@connection.connection_handler
def get_questions(cursor):
    cursor.execute("""
                        SELECT * FROM question;
                               """)
    questions = cursor.fetchall()
    return questions

@connection.connection_handler
def get_questions_by_user(cursor, user_name):
    cursor.execute("""
                        SELECT id, title, submission_time, view_number, vote_number FROM question WHERE user_name ='%s';
                               """ % (user_name))
    questions = cursor.fetchall()
    return questions

@connection.connection_handler
def get_answers_by_user(cursor, user_name):
    cursor.execute("""
                        SELECT id, question_id, submission_time, vote_number FROM answer WHERE user_name ='%s';
                               """ % (user_name))
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def add_question(cursor, new_question):
    placeholders = ', '.join(['%s'] * len(new_question))
    columns = ', '.join([x[0] for x in new_question])
    sql = "INSERT INTO %s ( %s ) VALUES ( %s ) RETURNING * ;" % ('question', columns, placeholders)

    cursor.execute(sql, [y[1] for y in new_question])
    rows = cursor.fetchall()
    id = max([row['id'] for row in rows])
    return id
# sprawdzic czy to bezpiyeczne


@connection.connection_handler
def edit_question(cursor, question_id, new_submission_time, new_title, new_message):
    cursor.execute(""" 
                        UPDATE question 
                        SET submission_time = %(new_submission_time)s, title = %(new_title)s, message = %(new_message)s
                        WHERE question.id = %(question_id)s;
                         """,
                   {'new_submission_time': new_submission_time, 'new_title': new_title, 'new_message': new_message,
                    'question_id': question_id})



@connection.connection_handler
def get_question_info(cursor, question_id):
    cursor.execute("""
                        SELECT question.title, question.message, question.id FROM question
                        where question.id = %(question_id)s;
                               """, {'question_id': question_id})

    question_info = cursor.fetchall()
    print(question_info)
    return question_info


@connection.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""
                        DELETE FROM question_tag
                        WHERE question_tag.question_id = %(question_id)s;
                        DELETE FROM comment
                        WHERE comment.question_id = %(question_id)s;
                        DELETE FROM answer
                        WHERE answer.question_id = %(question_id)s;
                        DELETE FROM question
                        WHERE question.id = %(question_id)s
           
                               """, {'question_id': question_id})


@connection.connection_handler
def get_answer_info(cursor, question_id):
    cursor.execute("""
                        SELECT answer.message FROM answer
                        where answer.question_id = %(question_id)s;
                               """, {'question_id': question_id})

    answer_info = cursor.fetchall()
    return answer_info

@connection.connection_handler
def add_answer_to_db(cursor, new_answer):
    placeholders = ', '.join(['%s'] * len(new_answer))
    columns = ', '.join([x[0] for x in new_answer])
    sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % ('answer', columns, placeholders)

    cursor.execute(sql, [y[1] for y in new_answer])

@connection.connection_handler
def search_questions(cursor, phrase):
    sql = '''select distinct question.id, question.title, question.message from question
            left join answer on answer.question_id = question.id
            WHERE question.message LIKE '%%%s%%' OR question.title LIKE '%%%s%%' OR answer.message LIKE '%%%s%%' 
            ORDER BY question.id;''' % (phrase, phrase, phrase)
    cursor.execute(sql)
    questions = cursor.fetchall()

    return questions


@connection.connection_handler
def check_user(cursor, register_form):
    cursor.execute("""
     SELECT user_name, email FROM users WHERE user_name = '%s' OR email = '%s'
    """ % (register_form['user_name'], register_form['email']))

    compare_result = cursor.fetchall()
    if len(compare_result) == 0:
        add_user(register_form)
        return 'registration successfull'
    else:
        return 'user with these data already exist'


@connection.connection_handler
def check_login_user_name(cursor, login_data):
    cursor.execute("""
     SELECT user_name FROM users WHERE user_name = '%s' 
    """ % (login_data['user_name']))

    compare_result = cursor.fetchall()
    if len(compare_result) == 0:
        return False
    else:
        return True

@connection.connection_handler
def check_login_password(cursor, login_data):
    cursor.execute("""
    SELECT password FROM users WHERE user_name = '%s'
     """ % (login_data['user_name']))
    db_password = cursor.fetchall()
    if len(db_password) == 0:
        return False
    else:
        compare = hashing_utility.verify_password(login_data['password'],db_password[0]['password'])
        print(compare)
        return compare


@connection.connection_handler
def add_user(cursor, register_form):
    hashed_password = hashing_utility.hash_password(register_form['password'])
    cursor.execute("""
                        INSERT INTO users (password, name, user_name, email) VALUES ('%s', '%s', '%s', '%s')"""
                   % (hashed_password, register_form['name'], register_form['user_name'],
                      register_form['email']))
