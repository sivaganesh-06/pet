from flask import Flask,render_template,redirect,url_for,request,flash,abort,session,jsonify,send_file
import mysql.connector
from pymysql import IntegrityError
import mysql.connector.pooling
from flask_session import Session
from itsdangerous import URLSafeTimedSerializer
from key import salt,secret_key
from stoken import token
from cmail import sendmail
from otp import genotp
import os
import re
from io import BytesIO
app=Flask(__name__)
app.secret_key=b"\xf5\x83]\x0b\xb4N\xe2\x19Q''\x11"
#conn=mysql.connector.pooling.MySQLConnectionPool(host='localhost',user='root',password="anusha@1999",db='data',pool_name='DED',pool_size=5, pool_reset_session=True)
mydb=mysql.connector.connect(host="localhost",user="root",password="harish",db='data')

app.config['SESSION_TYPE']='filesystem'
Session(app)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/home')
def home():
    return render_template('Home.html')
@app.route('/usersignup',methods=['GET','POST'])
def user():
    if request.method=="POST":
        username=request.form['username']
        print(username)
        email=request.form['email']
        password=request.form['password']
        try:
            #mydb = conn.get_connection()
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(*) from users where username=%s',[username])
            count=cursor.fetchone()[0]
            print(count)
            if count == 1 :
                raise Exception
        except Exception as e:
            flash('user already existed')
            return redirect(url_for('user'))
        else:
            data={'user':username,'email':email,'password':password}
            subject='The Confirmation Link For Ecom Website'
            body=f"Click on the link to confirm {url_for('confirm',token=token(data,salt=salt),_external=True)}"
            sendmail(to=email,subject=subject,body=body)
            flash('Verfication link has sent to email')
            return redirect(url_for('index'))    
    return render_template('user.html')
@app.route('/confirm/<token>')
def confirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt)
    except Exception as e:
        abort(404,'link expired')
    else:
        #
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into users(username,email,password) values(%s,%s,%s)',[data['user'],data['email'],data['password']])
        mydb.commit()
        cursor.close()
        flash('Your details has registered successfully')
        return redirect(url_for('userlogin'))
@app.route('/login',methods=['GET','POST'])
def userlogin():
    if session.get('user'):
        return redirect(url_for('home'))
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        try:
            #
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(*) from users where username=%s and password=%s',[username,password])
            count=cursor.fetchone()[0]
            print(count)
            if count==0:
                raise Exception
        except Exception as e:
            flash('username or password are incorrect')
            return redirect(url_for('userlogin'))
        else:
            session['user']=username
            if not session.get(username):
                session[username]={}
            return redirect(url_for('home'))
    return render_template('userlogin.html')
from pymysql import IntegrityError  # Import IntegrityError for handling duplicate entry error

@app.route('/addshelter', methods=['GET', 'POST'])
def addshelter():
    if request.method == 'POST':
        try:
        # Extracting form data
            name = request.form['name']
            species = request.form['species']
            breed = request.form['breed']
            age = request.form['age']
            size = request.form['size']
            personality = request.form['personality']
            location = request.form['location']
            image_url = request.files['image_url']
            history = request.files['history']
                
                # Generating filenames
            image_url_filename =image_url.filename
            history_filename = history.filename
                
                # Saving files
            path = os.path.dirname(os.path.abspath(__file__))
            static_path = os.path.join(path, 'static')
            image_url.save(os.path.join(static_path, image_url_filename))
            history.save(os.path.join(static_path, history_filename))
                
                # Retrieving shelter id
            cursor = mydb.cursor(buffered=True)
            cursor.execute('SELECT id FROM shelters WHERE email = %s', [session.get('shelter')])
            id = cursor.fetchall()[0][0]
            cursor.close()
                
                # Checking if the pet already exists
            cursor = mydb.cursor(buffered=True)
            cursor.execute('SELECT * FROM petprofiles WHERE name = %s AND shelter_id = %s', [name, id])
            existing_pet = cursor.fetchone()
            cursor.close()
                
            if existing_pet:
                    # If the pet already exists, raise an IntegrityError
                raise IntegrityError
            
        except IntegrityError as e:
            flash('Pet already added!')
            return redirect(url_for('dashboard'))
    
        except Exception as e:
            flash(f'An error occurred: {str(e)}')
            return redirect(url_for('index'))
    
        else:
        # Inserting pet profile into the database
            cursor = mydb.cursor(buffered=True)
            cursor.execute('INSERT INTO petprofiles (name, species, breed, age, size, personality,location,history, image_url, shelter_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', [name, species, breed, age, size, personality, location, history_filename, image_url_filename,  id])
            mydb.commit()
            cursor.close()
            flash('Thanks for donating!')
            return redirect(url_for('dashboard'))
    return render_template('shelter.html')
    
    

        

@app.route('/dashboard')
def dashboard():
    try:
        if session.get('user') or session.get('shelter'):
            #
            cursor = mydb.cursor(buffered=True)
            cursor.execute('select name, species, breed, age, size, location, personality, history, image_url, shelter_id, pet_id from petprofiles')
            pets = cursor.fetchall()
            cursor.close()
            return render_template('dashboard.html', pets=pets)

    except Exception as e:
        flash(f'An error occurred: {str(e)}')
        return redirect(url_for('index'))

@app.route('/shelter_registration',methods=['GET','POST'])
def shelter_registration():
    if request.method=="POST":
        name=request.form['name']
        location=request.form['location']
        contact_person=request.form['contact_person']
        email=request.form['email']
        phone_number=request.form['Phone_number']
        website=request.form['website']
        try:
            #
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(*) from shelters where name=%s',[name])
            count=cursor.fetchone()[0]
            print(count)
            if count == 1 :
                raise Exception
        except Exception as e:
            flash('user already existed')
            return redirect(url_for('shelter_registration'))
        else:
            data={'name':name,'location':location,'contact_person':contact_person,'email':email,'phone_number':phone_number,'website':website}
            subject='The Confirmation Link For Ecom Website'
            body=f"Click on the link to confirm {url_for('shelterconfirm',token=token(data,salt=salt),_external=True)}"
            sendmail(to=email,subject=subject,body=body)
            flash('Verfication link has sent to email')
            return redirect(url_for('index'))    
    return render_template('showshelter.html')
@app.route('/shelterconfirm/<token>')
def shelterconfirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt)
    except Exception as e:
        abort(404,'link expired')
    else:
        #
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into shelters(name,location,contact_person,email,phone_number,website) values(%s,%s,%s,%s,%s,%s)',[data['name'],data['location'],data['contact_person'],data['email'],data['phone_number'],data['website']])
        mydb.commit()
        cursor.close()
        flash('Your details has registered successfully')
        return redirect(url_for('shelterlogin'))
@app.route('/shelterlogin',methods=['GET','POST'])
def shelterlogin():
    if session.get('shelter'):
        return redirect(url_for('home'))
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        try:
            #
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(*) from shelters where name=%s and email=%s',[name,email])
            count=cursor.fetchone()[0]
            print(count)
            if count==0:
                raise Exception
        except Exception as e:
            flash('username or password are incorrect')
            return redirect(url_for('shelterlogin'))
        else:
            session['shelter']=email
            if not session.get(email):
                session[name]={}
            return redirect(url_for('home'))
    return render_template('shelterlogin.html')
@app.route('/petdashboard')
def petdashboard():
    try:
        #
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select p.name, p.species, p.breed, p.age, p.size, p.location, p.personality, p.history, p.shelter_id, s.name, s.phone_number, p.pet_id, p.image_url from petprofiles p join shelters s on p.shelter_id = s.id')
        pets_data = cursor.fetchall()
        cursor.close()
        return render_template('petdashboard.html', pets_data=pets_data)

    except Exception as e:
        flash(f'An error occurred: {str(e)}')
        return redirect(url_for('index'))
@app.route('/spetdashboard')
def spetdashboard():
    try:
        #
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select p.name, p.species, p.breed, p.age, p.size, p.location, p.personality, p.history, p.shelter_id, s.name, s.phone_number, p.pet_id,s.email,p.image_url from petprofiles p join shelters s on p.shelter_id = s.id')
        pets_data = cursor.fetchall()
        cursor.close()
        return render_template('spetdashboard.html', pets_data=pets_data)

    except Exception as e:
        flash(f'An error occurred: {str(e)}')
        return redirect(url_for('index'))

@app.route('/dis/<shelter_id>')
def dis(shelter_id):
    #
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select name,species,breed,age,size,location,personality,image_url,shelter_id from petprofiles where shelter_id=%s',[shelter_id])
    pets2=cursor.fetchall()
    cursor.close()
    return render_template('petdescription.html',pets2=pets2)
@app.route('/delete/<id>')
def delete(id):
    try:
        if session.get('shelter'):
            #
            cursor = mydb.cursor(buffered=True)
            cursor.execute('delete from petprofiles where pet_id=%s', [id])
            mydb.commit()
            cursor.close()
            flash(f'The pet with ID {id} has been deleted')
            return redirect(url_for('dashboard'))
        else:
            flash('You do not have permission to delete pets')
            return redirect(url_for('userlogin'))
    except Exception as e:
        flash(f'An error occurred: {str(e)}')
        return redirect(url_for('dashboard'))

    return redirect(url_for('userlogin'))
@app.route('/logout')
def logout():
    try:
        if session.get('user'):
            session.pop('user')
            return redirect(url_for('index'))
        else:
            flash('You are not logged in')
            return redirect(url_for('userlogin'))
    except Exception as e:
        flash(f'An error occurred: {str(e)}')
        return redirect(url_for('index'))

@app.route('/slogout')
def slogout():
    try:
        if session.get('shelter'):
            session.pop('shelter')
            return redirect(url_for('index'))
        else:
            flash('You are not logged in as a shelter')
            return redirect(url_for('shelterlogin'))
    except Exception as e:
        flash(f'An error occurred: {str(e)}')
        return redirect(url_for('index'))

@app.route('/updatepets/<id>', methods=['GET', 'POST'])
def updatepets(id):
    try:
        if session.get('shelter'):
            #
            cursor = mydb.cursor(buffered=True)
            cursor.execute('select name, species, breed, age, size, location from petprofiles where pet_id=%s', [id])
            data = cursor.fetchone()
            cursor.close()
            
            if request.method == 'POST':
                name = request.form['name']
                species = request.form['species']
                breed = request.form['breed']
                age = request.form['age']
                size = request.form['size']
                location = request.form['location']
                
                cursor = mydb.cursor(buffered=True)
                cursor.execute('update petprofiles set name=%s, species=%s, breed=%s, age=%s, size=%s, location=%s where pet_id=%s', [name, species, breed, age, size, location, id])
                mydb.commit()
                cursor.close()
                flash(f'Pet with ID {id} updated successfully')
                return redirect(url_for('dashboard'))
            
            return render_template('updatepets.html', data=data)
        
    except Exception as e:
        flash(f'An error occurred: {str(e)}')
        return redirect(url_for('dashboard'))


@app.route('/savedsearches', methods=['GET','POST'])
def create_saved_search():
    cursor=mydb.cursor(buffered=True)
    if session.get('user'):
        cursor.execute('select id from users where username=%s',[session.get('user')])
        id=cursor.fetchall()[0][0]
        if request.method=='POST':
            try:
           
                # Assume user_id is handled separately
                search_value = request.form['search_name']
                # Determine which parameter the user provided based on the search value
                if search_value.isdigit():
                    age = int(search_value)
                    species = breed = size = location = None
                elif search_value.isalpha():
                    species = search_value
                    breed = size = location = age= None
                else:
                    species = breed = size = location = age = None
                    location = search_value
                
            except KeyError as e:
                flash(f'Missing key in form data: {str(e)}', 'error')
                return redirect(url_for('home'))
            except Exception as e:
                flash(f'An error occurred: {str(e)}', 'error')
                return redirect(url_for('home'))
            else:
                print(id, search_value, species, breed, age, size, location)
                cursor = mydb.cursor(buffered=True)
                cursor.execute('INSERT INTO savedsearches (user_id, search_name, species, breed, age, size, location) VALUES (%s, %s, %s, %s, %s, %s, %s)',[id,search_value, species, breed, age, size, location])
                mydb.commit()
                strg=['A-Za-z0-9']
                pattern=re.compile(f'^{strg}', re.IGNORECASE)
                if (pattern.match(search_value)):
                    cursor=mydb.cursor(buffered=True)
                    cursor.execute('select p.name, p.species, p.breed, p.age, p.size, p.location, p.personality, p.history, p.shelter_id, s.name, s.phone_number, p.pet_id,p.image_url from petprofiles p join shelters s on p.shelter_id = s.id where species like %s', [search_value + '%'])
                    pets_data=cursor.fetchall()
                    cursor.close()
                    return render_template('petdashboard.html',pets_data=pets_data)

                flash('Saved search created successfully', 'success')
                return redirect(url_for('home'))
    else: 
        cursor.execute('SELECT id FROM shelters WHERE email=%s', [session.get('shelter')])
        id=cursor.fetchall()[0][0]
        if request.method=='POST':
            try:
           
                # Assume user_id is handled separately
                search_value = request.form['search_name']
                # Determine which parameter the user provided based on the search value
                if search_value.isdigit():
                    age = int(search_value)
                    species = breed = size = location = None
                elif search_value.isalpha():
                    species = search_value
                    breed = size = location = age= None
                else:
                    species = breed = size = location = age = None
                    location = search_value
                    
            except KeyError as e:
                flash(f'Missing key in form data: {str(e)}', 'error')
                return redirect(url_for('home'))
            except Exception as e:
                flash(f'An error occurred: {str(e)}', 'error')
                return redirect(url_for('home'))
            else:
                print(id, search_value, species, breed, age, size, location)
                cursor = mydb.cursor(buffered=True)
                cursor.execute('INSERT INTO savedsearches (s_id, search_name, species, breed, age, size, location) VALUES (%s, %s, %s, %s, %s, %s, %s)',[id,search_value, species, breed, age, size, location])
                mydb.commit()
                strg=['A-Za-z0-9']
                pattern=re.compile(f'^{strg}', re.IGNORECASE)
                if (pattern.match(search_value)):
                    cursor=mydb.cursor(buffered=True)
                    cursor.execute('select p.name, p.species, p.breed, p.age, p.size, p.location, p.personality, p.history, p.shelter_id, s.name, s.phone_number, p.pet_id,s.email,p.image_url from petprofiles p join shelters s on p.shelter_id = s.id where species like %s', [search_value + '%'])
                    pets_data=cursor.fetchall()
                    cursor.close()
                    return render_template('spetdashboard.html',pets_data=pets_data)
                    

                flash('Saved search created successfully', 'success')
                return redirect(url_for('home'))
        
    cursor.close()
    return render_template('Home.html')


@app.route('/adopt/<p_id>', methods=['GET', 'POST'])
def adopt(p_id): 
    print(p_id) 
    try:
        if session.get('user'):
            cursor = mydb.cursor(buffered=True)
            cursor.execute('select id from users where username=%s', [session.get('user')])
            id = cursor.fetchall()[0][0]
            cursor.execute('select name, species, breed, age, size, location, personality, image_url, shelter_id from petprofiles where pet_id=%s', [p_id])
            pet_data = cursor.fetchone()
            cursor.execute('insert into adoption(id, name, species, breed, age, size, location, description, image_url, shelter_id, user_id) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', [p_id, pet_data[0], pet_data[1], pet_data[2], pet_data[3], pet_data[4], pet_data[5], pet_data[6], pet_data[7], pet_data[8], id])
            mydb.commit()
            cursor.close()
            return redirect(url_for('uradpotion'))
        else:
            flash('You must be logged in to adopt a pet')
            return redirect(url_for('userlogin'))
    except Exception as e:
        flash(f'The pet has already adopted')
        return redirect(url_for('petdashboard'))
    #return render_template('adoptprocess.html', profile=profile)

@app.route('/uradpotion')
def uradpotion():
    if session.get('user'):
        try:
            cursor = mydb.cursor(buffered=True)
            cursor.execute('select id from users where username=%s', [session.get('user')])
            id1 = cursor.fetchone()[0]
            cursor.execute('select name, species, breed, age, size, location, description, image_url, shelter_id, user_id from adoption where user_id=%s',[id1])
            adpotions = cursor.fetchall()
            print(adpotions)
            cursor.close()
            return render_template('adoptprocess.html', adpotions=adpotions)
        except Exception as e:
            flash(f'An error occurred: {str(e)}')
            return redirect(url_for('index'))
    return redirect(url_for('userlogin'))


@app.route('/profile')
def profile():
    if session.get('user'):
        #
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select id from users where username=%s', [session.get('user')])
        id = cursor.fetchone()[0]
        cursor.execute('select u.username, u.email, a.name, a.shelter_id, a.breed, u.id from users u join adoption a on a.user_id = u.id where u.id = %s', [id])
        profiles = cursor.fetchall()
        cursor.close()
        return render_template('profile.html', profiles=profiles)
    else:
        return redirect(url_for('user_login'))


@app.route('/add', methods=['GET', 'POST'])
def add_filter():
    try:
        if request.method == 'POST':
            location = request.form['location']
            pet_type = request.form['pet_type']
            size = request.form['size']
            age = request.form['age']

            query = "INSERT INTO searchfilters (location, pet_type, size, age) VALUES (%s, %s, %s, %s)"
            values = (location, pet_type, size, age)

            # Execute the query
            #
            cursor = mydb.cursor(buffered=True)
            cursor.execute(query, values)
            mydb.commit()
            cursor.close()
            return redirect(url_for('filtersearch', location=location, pet_type=pet_type, size=size, age=age))

        return render_template('filter.html')
    except Exception as e:
        flash(f'An error occurred: {str(e)}')
        return redirect(url_for('index'))

@app.route('/filtersearch/<location>/<pet_type>/<size>/<age>', methods=['GET','POST'])
def filtersearch(location, pet_type, size, age):
    try:
        # Construct the SQL query to retrieve user's saved filters
        filter_query = "SELECT * FROM searchfilters WHERE 1=1"
        params = []

        if location:
            filter_query += " AND location = %s"
            params.append(location)
        if pet_type:
            filter_query += " AND pet_type = %s"
            params.append(pet_type)
        if size:
            filter_query += " AND size = %s"
            params.append(size)
        if age:
            filter_query += " AND age = %s"
            params.append(age)

        # Execute the query to retrieve user's saved filters
        #
        cursor = mydb.cursor(buffered=True)
        cursor.execute(filter_query, tuple(params))
        filter_results = cursor.fetchall()

        # Construct the SQL query to fetch pets matching the filters
        pet_query = "SELECT * FROM petprofiles WHERE 1=1"
        pet_params = []

        if filter_results:
            pet_query += " AND ("
            for i, result in enumerate(filter_results):
                if i > 0:
                    pet_query += " OR"
                pet_query += " (species = %s or location = %s or size = %s or age = %s)"
                pet_params.extend([result[2], result[1], result[3], result[4]])
            pet_query += ")"

        # Execute the query to fetch pets matching the filters
        if pet_params:
            cursor.execute(pet_query, pet_params)
            pet_results = cursor.fetchall()
            cursor.close()
        else:
            pet_results = []

        return render_template('results.html', results=pet_results)
    except Exception as e:
        flash(f'An error occurred: {str(e)}')
        return redirect(url_for('index'))

@app.route('/ursearches/<id>')
def ursearches(id):
    try:
        
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select * from savedsearches where user_id=%s',[id])
        ser = cursor.fetchall()
        cursor.close()
        return render_template('ursearches.html', ser=ser)
    except Exception as e:
        flash(f'An error occurred: {str(e)}')
        return redirect(url_for('index'))
@app.route('/sheltersearches/<id>')
def sheltersearches(id):
    try:
        
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select * from savedsearches where s_id=%s',[id])
        ser = cursor.fetchall()
        cursor.close()
        return render_template('ursearches.html', ser=ser)
    except Exception as e:
        flash(f'An error occurred: {str(e)}')
        return redirect(url_for('index'))

@app.route('/shprofile')
def shprofile():
    try:
        if session.get('shelter'):
            #
            cursor = mydb.cursor(buffered=True)
            cursor.execute('select id from shelters where email=%s',[session.get('shelter')])
            id = cursor.fetchall()[0][0]
            cursor.execute('select * from shelters  where id=%s',[id])
            profiles = cursor.fetchall()
            cursor.close()
            return render_template('sprofile.html', profiles=profiles)
    except Exception as e:
        flash(f'An error occurred: {str(e)}')
        return redirect(url_for('index'))
@app.route('/search',methods=['GET','POST'])
def search():
    return 'hi'  
@app.route('/smessage/<id1>/<pid>', methods=['GET', 'POST'])
def smessage(id1,pid):
    if session.get('shelter'):  # Allow both users and vendor

        cursor = mydb.cursor(buffered=True)
        cursor.execute('SELECT id FROM shelters WHERE email=%s', [session.get('shelter')])
        user_id = cursor.fetchone()[0]
        cursor.execute("SELECT * from chat_messages WHERE (sender_id = %s AND receiver_id = %s and pid=%s) ORDER BY created_at", (id1,user_id,pid))
        data = cursor.fetchall()
        
        
        cursor.execute("SELECT * from chat_messages WHERE (receiver_id = %s AND sender_id = %s and pid=%s) ORDER BY created_at", (id1,user_id,pid))
        data1 = cursor.fetchall()
        messages=data+data1
        sender = [(msg[0], msg[1],msg[2],msg[3],msg[4],msg[5]) for msg in messages if msg[2] == user_id]
        receiver = [(msg[0], msg[1],msg[2],msg[3],msg[4],msg[5]) for msg in messages if msg[2] != user_id]
        
        if request.method == 'POST':
            message = request.form['Message']
            file=request.files['file']
            filename=genotp()+'.jpg'
            path=os.path.dirname(os.path.abspath(__file__))
            static_path=os.path.join(path,'static')
            file.save(os.path.join(static_path,filename))
            cursor.execute('INSERT INTO chat_messages (sender_id, receiver_id, message,file_path,pid) VALUES (%s, %s, %s,%s,%s)', (user_id,id1, message,filename,pid))
            mydb.commit()
            cursor.execute("SELECT * from chat_messages WHERE (sender_id = %s AND receiver_id = %s and pid=%s) ORDER BY created_at", (id1,user_id,pid))
            data = cursor.fetchall()
            
            cursor.execute("SELECT * from chat_messages WHERE (receiver_id = %s AND sender_id = %s and pid=%s) ORDER BY created_at", (id1,user_id,pid))
            data1 = cursor.fetchall()
            cursor.close()
            messages=data+data1
            sender = [(msg[0], msg[1],msg[2],msg[3],msg[4],msg[5]) for msg in messages if msg[2] == user_id]
            receiver = [(msg[0], msg[1],msg[2],msg[3],msg[4],msg[5]) for msg in messages if msg[2] != user_id]
            return redirect(url_for('smessage', id1=id1,pid=pid))

        return render_template('chatting.html', sender=sender, receiver=receiver, sender_id=id1, receiver_id=user_id)
    return redirect(url_for('shelterlogin'))
@app.route('/message/<id1>/<pid>', methods=['GET', 'POST'])
def message(id1,pid):
    if session.get('user'):  # Allow both users and vendor

        cursor = mydb.cursor(buffered=True)
        cursor.execute('SELECT id FROM users WHERE username=%s', [session.get('user')])
        user_id = cursor.fetchone()[0]
        cursor.execute("SELECT * from chat_messages WHERE (sender_id = %s AND receiver_id = %s and pid=%s) ORDER BY created_at", (id1,user_id,pid))
        data = cursor.fetchall()
        
        
        cursor.execute("SELECT * from chat_messages WHERE (receiver_id = %s AND sender_id = %s and pid=%s) ORDER BY created_at", (id1,user_id,pid))
        data1 = cursor.fetchall()
        messages=data+data1
        sender = [(msg[0], msg[1],msg[2],msg[3],msg[4],msg[5]) for msg in messages if msg[2] == user_id]
        receiver = [(msg[0], msg[1],msg[2],msg[3],msg[4],msg[5]) for msg in messages if msg[2] != user_id]
        
        if request.method == 'POST':
            message = request.form['Message']
            file=request.files['file']
            filename=genotp()+'.jpg'
            path=os.path.dirname(os.path.abspath(__file__))
            static_path=os.path.join(path,'static')
            file.save(os.path.join(static_path,filename))
            cursor.execute('INSERT INTO chat_messages (sender_id, receiver_id, message,file_path,pid) VALUES (%s, %s, %s,%s,%s)', (user_id,id1, message,filename,pid))
            mydb.commit()
            cursor.execute("SELECT * from chat_messages WHERE (sender_id = %s AND receiver_id = %s and pid=%s) ORDER BY created_at", (id1,user_id,pid))
            data = cursor.fetchall()
            
            cursor.execute("SELECT * from chat_messages WHERE (receiver_id = %s AND sender_id = %s and pid=%s) ORDER BY created_at", (id1,user_id,pid))
            data1 = cursor.fetchall()
            cursor.close()
            messages=data+data1
            sender = [(msg[0], msg[1],msg[2],msg[3],msg[4],msg[5]) for msg in messages if msg[2] == user_id]
            receiver = [(msg[0], msg[1],msg[2],msg[3],msg[4],msg[5]) for msg in messages if msg[2] != user_id]
            return redirect(url_for('message', id1=id1,pid=pid))

        return render_template('chatting.html', sender=sender, receiver=receiver, sender_id=user_id, receiver_id=id1)
    return redirect(url_for('userlogin'))
@app.route('/chats/<pid>',methods=['GET','POST'])
def chats(pid):
    if session.get('shelter'):
        cursor=mydb.cursor(buffered=True)
        
        cursor.execute('SELECT id FROM shelters WHERE email=%s', [session.get('shelter')])
        user_id = cursor.fetchone()[0]
        print(user_id)
        cursor.execute('select distinct sender_id from chat_messages where receiver_id=%s and pid=%s',[user_id,pid])
        count=cursor.fetchall()
        print(count)
        cursor.close()
        if request.method=='POST':
            u_id=request.form['dropdown']
            return redirect(url_for('smessage',pid=pid,id1=u_id))
        return render_template('chats.html',count=count)
@app.route('/view_file/<fid>')
def view_file(fid):
    
    cursor = mydb.cursor(buffered=True)
    cursor.execute('SELECT history FROM petprofiles WHERE name = %s', [fid])
    data = cursor.fetchone()
    cursor.close()

    if data:
        filename = data[0]
        path = os.path.dirname(os.path.abspath(__file__))
        static_path = os.path.join(path, 'static')
        file_path = os.path.join(static_path, filename)

        try:
            with open(file_path, 'rb') as f:
                byte_data = BytesIO(f.read())
            return send_file(byte_data, download_name=filename)
        except FileNotFoundError:
            return "File not found", 404
    else:
        return "No history found for the given pet name", 404

   
app.run(debug=True,use_reloader=True)