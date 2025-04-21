from app import create_app, db
from app.models.news import Category, Source, NewsArticle
from datetime import datetime, timedelta
import random

def init_db():
    app = create_app()
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if data already exists
        if Category.query.count() > 0:
            print("Database already initialized. Skipping...")
            return
        
        # Create categories
        categories = [
            {"name": "World", "slug": "world"},
            {"name": "Business", "slug": "business"},
            {"name": "Technology", "slug": "technology"},
            {"name": "Science", "slug": "science"},
            {"name": "Health", "slug": "health"},
            {"name": "Entertainment", "slug": "entertainment"},
            {"name": "Sports", "slug": "sports"},
            {"name": "Politics", "slug": "politics"}
        ]
        
        for category_data in categories:
            category = Category(name=category_data["name"], slug=category_data["slug"])
            db.session.add(category)
        
        db.session.commit()
        print(f"Added {len(categories)} categories")
        
        # Create sources
        sources = [
            {"name": "BBC News", "url": "https://www.bbc.com/news"},
            {"name": "CNN", "url": "https://www.cnn.com"},
            {"name": "Al Jazeera", "url": "https://www.aljazeera.com"},
            {"name": "Reuters", "url": "https://www.reuters.com"},
            {"name": "Dawn News", "url": "https://www.dawn.com"},
            {"name": "The News", "url": "https://www.thenews.com.pk"}
        ]
        
        for source_data in sources:
            source = Source(name=source_data["name"], url=source_data["url"])
            db.session.add(source)
        
        db.session.commit()
        print(f"Added {len(sources)} sources")
        
        # Create sample news articles
        sample_articles = [
            {
                "title": "Global Climate Summit Reaches Historic Agreement",
                "title_urdu": "عالمی موسمیاتی سمٹ تاریخی معاہدے پر پہنچ گئی",
                "slug": "global-climate-summit-reaches-historic-agreement",
                "content": "World leaders have reached a historic agreement at the Global Climate Summit to reduce carbon emissions by 50% by 2030. The agreement, which was signed by 195 countries, includes commitments to phase out coal power, increase renewable energy investments, and provide financial support to developing nations.\n\nThe summit, held in Geneva, Switzerland, lasted for two weeks and involved intense negotiations between major polluters and countries most vulnerable to climate change. UN Secretary-General António Guterres called the agreement \"a lifeline for future generations\" and urged immediate implementation.\n\nEnvironmental activists have cautiously welcomed the deal but emphasized that concrete actions must follow the promises. The agreement will be legally binding once ratified by individual countries, with a monitoring mechanism to ensure compliance.",
                "content_urdu": "عالمی رہنماؤں نے گلوبل کلائمیٹ سمٹ میں 2030 تک کاربن اخراج میں 50 فیصد کمی لانے کے لیے ایک تاریخی معاہدے پر پہنچ گئے ہیں۔ یہ معاہدہ، جس پر 195 ممالک نے دستخط کیے ہیں، کوئلے سے چلنے والی بجلی کو ختم کرنے، قابل تجدید توانائی میں سرمایہ کاری بڑھانے، اور ترقی پذیر ممالک کو مالی مدد فراہم کرنے کے عزم پر مشتمل ہے۔\n\nسوئٹزرلینڈ کے جنیوا میں منعقد ہونے والی یہ سمٹ دو ہفتوں تک جاری رہی اور اس میں بڑے آلودگی پھیلانے والے ممالک اور موسمیاتی تبدیلی سے سب سے زیادہ متاثر ہونے والے ممالک کے درمیان شدید مذاکرات ہوئے۔ اقوام متحدہ کے سیکرٹری جنرل انتونیو گوتیرس نے اس معاہدے کو \"آنے والی نسلوں کے لیے ایک زندگی کی لکیر\" قرار دیا اور فوری عملدرآمد پر زور دیا۔\n\nماحولیاتی کارکنوں نے اس معاہدے کا محتاط خیرمقدم کیا ہے لیکن اس بات پر زور دیا ہے کہ وعدوں کے بعد ٹھوس اقدامات ہونے چاہئیں۔ یہ معاہدہ انفرادی ممالک کی جانب سے توثیق کے بعد قانونی طور پر پابند ہوگا، جس میں تعمیل کو یقینی بنانے کے لیے ایک نگرانی کا طریقہ کار شامل ہے۔",
                "summary": "World leaders have reached a historic agreement at the Global Climate Summit to reduce carbon emissions by 50% by 2030, with commitments to phase out coal power and increase renewable energy investments.",
                "category_id": 1,  # World
                "source_id": 1,  # BBC News
                "status": "published"
            },
            {
                "title": "Tech Giant Unveils Revolutionary AI Assistant",
                "title_urdu": "ٹیک جائنٹ نے انقلابی اے آئی اسسٹنٹ متعارف کرایا",
                "slug": "tech-giant-unveils-revolutionary-ai-assistant",
                "content": "Leading technology company TechCorp has unveiled its latest artificial intelligence assistant, which it claims can understand and respond to human emotions. The AI, named 'Empathia', uses advanced facial recognition and voice analysis to detect emotional states and adjust its responses accordingly.\n\nDuring a demonstration at the company's headquarters, Empathia accurately identified subtle emotional cues from test subjects and provided appropriate responses. The system can recognize six basic emotions - happiness, sadness, anger, fear, surprise, and disgust - as well as more complex emotional states.\n\n\"This represents a significant breakthrough in human-computer interaction,\" said Dr. Sarah Chen, TechCorp's Chief AI Scientist. \"For the first time, we have an AI that doesn't just understand what you're saying, but how you're feeling when you say it.\"\n\nPrivacy advocates have raised concerns about the emotional data being collected and stored. TechCorp has stated that all emotional processing happens on-device and no emotional data is sent to their servers. The company plans to release Empathia to consumers next year after further refinement and testing.",
                "content_urdu": "معروف ٹیکنالوجی کمپنی ٹیک کارپ نے اپنا تازہ ترین مصنوعی ذہانت اسسٹنٹ متعارف کرایا ہے، جس کے بارے میں اس کا دعویٰ ہے کہ یہ انسانی جذبات کو سمجھ اور ان کا جواب دے سکتا ہے۔ 'ایمپیتھیا' نامی اے آئی، جذباتی حالات کا پتہ لگانے اور اس کے مطابق اپنے جوابات کو ایڈجسٹ کرنے کے لیے جدید چہرے کی شناخت اور آواز کے تجزیے کا استعمال کرتا ہے۔\n\nکمپنی کے ہیڈکوارٹر میں ایک مظاہرے کے دوران، ایمپیتھیا نے ٹیسٹ سبجیکٹس سے نازک جذباتی اشاروں کی درست شناخت کی اور مناسب جوابات فراہم کیے۔ یہ سسٹم چھ بنیادی جذبات - خوشی، غم، غصہ، خوف، حیرت، اور نفرت - کے ساتھ ساتھ زیادہ پیچیدہ جذباتی حالات کو بھی پہچان سکتا ہے۔\n\n\"یہ انسان اور کمپیوٹر کے درمیان تعامل میں ایک اہم پیش رفت کی نمائندگی کرتا ہے،\" ٹیک کارپ کی چیف اے آئی سائنسدان ڈاکٹر سارہ چین نے کہا۔ \"پہلی بار، ہمارے پاس ایک اے آئی ہے جو نہ صرف یہ سمجھتی ہے کہ آپ کیا کہہ رہے ہیں، بلکہ یہ بھی کہ آپ اسے کہتے وقت کیسا محسوس کر رہے ہیں۔\"\n\nرازداری کے وکلاء نے جمع کیے جانے والے اور ذخیرہ کیے جانے والے جذباتی ڈیٹا کے بارے میں تشویش کا اظہار کیا ہے۔ ٹیک کارپ نے کہا ہے کہ تمام جذباتی پروسیسنگ ڈیوائس پر ہوتی ہے اور کوئی جذباتی ڈیٹا ان کے سرورز پر نہیں بھیجا جاتا۔ کمپنی مزید بہتری اور ٹیسٹنگ کے بعد اگلے سال صارفین کے لیے ایمپیتھیا کو ریلیز کرنے کا منصوبہ رکھتی ہے۔",
                "summary": "TechCorp has unveiled 'Empathia', an AI assistant that can understand and respond to human emotions using facial recognition and voice analysis, representing a breakthrough in human-computer interaction.",
                "category_id": 3,  # Technology
                "source_id": 3,  # Al Jazeera
                "status": "published"
            },
            {
                "title": "Major Breakthrough in Cancer Treatment Announced",
                "title_urdu": "کینسر کے علاج میں بڑی پیش رفت کا اعلان",
                "slug": "major-breakthrough-in-cancer-treatment-announced",
                "content": "Medical researchers have announced a significant breakthrough in cancer treatment that could potentially transform how certain aggressive cancers are treated. The new therapy, which combines immunotherapy with targeted genetic modification, has shown remarkable results in early clinical trials.\n\nIn a study involving 120 patients with advanced pancreatic cancer, 78% showed significant tumor reduction, with 35% experiencing complete remission. These results are unprecedented for pancreatic cancer, which has traditionally had one of the lowest survival rates among cancer types.\n\n\"What makes this approach revolutionary is that it teaches the body's immune system to recognize cancer cells that previously were able to hide from immune detection,\" explained Dr. James Rodriguez, lead researcher at the International Cancer Research Institute. \"We're essentially removing the invisibility cloak from these cancer cells.\"\n\nThe treatment works by extracting immune cells from patients, genetically modifying them to better identify specific markers on cancer cells, and then reinfusing them into the patient. While side effects include fever and fatigue, they are generally less severe than traditional chemotherapy.\n\nResearchers caution that larger trials are needed before the treatment becomes widely available, but many oncologists are already describing the results as a potential paradigm shift in cancer care.",
                "content_urdu": "میڈیکل محققین نے کینسر کے علاج میں ایک اہم پیش رفت کا اعلان کیا ہے جو ممکنہ طور پر کچھ جارحانہ کینسر کے علاج کے طریقے کو تبدیل کر سکتی ہے۔ نئی تھراپی، جو امیونوتھراپی کو ہدفی جینیاتی ترمیم کے ساتھ جوڑتی ہے، ابتدائی کلینیکل ٹرائلز میں حیرت انگیز نتائج دکھائے ہیں۔\n\nایڈوانسڈ پینکریاٹک کینسر میں مبتلا 120 مریضوں پر مشتمل ایک مطالعے میں، 78% نے ٹیومر میں نمایاں کمی دکھائی، جبکہ 35% میں مکمل ریمیشن دیکھا گیا۔ یہ نتائج پینکریاٹک کینسر کے لیے بے مثال ہیں، جس میں روایتی طور پر کینسر کی اقسام میں سب سے کم بقا کی شرح رہی ہے۔\n\n\"جو چیز اس طریقہ کار کو انقلابی بناتی ہے وہ یہ ہے کہ یہ جسم کے مدافعتی نظام کو کینسر کے خلیات کو پہچاننا سکھاتی ہے جو پہلے مدافعتی نظام سے چھپ سکتے تھے،\" انٹرنیشنل کینسر ریسرچ انسٹیٹیوٹ کے لیڈ ریسرچر ڈاکٹر جیمز روڈریگز نے وضاحت کی۔ \"ہم اصل میں ان کینسر کے خلیات سے غیر مرئی چادر ہٹا رہے ہیں۔\"\n\nیہ علاج مریضوں سے مدافعتی خلیات نکال کر، انہیں جینیاتی طور پر ترمیم کر کے کینسر کے خلیات پر مخصوص مارکرز کو بہتر طور پر پہچاننے کے لیے، اور پھر انہیں مریض میں دوبارہ انفیوز کر کے کام کرتا ہے۔ اگرچہ ضمنی اثرات میں بخار اور تھکاوٹ شامل ہیں، لیکن یہ عام طور پر روایتی کیموتھراپی سے کم شدید ہیں۔\n\nمحققین نے خبردار کیا ہے کہ علاج کے وسیع پیمانے پر دستیاب ہونے سے پہلے بڑے پیمانے پر ٹرائلز کی ضرورت ہے، لیکن بہت سے آنکولوجسٹس پہلے ہی نتائج کو کینسر کی دیکھ بھال میں ایک ممکنہ پیراڈائم شفٹ کے طور پر بیان کر رہے ہیں۔",
                "summary": "Medical researchers have announced a breakthrough cancer treatment combining immunotherapy with targeted genetic modification, showing remarkable results in early clinical trials with 78% of advanced pancreatic cancer patients experiencing significant tumor reduction.",
                "category_id": 5,  # Health
                "source_id": 4,  # Reuters
                "status": "published"
            }
        ]
        
        # Add sample articles
        for article_data in sample_articles:
            # Generate random dates within the last week
            days_ago = random.randint(0, 7)
            published_date = datetime.now() - timedelta(days=days_ago)
            
            article = NewsArticle(
                title=article_data["title"],
                title_urdu=article_data["title_urdu"],
                slug=article_data["slug"],
                content=article_data["content"],
                content_urdu=article_data["content_urdu"],
                summary=article_data["summary"],
                published_date=published_date,
                created_date=published_date,
                updated_date=published_date,
                category_id=article_data["category_id"],
                source_id=article_data["source_id"],
                status=article_data["status"],
                meta_title=article_data["title"],
                meta_description=article_data["summary"],
                keywords="news, urdu, " + article_data["title"].lower().replace(" ", ", ")
            )
            db.session.add(article)
        
        db.session.commit()
        print(f"Added {len(sample_articles)} sample articles")
        
        print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()