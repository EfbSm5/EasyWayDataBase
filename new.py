from create_app import create_app, db
from models.user import User
from models.comment import Comment
from models.easypoint import EasyPoint
from models.dynamicpost import DynamicPost
from models.photo import Photo

app = create_app()

def create_test_data():
    with app.app_context():
        # 检查用户是否已经存在
        user3 = User.query.get(100)
        if not user3:
            user3 = User(id=100, name="Cindy", avatar="https://bkimg.cdn.bcebos.com/pic/5882b2b7d0a20cf43289a8ce7d094b36acaf9981?x-bce-process=image/format,f_auto/watermark,image_d2F0ZXIvYmFpa2UyNzI,g_7,xp_5,yp_5,P_20/resize,m_lfit,limit_1,h_1080")
            db.session.add(user3)
            db.session.commit()
        data = [
        (30.659224, 114.120428, "武汉径河地铁站B口"),
        (30.649214, 114.120413, "武汉三店地铁站B口"),
        (30.631491, 114.124109, "武汉码头潭公园地铁站C口"),
        (30.624459, 114.128544, "武汉东吴大道地铁站A口"),
        (30.61792, 114.138936, "武汉五环大道地铁站A口"),
        (30.617984, 114.156453, "武汉额头湾地铁站B口"),
        (30.614657, 114.164249, "武汉竹叶海地铁站B口"),
        (30.610358, 114.169209, "武汉舵落口地铁站C口"),
        (30.603937, 114.183252, "武汉古田一路地铁站B口"),
        (30.598171, 114.196436, "武汉古田二路地铁站C口"),
        (30.593831, 114.204789, "武汉古田三路地铁站C口"),
        (30.589559, 114.212175, "武汉古田四路地铁站C口"),
        (30.585661, 114.218822, "武汉汉西一路地铁站D口"),
        (30.657445, 114.333662, "武汉新荣地铁站D口"),
        (30.664658, 114.339891, "武汉堤角地铁站A口"),
        (30.684222, 114.342161, "武汉滠口新城地铁站C口"),
        (30.712492, 114.33033, "武汉汉口北地铁站A口")
        ]
        point_id = 10  # 从 10 开始
        refresh_time = "2025.3.6"
        for item in data:
            lat, lng, name = item  # 假设数据格式为 (lat, lng, name)
            easy_point = EasyPoint(
                comment_id=1,
                point_id=point_id,
                name=name,
                type="无障碍电梯",
                info="",
                location="",
                photo="https://27142293.s21i.faiusr.com/2/ABUIABACGAAg_I_bmQYokt25kQUwwAc4gAU.jpg",
                refresh_time=refresh_time,
                like=0,
                dislike=0,
                lat=lat,
                lng=lng,
                user_id=100,
                )
        
            db.session.add(easy_point)
            db.session.commit()
            point_id += 1
            print("Test data created successfully!")


        
if __name__ == "__main__":
    create_test_data()



