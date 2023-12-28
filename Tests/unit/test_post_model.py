from models import Pet

def test_post_model():
    post = Pet('Leo', 4,'Male','Dog','Husky','Healthy','Trained','Charlotte','North Carolina','He is a goodest boy', 1,'')

    assert post.pet_name == 'Leo'
    assert post.pet_age == 4
    assert post.pet_gender == 'Male'
    assert post.pet_type == 'Dog'
    assert post.pet_breed == 'Husky'
    assert post.pet_health == 'Healthy'
    assert post.pet_training == 'Trained'
    assert post.city == 'Charlotte'
    assert post.state == 'North Carolina'
    assert post.pet_about == 'He is a goodest boy'
    assert post.pet_owner == 1
    assert post.photo == ''