


from unittest import TestCase

from app import app
from models import Post, db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users"""

    def setUp(self):
        """Add example User"""
        Post.query.delete()

        User.query.delete()
        
        user = User(first_name="Test", last_name="User",
        image_url="https://media.istockphoto.com/vectors/pointing-at-himself-emoticon-with-medical-mask-vector-id1270960583?k=20&m=1270960583&s=612x612&w=0&h=0iZty2D-HtlPE2yKOOJj_evYSPSkP4n7BTWaaDwKhBg=")
        
       

        db.session.add(user)
        db.session.commit()
        self.id = user.id
        self.user = user
        

        post = Post(title="First Post", content="First Post!", user_id=self.id)
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id
        

    
    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
        
         


    def test_home_page(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Blogly Recent Posts', html)
            

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test', html)
            self.assertIn('User', html)
            

    def test_show_user_form(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Create a User', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first-name": "John", "last-name": "Smith", "img-url": "https://cdn.dribbble.com/users/2598141/screenshots/12479673/media/2fad4b5c7e7bbc33e731692d50b7edbc.png?compress=1&resize=400x300"}
            resp = client.post('/users/new/created', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John', html)
            self.assertIn('Smith', html)

    def test_edit_user(self):
        with app.test_client() as client:
            d = {"first-name": "Joe", "last-name": "Blow", "img-url": "http://s3.amazonaws.com/pix.iemoji.com/images/emoji/apple/ios-12/256/smiling-face.png"}
            resp = client.post(f'/users/{self.id}/edit/edited', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Joe', html)
            self.assertIn('Blow', html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.get('/users/2/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Joe', html)
            self.assertNotIn('Blow', html)


    def test_show_post_form(self):
        with app.test_client() as client:
            
            resp = client.get(f'/users/{self.id}/posts/new')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Title', html) 
            self.assertIn('Content', html)

    
    def test_create_new_post(self):
        with app.test_client() as client:
            d = {"title": "Test Title", "content":"Test content!, user"}
            resp = client.post(f'/users/{self.id}/posts/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Title', html) 

    def test_edit_post(self):
        with app.test_client() as client:
             d = {"title": "Change Post", "content":"Post changed"}
             resp = client.post(f'/posts/{self.post_id}/edit', data=d, follow_redirects=True)
             html = resp.get_data(as_text=True)
             
             self.assertEqual(resp.status_code, 200)
             self.assertIn('Change Post', html)
             self.assertNotIn('First Post', html)

    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}/delete', follow_redirects=True)
            
            
            self.assertEqual(resp.status_code, 302)

    def test_updated_user_page(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Change Post', html)
            





             



    
  
  
  
  
  
  
    

        


       





            




      










