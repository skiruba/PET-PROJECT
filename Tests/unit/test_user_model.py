
from models import User

def test_user_model():
    user = User('asimsid', 'thePassword','Asim','Siddique',25,'Male','asim.frost@yahoo.com')

    assert user.user_username == 'asimsid'
    assert user.user_password == 'thePassword'
    assert user.first_name == 'Asim'
    assert user.last_name == 'Siddique'
    assert user.user_age == 25
    assert user.user_gender == 'Male'
    assert user.user_email_address == 'asim.frost@yahoo.com'