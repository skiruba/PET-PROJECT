def test_faq_page(test_app):
    res = test_app.get('/faq')

    assert res.status_code == 200
    assert b'Frequently Asked Questions' in res.data
    assert b'What should I know before adopting?' in res.data
    assert b'What is the process like?' in res.data
    assert b'How many animals can I adopt?' in res.data
    assert b'Are there appointments to go see an animal?' in res.data

def test_about_us(test_app):
    res = test_app.get('/aboutus')

    assert res.status_code == 200
    assert b'Pet Finder - About Us' in res.data
    assert b'We are a group of passionate people who want to' in res.data

def test_learn(test_app):
    res = test_app.get('/external-sources')

    assert res.status_code == 200
    assert b'Caring for your Dog' in res.data
    assert b'Learn about dog breeds that fit your family and lifestyle' in res.data
    assert b'Emergency Services' in res.data


def test_browse(test_app):
    res = test_app.get('/browse')

    assert b'Browse Pets' in res.data
    assert b'Pet Type' in res.data


def test_create_user(test_app):
    res = test_app.post('/reguser', data={

        'user_username':'khaill',
        'user_password':'abc123',
        'first_name': 'John',
        'last_name': 'Snow',
        'user_age': 25,
        'user_gender': 'Male',
        'user_email_address': 'john.snow@gmail.com',
    },follow_redirects=True)

    assert res.status_code == 200
    
    

    
def test_login(test_app):
    res = test_app.post('/login', data={
        'user_username':'khaill',
        'user_password':'abc123',
    },follow_redirects=True)

    assert res.status_code == 200
    
    #redirect to home page
    assert b'Adopting' in res.data
    assert b'Listing' in res.data



def test_edit_user(test_app):
    res = test_app.post('/account', data={
        'first_name': 'Edith',
        'last_name': 'Snow',
        'user_age': 45,
        'user_gender': 'Male',
        'user_email_address': 'john.snow@gmail.com',
    })
    
    assert b'Edith' in res.data
    assert b'45' in res.data



def test_pet_post_form(test_app):
    res = test_app.get('/petpost')

    assert b'Post Your Pet For Sale' in res.data
    assert b'Pet Type' in res.data
    assert b'Pet Training' in res.data
    assert b'Pet Health' in res.data
    assert b'Tell Us About Your Pet' in res.data




