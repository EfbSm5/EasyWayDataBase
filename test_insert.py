from create_app import create_app, db
from models.user import User
from models.comment import Comment
from models.easypoint import EasyPoint
from models.dynamicpost import DynamicPost

app = create_app()

def create_test_data():
    with app.app_context():
        # 创建测试用户
        user1 = User(name="Alice", avatar="https://27142293.s21i.faiusr.com/2/ABUIABACGAAg_I_bmQYokt25kQUwwAc4gAU.jpg")
        user2 = User(name="Bob", avatar="https://bkimg.cdn.bcebos.com/pic/5882b2b7d0a20cf43289a8ce7d094b36acaf9981?x-bce-process=image/format,f_auto/watermark,image_d2F0ZXIvYmFpa2UyNzI,g_7,xp_5,yp_5,P_20/resize,m_lfit,limit_1,h_1080")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        # 创建测试评论
        comment1 = Comment(comment_id=1,user_id=user1.id, content="This is a comment by Alice", like=10, dislike=1, date="2024-12-29")
        comment2 = Comment(comment_id=2,user_id=user2.id, content="This is a comment by Bob", like=5, dislike=0, date="2024-12-30")
        db.session.add(comment1)
        db.session.add(comment2)
        db.session.commit()

        # 创建测试 EasyPoint
        easypoint1 = EasyPoint(comment_id=1, user_id=user1.id, name="EasyPoint 1", type="Type 1", info="Info 1", location="Location 1", photo="https://27142293.s21i.faiusr.com/2/ABUIABACGAAg_I_bmQYokt25kQUwwAc4gAU.jpg", refresh_time="2024-12-29", like=100, dislike=10, lat=37.7749, lng=-122.4194)
        easypoint2 = EasyPoint(comment_id=2, user_id=user2.id, name="EasyPoint 2", type="Type 2", info="Info 2", location="Location 2", photo="https://27142293.s21i.faiusr.com/2/ABUIABACGAAg_I_bmQYokt25kQUwwAc4gAU.jpg", refresh_time="2024-12-30", like=50, dislike=5, lat=34.0522, lng=-118.2437)
        db.session.add(easypoint1)
        db.session.add(easypoint2)
        db.session.commit()

        # 创建测试 DynamicPost
        dynamicpost1 = DynamicPost(title="DynamicPost 1",type=2, date="2024-12-29", like=20, content="Content 1", lat=30.5155, lng= 114.4268, position="Position 1", user_id=user1.id, comment_id=comment1.comment_id)
        dynamicpost1.set_photos(["https://27142293.s21i.faiusr.com/2/ABUIABACGAAg_I_bmQYokt25kQUwwAc4gAU.jpg","https://27142293.s21i.faiusr.com/2/ABUIABACGAAg_I_bmQYokt25kQUwwAc4gAU.jpg"])
        dynamicpost2 = DynamicPost(title="DynamicPost 2", type=1,date="2024-12-30", like=15, content="Content 2", lat=31.5155, lng=114.4268, position="Position 2", user_id=user2.id, comment_id=comment2.comment_id)
        dynamicpost2.set_photos(["https://27142293.s21i.faiusr.com/2/ABUIABACGAAg_I_bmQYokt25kQUwwAc4gAU.jpg","https://27142293.s21i.faiusr.com/2/ABUIABACGAAg_I_bmQYokt25kQUwwAc4gAU.jpg"])
        db.session.add(dynamicpost1)
        db.session.add(dynamicpost2)
        db.session.commit()



        print("Test data created successfully!")

if __name__ == "__main__":
    create_test_data()