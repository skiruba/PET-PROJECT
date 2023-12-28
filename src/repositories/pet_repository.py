from models import User, Pet, Comment
from models import db
from sqlalchemy import update, delete
import os

class PetRepository:

    def create_user(self, user_username, user_password, first_name, last_name, user_age, user_gender, user_email_address):
        new_user = User(user_username=user_username, user_password=user_password, first_name=first_name, last_name=last_name, user_age=user_age, user_gender=user_gender, user_email_address=user_email_address)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def update_user(self, user_id, first_name, last_name, user_age, user_gender, user_email_address):
        #new_user = User(first_name=first_name, last_name=last_name, user_age=user_age, user_gender=user_gender, user_email_address=user_email_address)
        upd = update(User)
        upd = upd.values(first_name=first_name, last_name=last_name, user_age=user_age, user_gender=user_gender, user_email_address=user_email_address)
        upd = upd.where(User.user_id == user_id)
        db.session.execute(upd)
        db.session.commit()
        return 1

    def create_pet(self, pet_name, pet_age, pet_gender, pet_type, pet_breed, pet_health, pet_training, city, state, pet_about, pet_owner, photo):
        new_pet = Pet(pet_name=pet_name, pet_age=pet_age, pet_gender=pet_gender, pet_type=pet_type, pet_breed=pet_breed, pet_health=pet_health, pet_training=pet_training, city=city, state=state, pet_about=pet_about, pet_owner=pet_owner, photo=photo)
        db.session.add(new_pet)
        db.session.commit()
        return new_pet

    def update_pet(self, pet_id, pet_name, pet_age, pet_gender, pet_type, pet_breed, pet_health, pet_training, city, state, pet_about):
        upd = update(Pet)
        upd = upd.values(pet_name=pet_name, pet_age=pet_age, pet_gender=pet_gender, pet_type=pet_type, pet_breed=pet_breed, pet_health=pet_health, pet_training=pet_training, city=city, state=state, pet_about=pet_about)
        upd = upd.where(Pet.pet_id == pet_id)
        db.session.execute(upd)
        db.session.commit()
        return 1

    def update_comment(self, comment_content, comment_id):
        upd = update(Comment)
        upd = upd.values(comment_content = comment_content)
        upd = upd.where(Comment.comment_id == comment_id)
        db.session.execute(upd)
        db.session.commit()
        return 1

    def create_comment(self, author_id, comment_content, post_id):
        new_comment = Comment(author_id=author_id, comment_content=comment_content, post_id=post_id)
        db.session.add(new_comment)
        db.session.commit()
        return new_comment
    
    def get_user(self, user_id):
        result = User.query.get_or_404(user_id)
        return result
    
    def get_all_pets(self):
        all_pets = Pet.query.all()
        return all_pets

    def get_pets_by_type(self, pet_type):
        pets = db.session.query(Pet).filter(Pet.pet_type == pet_type)
        return pets

    def get_my_listings(self, user_id):
        results = db.session.query(Pet).filter(Pet.pet_owner == user_id)
        return results

    def get_pet(self, pet_id):
        #result = db.session.query(Pet).filter_by(Pet.pet_id == 7)
        #result = Pet.query.get_or_404(pet_id)
        result = db.session.query(Pet, User).filter(Pet.pet_id == pet_id, Pet.pet_owner == User.user_id).all()
        return result

    def get_comments(self, pet_id):
        result = db.session.query(Comment, User).filter(Comment.post_id == pet_id, Comment.author_id == User.user_id).all()
        return result

    def get_comment_by_id(self, comment_id):
        result = Comment.query.get_or_404(comment_id)
        return result

    def delete_pet(self,pet_id):
        
        #get all comments for pet and delete
        dele = delete(Comment).where(Comment.post_id == pet_id)
        db.session.execute(dele)
        #db.session.commit()

        single_pet = Pet.query.get_or_404(pet_id)
        os.remove(os.path.join('./static/' + single_pet.photo))

        dele = delete(Pet).where(Pet.pet_id == pet_id)
        db.session.execute(dele)
        db.session.commit()
        return 1

    def delete_comment(self,comment_id,user_id):
        comment = pet_repository_singleton.get_comment_by_id(comment_id)
        if(comment.author_id == user_id):
            dele = delete(Comment).where(Comment.comment_id == comment_id)
            db.session.execute(dele)
            db.session.commit()
            return 1
        else:
            return 0

    def delete_user(self, user_id):
        dele = delete(User).where(User.user_id == user_id)
        db.session.execute(dele)
        db.session.commit()
        return 1



# Singleton to be used in other modules
pet_repository_singleton = PetRepository()
