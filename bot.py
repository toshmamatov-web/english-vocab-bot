import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

# 🔑 Bot tokeningizni shu yerga yozing
TOKEN = "8823058668:AAEOqNgnjUPgy6hz_C9xlz2-rx6VIkwDUC0"

# 📚 «English in Pictures» kitobining barcha mavzulari va to'liq so'zlar bazasi (kitobdagi miqdor bo'yicha)
DICTIONARY = {
    "m1": {
        "title": "👨‍👩‍👧 1. Oila va Inson (Family and People)",
        "words": [
            ("Father", "Отец", "Ota"),
            ("Mother", "Мать", "Ona"),
            ("Grandfather", "Дедушка", "Buva"),
            ("Grandmother", "Бабушка", "Buvi"),
            ("Son", "Сын", "O'g'il"),
            ("Daughter", "Дочь", "Qiz"),
            ("Brother", "Брат", "Aka / Uka"),
            ("Sister", "Сестра", "Opa / Singil"),
            ("Uncle", "Дядя", "Amaki / Tog'a"),
            ("Aunt", "Тётя", "Xola / Amma"),
            ("Cousin", "Двоюродный брат/сестра", "Amakivachcha"),
            ("Baby", "Младенец", "Chaqaloq"),
            ("Man", "Мужчина", "Erkak"),
            ("Woman", "Женщина", "Ayol"),
            ("Boy", "Мальчик", "O'g'il bola"),
            ("Girl", "Девочка", "Qiz bola"),
        ],
    },
    "m2": {
        "title": "🏠 2. Uy va Xonalar (House and Rooms)",
        "words": [
            ("House", "Дом", "Uy"),
            ("Roof", "Крыша", "Tom"),
            ("Wall", "Стена", "Devor"),
            ("Door", "Дверь", "Eshik"),
            ("Window", "Окно", "Deraza"),
            ("Floor", "Пол", "Pol"),
            ("Ceiling", "Потолок", "Shift"),
            ("Living room", "Гостиная", "Mehmonxona"),
            ("Bedroom", "Спальня", "Yotoqxona"),
            ("Kitchen", "Кухня", "Oshxona"),
            ("Bathroom", "Ванная комната", "Yuvinish xonasi"),
            ("Corridor", "Коридор", "Koridor"),
            ("Stairs", "Лестница", "Zina"),
            ("Balcony", "Балкон", "Balkon"),
            ("Yard", "Двор", "Hovli"),
            ("Garage", "Гараж", "Garaj"),
        ],
    },
    "m3": {
        "title": "🏫 3. Maktab (School)",
        "words": [
            ("School", "Школа", "Maktab"),
            ("Classroom", "Классная комната", "Sinfxona"),
            ("Desk", "Парта", "Parta"),
            ("Blackboard", "Классная доска", "Sinf doskasi"),
            ("Book", "Книга", "Kitob"),
            ("Notebook", "Тетрадь", "Daftar"),
            ("Pen", "Ручка", "Ruchka"),
            ("Pencil", "Карандаш", "Qalam"),
            ("Ruler", "Линейка", "Chizg'ich"),
            ("Rubber", "Ластик", "O'chirg'ich"),
            ("Schoolbag", "Портфель", "Portfel"),
            ("Pencil case", "Пенал", "Penal"),
            ("Scissors", "Ножницы", "Qaychi"),
            ("Glue", "Клей", "Yelim"),
            ("Colors", "Краски", "Bo'yoqlar"),
            ("Paper", "Бумага", "Qog'oz"),
        ],
    },
    "m4": {
        "title": "🧸 4. O'yinchoqlar (Toys)",
        "words": [
            ("Doll", "Кукла", "Qo'g'irchoq"),
            ("Ball", "Мяч", "To'p"),
            ("Car", "Машинка", "Mashina"),
            ("Teddy bear", "Плюшевый мишка", "Ayiqcha"),
            ("Puzzle", "Пазл", "Pazl"),
            ("Balloon", "Воздушный шар", "Shar"),
            ("Robot", "Робот", "Robot"),
            ("Blocks", "Кубиki", "Kubiklar"),
            ("Kite", "Воздушный змей", "Varrak"),
            ("Train", "Игрушечный поезд", "O'yinchoq poyezd"),
            ("Drum", "Игрушечный барабан", "O'yinchoq baraban"),
            ("Plane", "Игрушечный самолет", "O'yinchoq samolyot"),
            ("Rattle", "Погремушка",choqlik := "Qarg'iroqcha"),
            ("Ship", "Игрушечный корабль", "O'yinchoq kema"),
            ("Top", "Юла", "Yula"),
            ("Skipping rope", "Скакалка", "Sakrash arqoni"),
        ],
    },
    "m5": {
        "title": "🎨 5. Ranglar (Colors)",
        "words": [
            ("White", "Белый", "Oq"),
            ("Black", "Чёрный", "Qora"),
            ("Red", "Красный", "Qizil"),
            ("Blue", "Синий", "Ko'k"),
            ("Light blue", "Голубой", "Moviy"),
            ("Yellow", "Жёлтый", "Sariq"),
            ("Green", "Зелёный", "Yashil"),
            ("Orange", "Оранжевый", "To'q sariq"),
            ("Pink", "Розовый", "Pushti"),
            ("Purple", "Фиолетовый", "Siyohrang"),
            ("Brown", "Коричневый", "Jigarrang"),
            ("Grey", "Серый", "Kulrang"),
            ("Golden", "Золотой", "Oltin rang"),
            ("Silver", "Серебряный", "Kumush rang"),
            ("Dark", "Тёмный", "To'q rang"),
            ("Light", "Светлый", "Ochiq rang"),
        ],
    },
    "m6": {
        "title": "🔢 6. Sonlar (Numbers)",
        "words": [
            ("Zero", "Ноль", "Nol"),
            ("One", "Один", "Bir"),
            ("Two", "Два", "Ikki"),
            ("Three", "Три", "Uch"),
            ("Four", "Четыре", "To'rt"),
            ("Five", "Пять", "Besh"),
            ("Six", "Шесть", "Olti"),
            ("Seven", "Семь", "Yetti"),
            ("Eight", "Восемь", "Sakkiz"),
            ("Nine", "Девять", "To'qqiz"),
            ("Ten", "Десять", "O'n"),
            ("Eleven", "Одиннадцать", "O'n bir"),
            ("Twelve", "Двенадцать", "O'n ikki"),
            ("Twenty", "Двадцать", "Yigirma"),
            ("Hundred", "Сто", "Yuz"),
            ("Thousand", "Тысяча", "Ming"),
        ],
    },
    "m7": {
        "title": "❄️ 7. Fasillar (Seasons)",
        "words": [
            ("Winter", "Зима", "Qish"),
            ("Spring", "Весна", "Bahor"),
            ("Summer", "Лето", "Yoz"),
            ("Autumn", "Осень", "Kuz"),
            ("Cold", "Холод", "Sovuq"),
            ("Warm", "Тепло", "Iliq"),
            ("Hot", "Жарко", "Issiq"),
            ("Cool", "Прохладно", "Salqin"),
            ("Snow", "Снег", "Qor"),
            ("Rain", "Дождь", "Yomg'ir"),
            ("Sun", "Солнце", "Quyosh"),
            ("Wind", "Ветер", "Shamol"),
            ("Cloud", "Облако", "Bulut"),
            ("Ice", "Лёд", "Muz"),
            ("Storm", "Буря", "Bo'ron"),
            ("Fog", "Туман", "Tuman"),
        ],
    },
    "m8": {
        "title": "🗓 8. Oylar (Months)",
        "words": [
            ("January", "Январь", "Yanvar"),
            ("February", "Февраль", "Fevral"),
            ("March", "Март", "Mart"),
            ("April", "Апрель", "Aprel"),
            ("May", "Май", "May"),
            ("June", "Июнь", "Iyun"),
            ("July", "Июль", "Iyul"),
            ("August", "Август", "Avgust"),
            ("September", "Сентябрь", "Sentabr"),
            ("October", "Октябрь", "Oktabr"),
            ("November", "Ноябрь", "Noyabr"),
            ("December", "Декабрь", "Dekabr"),
            ("Month", "Месяц", "Oy"),
            ("Year", "Год", "Yil"),
            ("Date", "Дата", "Sana"),
            ("Calendar", "Календарь", "Kalendar"),
        ],
    },
    "m9": {
        "title": "📅 9. Hafta kunlari (Days of the week)",
        "words": [
            ("Monday", "Понедельник", "Dushanba"),
            ("Tuesday", "Вторник", "Seshanba"),
            ("Wednesday", "Среда", "Chorshanba"),
            ("Thursday", "Четверг", "Payshanba"),
            ("Friday", "Пятница", "Juma"),
            ("Saturday", "Суббота", "Shanba"),
            ("Sunday", "Воскресенье", "Yakshanba"),
            ("Week", "Неделя", "Hafta"),
            ("Weekend", "Выходной", "Dam olish kuni"),
            ("Today", "Сегодня", "Bugun"),
            ("Tomorrow", "Завтра", "Ertaga"),
            ("Yesterday", "Вчера", "Kecha"),
            ("Day", "День", "Kun"),
            ("Night", "Ночь", "Tun"),
            ("Morning", "Утро", "Tong"),
            ("Evening", "Вечер", "Kechqurun"),
        ],
    },
    "m10": {
        "title": "🐄 10. Uy hayvonlari (Domestic animals)",
        "words": [
            ("Cow", "Корова", "Sigir"),
            ("Bull", "Бык", "Buzoq / Ho'kiz"),
            ("Calf", "Телёнок", "Buzoqlarcha"),
            ("Horse", "Лошадь", "Ot"),
            ("Foal", "Жеребёнок", "Toy"),
            ("Sheep", "Овца", "Qo'y"),
            ("Lamb", "Ягнёнок", "Qo'zi"),
            ("Goat", "Коза", "Echki"),
            ("Kid", "Козлёнок", "Uloq"),
            ("Pig", "Свинья", "Cho'chqa"),
            ("Piglet", "Поросёнок", "To'ng'izcha"),
            ("Cat", "Кошка", "Mushuk"),
            ("Kitten", "Котёнок", "Mushukcha"),
            ("Dog", "Собака", "It"),
            ("Puppy", "Щенок", " Kuchukcha"),
            ("Rabbit", "Кролик", "Quyon"),
            ("Donkey", "Осёл", "Eshak"),
            ("Camel", "Верблюд", "Tuya"),
        ],
    },
    "m11": {
        "title": "🦁 11. Yovoyi hayvonlar (Wild animals)",
        "words": [
            ("Lion", "Лев", "Sher"),
            ("Tiger", "Тигр", "Yo'lbars"),
            ("Bear", "Медведь", "Ayiq"),
            ("Wolf", "Волк", "Bo'ri"),
            ("Fox", "Лиса", "Tulki"),
            ("Elephant", "Слон", "Fil"),
            ("Monkey", "Обезьяна", "Maymun"),
            ("Zebra", "Зебра", "Zebra"),
            ("Giraffe", "Жираф", "Jirafa"),
            ("Kangaroo", "Кенгуру", "Kenguru"),
            ("Panda", "Панда", "Panda"),
            ("Leopard", "Леопард", "Leopard"),
            ("Cheetah", "Гепард", "Gepard"),
            ("Hippo", "Бегемот", "Begemot"),
            ("Rhino", "Носорог", "Karkidon"),
            ("Deer", "Олень", "Bug'u"),
        ],
    },
    "m12": {
        "title": "🦅 12. Qushlar (Birds)",
        "words": [
            ("Chicken", "Курица", "Tovuq"),
            ("Rooster", "Петух", "Xo'roz"),
            ("Chick", "Цыплёнок", "Jo'ja"),
            ("Duck", "Утка", "O'rdak"),
            ("Goose", "Гусь", "G'oz"),
            ("Turkey", "Индюк", "Kurka"),
            ("Eagle", "Орел", "Burgut"),
            ("Owl", "Сова", "Boyqush"),
            ("Pigeon", "Голубь", "Kabutar"),
            ("Parrot", "Попугай", "To'tiqush"),
            ("Swan", "Лебедь", "Oqqush"),
            ("Crow", "Ворона", "Qarg'a"),
            ("Sparrow", "Воробей", "Chumchuq"),
            ("Swallow", "Ласточка", "qaldirg'och"),
            ("Stork", "Аист", "Laylak"),
            ("Penguin", "Пингвин", "Pingvin"),
        ],
    },
    "m13": {
        "title": "🐝 13. Hasharotlar (Insects)",
        "words": [
            ("Bee", "Пчела", "Asalari"),
            ("Butterfly", "Бабочка", "Kapalak"),
            ("Ant", "Муравей", "Chumoli"),
            ("Fly", "Муха", "Pashsha"),
            ("Mosquito", "Комар", "Chivin"),
            ("Spider", "Паук", "O'rgimchak"),
            ("Wasp", "Оса", "Qovog'ari"),
            ("Ladybug", "Божья коровка", "Hojibibi"),
            ("Snail", "Улитка", "Shilliqurt"),
            ("Worm", "Червь", "Chuvalchang"),
            ("Caterpillar", "Гусеница", "Gusenitsa"),
            ("Dragonfly", "Стрекоза", "Nayzaqanot"),
            ("Grasshopper", "Кузнечик", "Chigirtka"),
            ("Beetle", "Жук", "Qo'ng'iz"),
            ("Scorpion", "Скорпион", " Chayon"),
            ("Centipede", "Сороконожка", " Qirqoyoq"),
        ],
    },
    "m14": {
        "title": "🐟 14. Baliqlar va Dengiz olami (Fish and Sea life)",
        "words": [
            ("Fish", "Рыба", "Baliq"),
            ("Shark", "Акула", "Akula"),
            ("Whale", "Кит", "Kit"),
            ("Dolphin", "Дельфин", "Delfin"),
            ("Crab", "Краб", "Qisqichbaqa"),
            ("Octopus", "Осьминог", "Sakkizoyoq"),
            ("Jellyfish", "Медуза", "Meduza"),
            ("Starfish", "Морская звезда", "Dengiz yulduzi"),
            ("Seahorse", "Морской конёк", "Dengiz oti"),
            ("Turtle", "Морская черепаха", "Dengiz toshbaqasi"),
            ("Seal", "Тюлень", "Tyulen"),
            ("Walrus", "Морж", "Morj"),
            ("Squid", "Кальмар", "Kalmar"),
            ("Shell", "Ракушка", "Chig'anoq"),
            ("Coral", "Коралл", "Marjon"),
            ("Stingray", "Скат", "Skat"),
        ],
    },
    "m15": {
        "title": "🍎 15. Mevalar (Fruits)",
        "words": [
            ("Apple", "Яблоко", "Olma"),
            ("Banana", "Банан", "Banan"),
            ("Orange", "Апельсин", "Apelsin"),
            ("Lemon", "Лимон", "Limon"),
            ("Grapes", "Виноград", "Uzum"),
            ("Watermelon", "Арбуз", "Tarvuz"),
            ("Melon", "Дыня", "Qovun"),
            ("Peach", "Персик", "Shaftoli"),
            ("Pear", "Груша", "Nok"),
            ("Strawberry", "Клубника", "Qulupnay"),
            ("Cherry", "Вишня", "Olcha"),
            ("Plum", "Слива", "Olxo'ri"),
            ("Apricot", "Абрикос", "O'rik"),
            ("Pineapple", "Ананас", "Ananas"),
            ("Pomegranate", "Гранат", "Anor"),
            ("Kiwi", "Киви", "Kivi"),
        ],
    },
    "m16": {
        "title": "🥕 16. Sabzavotlar (Vegetables)",
        "words": [
            ("Potato", "Картофель", "Kartoshka"),
            ("Tomato", "Помидор", "Pomidor"),
            ("Cucumber", "Огурец", "Bodring"),
            ("Carrot", "Морковь", "Sabzi"),
            ("Onion", "Лук", "Piyoz"),
            ("Garlic", "Чеснок", "Sarimsoq"),
            ("Cabbage", "Капуста", "Karam"),
            ("Pepper", "Перец", "Qalampir"),
            ("Radish", "Редис", "Rediska"),
            ("Eggplant", "Баклажан", "Baqlajon"),
            ("Pumpkin", "Тыква", "Qovoq"),
            ("Beet", "Свёкла", "Lavlagi"),
            ("Corn", "Кукуруza", "Makkajo'xori"),
            ("Peas", "Горох", "No'xat"),
            ("Parsley", "Петрушка", "Petrushka"),
            ("Dill", "Укроп", "Shivit"),
        ],
    },
    "m17": {
        "title": "🍲 17. Oziq-ovqat va Ichimliklar (Food and Drinks)",
        "words": [
            ("Bread", "Хлеб", "Non"),
            ("Water", "Вода", "Suv"),
            ("Milk", "Молоко", "Sut"),
            ("Tea", "Чай", "Choy"),
            ("Coffee", "Кофе", "Kofe"),
            ("Cheese", "Сыр", "Pishloq"),
            ("Butter", "Масло", "Sariyog'"),
            ("Meat", "Мясо", "Go'sht"),
            ("Soup", "Суп", "Sho'rva"),
            ("Salt", "Соль", "Tuz"),
            ("Sugar", "Сахар", "Shakar"),
            ("Egg", "Яйцо", "Tuxum"),
            ("Rice", "Рис", "Guruch"),
            ("Honey", "Мёд", "Asal"),
            ("Juice", "Сок", "Sharbat"),
            ("Cookie", "Печенье", "Pechenye"),
        ],
    },
    "m18": {
        "title": "👕 18. Kiyim-kechaklar (Clothes)",
        "words": [
            ("Shirt", "Рубашка", "Ko'ylak"),
            ("T-shirt", "Футболка", "Futbolka"),
            ("Pants", "Брюки", "Shim"),
            ("Dress", "Платье", "Ayollar ko'ylagi"),
            ("Coat", "Пальто", "Palto"),
            ("Jacket", "Куртка", "Kurtka"),
            ("Hat", "Шляпа", "Shlyapa"),
            ("Cap", "Кепка", "Kepka"),
            ("Scarf", "Шарф", "Sharf"),
            ("Skirt", "Юбка", "Yubka"),
            ("Sweater", "Свитер", "Sviter"),
            ("Suit", "Костюм", "Kostyum"),
            ("Gloves", "Перчатки", "Qo'lqop"),
            ("Belt", "Ремень", "Kamar"),
            ("Tie", "Галстук", "Gastuk"),
            ("Blouse", "Блузка", " Bluzka"),
        ],
    },
    "m19": {
        "title": "👞 19. Oyoq kiyimlar (Shoes)",
        "words": [
            ("Shoes", "Туфли", "Tufli"),
            ("Boots", "Ботинки", "Botinka"),
            ("Slippers", "Тапочки", "Shipak"),
            ("Sneakers", "Кроссовки", "Krossovka"),
            ("Socks", "Носки", "Paypoq"),
            ("Sandals", "Сандалии", "Sandali"),
            ("High heels", "Туфли на каблуках", " baland poshnali tufli"),
            ("Rubber boots", "Резиновые сапоги", "rezina botinka"),
            ("Flip-flops", "Шлёпанцы", "Shiplap"),
            ("Tights", "Колготки", "Kogotki"),
            ("Stockings", "Чулки", " Chulki"),
            ("Insoles", "Стельки", " Stelka"),
            ("Shoelaces", "Шнурки", " Shnurok"),
            ("Cleats", "Бутсы", " Butsa"),
            ("Moccasins", "Мокасины", " Mokasin"),
            ("Galoshes", "Галоши", " Kalish"),
        ],
    },
    "m20": {
        "title": "👁 20. Tana a'zolari (Body parts)",
        "words": [
            ("Head", "Голова", "Bosh"),
            ("Eye", "Глаз", "Ko'z"),
            ("Ear", "Ухо", "Quloq"),
            ("Nose", "Нос", "Burun"),
            ("Mouth", "Рот", "Og'iz"),
            ("Tooth", "Зуб", "Tish"),
            ("Hand", "Рука", "Qo'l"),
            ("Leg", "Нога", "Oyoq"),
            ("Hair", "Волосы", "Soch"),
            ("Finger", "Палец", "Barmoq"),
            ("Face", "Лицо", "Yuz"),
            ("Neck", "Шея", "Bo'yin"),
            ("Arm", "Рука (elka-bilak)", "Qo'l"),
            ("Knee", "Колено", "Tizza"),
            ("Foot", "Стопа", "Oyoq kafti"),
            ("Tongue", "Язык", "Til"),
        ],
    },
    "m21": {
        "title": "👨‍⚕️ 21. Kasblar (Professions)",
        "words": [
            ("Teacher", "Учитель", "O'qituvchi"),
            ("Doctor", "Врач", "Shifokor"),
            ("Driver", "Водитель", "Haydovchi"),
            ("Police officer", "Полицейский", "Militsiya"),
            ("Cook", "Повар", "Oshpaz"),
            ("Builder", "Строитель", "Quruvchi"),
            ("Farmer", "Фермер", "Fermer"),
            ("Pilot", "Пилот", "Pilot"),
            ("Firefighter", "Пожарный", "O't o'chiruvchi"),
            ("Artist", "Художник", "Rassom"),
            ("Dentist", "Стоматолог", "Stomatolog"),
            ("Nurse", "Медсестра", "Hamshira"),
            ("Singer", "Певец", "Xonanda"),
            ("Actor", "Актер", "Aktyor"),
            ("Writer", "Писатель", "Yozuvchi"),
            ("Scientist", "Ученый", "Olim"),
        ],
    },
    "m22": {
        "title": "🚗 22. Transport vositalari (Vehicles)",
        "words": [
            ("Car", "Машина", "Mashina"),
            ("Bus", "Автобус", "Avtobus"),
            ("Train", "Поезд", "Poyezd"),
            ("Plane", "Самолёт", "Samolyot"),
            ("Ship", "Корабль", "Kema"),
            ("Bicycle", "Велосипед", "Velosiped"),
            ("Motorcycle", "Мотоцикл", "Mototsikl"),
            ("Helicopter", "Вертолёт", "Vertolyot"),
            ("Taxi", "Такси", "Taksi"),
            ("Truck", "Грузовик", "Yuk mashinasi"),
            ("Tram", "Трамвай", "Tramvay"),
            ("Trolleybus", "Троллейбус", " Trolleybus"),
            ("Subway", "Метро", "Metro"),
            ("Scooter", "Самокат", "Samokat"),
            ("Rocket", "Ракета", "Raketa"),
            ("Boat", "Лодка", "Qayiq"),
        ],
    },
    "m23": {
        "title": "⛅ 23. Tabiat va Ob-havo (Nature and Weather)",
        "words": [
            ("Sun", "Солнце", "Quyosh"),
            ("Sky", "Небо", "Osmon"),
            ("Cloud", "Облако", "Bulut"),
            ("Rain", "Дождь", "Yomg'ir"),
            ("Snow", "Снег", "Qor"),
            ("Wind", "Ветер", "Shamol"),
            ("Mountain", "Гора", "Tog'"),
            ("River", "Река", "Daryo"),
            ("Sea", "Море", "Dengiz"),
            ("Forest", "Лес", "O'rmon"),
            ("Star", "Звезда", "Yulduz"),
            ("Moon", "Луна", "Oy"),
            ("Lake", "Озеро", "Ko'l"),
            ("Island", "Остров", "Orol"),
            ("Desert", "Пустыня", "Cho'l"),
            ("Volcano", "Вулкан", " Vulqon"),
        ],
    },
    "m24": {
        "title": "⚽ 24. Sport turlari (Sports)",
        "words": [
            ("Football", "Футбол", "Futbol"),
            ("Basketball", "Баскетбол", "Basketbol"),
            ("Volleyball", "Волейбол", "Voleybol"),
            ("Tennis", "Теннис", "Tennis"),
            ("Boxing", "Бокс", "Boks"),
            ("Swimming", "Плавание", "Suzish"),
            ("Running", "Бег", "Yugurish"),
            ("Chess", "Шахматы", "Shaxmat"),
            ("Wrestling", "Борьба", "Kurash"),
            ("Gymnastics", "Гимнастика", "Gimnastika"),
            ("Hockey", "Хоккей", "Xokkey"),
            ("Weightlifting", "Тяжелая атлетика", " Og'ir atletika"),
            ("Judo", "Дзюдо", "Dzyudo"),
            ("Karate", "Каратэ", "Karate"),
            ("Cycling", "Велоспорт", "Velosport"),
            ("Skiing", "Лыжный спорт", "Chang'i sporti"),
        ],
    },
    "m25": {
        "title": "🎸 25. Musiqa asboblari (Musical instruments)",
        "words": [
            ("Guitar", "Гитара", "Gitara"),
            ("Piano", "Пианино", "Pianino"),
            ("Drum", "Барабан", "Baraban"),
            ("Flute", "Флейта", "Fleyta"),
            ("Violin", "Скрипка", "Skripka"),
            ("Accordion", "Аккордеон", "Akkordeon"),
            ("Trumpet", "Труба", " Truba"),
            ("Saxophone", "Саксофон", "Saksofon"),
            ("Harpsichord", "Арфа", "Arfa"),
            ("Tambourine", "Бубен", "Doyra"),
            ("Xylophone", "Ксилофон", " Ksilofon"),
            ("Cymbal", "Тарелки", " Zang"),
            ("Synthesizer", "Синтезатор", "Sintezator"),
            ("Clarinet", "Кларнет", " Klarnet"),
            ("Trombone", "Тромбон", " Trombon"),
            ("Harmonica", "Губная гармошка", " garmoshka"),
        ],
    },
    "m26": {
        "title": "🍽 26. Idish-tovoqlar (Tableware)",
        "words": [
            ("Plate", "Тарелка", "Likopcha"),
            ("Cup", "Чашка", "Chashka"),
            ("Glass", "Стакан", "Stakan"),
            ("Spoon", "Ложка", "Qoshiq"),
            ("Fork", "Вилка", "Sanchqi"),
            ("Knife", "Нож", "Pichoq"),
            ("Pan", "Сковорода", "Tova"),
            ("Pot", "Кастрюля", "Qozon"),
            ("Teapot", "Чайник", "Choynak"),
            ("Kettle", "Электрический чайник", " Elektr choynak"),
            ("Bowl", "Пиала", "Piyola"),
            ("Tray", "Поднос", " Patnis"),
            ("Napkin", "Салфетка", " Salfetka"),
            ("Ladle", "Половник", " cho'mich"),
            ("Grater", "Тёрка", " qirg'ich"),
            ("Cutting board", "Разделочная доска", " kesish taxtasi"),
        ],
    },
    "m27": {
        "title": "🏙 27. Shahar (City)",
        "words": [
            ("Street", "Улица", "Ko'cha"),
            ("Building", "Здание", "Bino"),
            ("Hospital", "Больница", "Kasalxona"),
            ("School", "Школа", "Maktab"),
            ("Shop", "Магазин", "Do'kon"),
            ("Park", "Парк", "Bog'"),
            ("Bank", "Банк", "Bank"),
            ("Library", "Библиотека", "Kutubxona"),
            ("Museum", "Музей", "Muzey"),
            ("Theater", "Театр", "Teatr"),
            ("Cinema", "Кинотеатр", "Kinoteatr"),
            ("Hotel", "Гостиница", "Mehmonxona"),
            ("Pharmacy", "Аптека", "Dorixona"),
            ("Square", "Площадь", "Maydon"),
            ("Stadion", "Стадион", "Stadion"),
            ("Station", "Вокзал", "Vokzal"),
        ],
    },
    "m28": {
        "title": "🎉 28. Bayramlar (Holidays)",
        "words": [
            ("New Year", "Новый год", "Yangi yil"),
            ("Birthday", "День рождения", "Tug'ilgan kun"),
            ("Holiday", "Праздник", "Bayram"),
            ("Gift", "Подарок", "Sovg'a"),
            ("Cake", "Торт", "Tort"),
            ("Candle", "Свеча", "Sham"),
            ("Balloon", "Праздничный шар", "Bayram shari"),
            ("Fireworks", "Фейерверк", "Mushakbozlik"),
            ("Card", "Открытка", "Ochiqxona"),
            ("Invitation", "Приглашение", "Taklifnoma"),
            ("Clown", "Клоун", "Masxaraboz"),
            ("Mask", "Маска", "Niqob"),
            ("Garland", "Гирлянда", "Girlyanda"),
            ("Ribbon", "Лента", "Lenta"),
            ("Confetti", "Конфетти", "Konfetti"),
            ("Badge", "Значок", "nishon"),
        ],
    },
    "m29": {
        "title": "😊 29. Hissiyotlar (Emotions)",
        "words": [
            ("Happy", "Счастливый", "Baxtli"),
            ("Sad", "Грустный", "Xafa"),
            ("Angry", "Злой", "Jahl qilgan"),
            ("Tired", "Уставший", "Charchagan"),
            ("Surprised", "Удивленный", "Hayratda"),
            ("Scared", "Испуганный", "Qo'rqqan"),
            ("Joyful", "Радостный", "Quvnoq"),
            ("Serious", "Серьезный", "Jiddiy"),
            ("Calm", "Спокойный", "Tinch"),
            ("Bored", "Скучающий", "Zerikkan"),
            ("Sleepy", "Сонный", "Uyqusiragan"),
            ("Crying", "Плачущий", "Yig'layotgan"),
            ("Laughing", "Смеющийся", "Kulayotgan"),
            ("Confused", "Растерянный", "Dovdiragan"),
            ("Proud", "Гордый", "Mag'rur"),
            ("Excited", "Взволнованный", "Hayajonlangan"),
        ],
    },
    "m30": {
        "title": "🔵 30. Shakllar (Shapes)",
        "words": [
            ("Circle", "Круг", "Doira"),
            ("Square", "Квадрат", "Kvadrat"),
            ("Triangle", "Треугольник", "Uchburchak"),
            ("Rectangle", "Прямоугольник", "To'g'ri to'rtburchak"),
            ("Star", "Звезда", "Yulduz"),
            ("Oval", "Овал", "Oval"),
            ("Rhombus", "Ромб", "Romb"),
            ("Cylinder", "Цилиндр", "Tsilindr"),
            ("Cone", "Конус", "Konus"),
            ("Cube", "Куб", "Kub"),
            ("Sphere", "Сфера", "Sfera"),
            ("Line", "Линия", "Chiziq"),
            ("Point", "Точка", "Nuqta"),
            ("Angle", "Угол", "Burchak"),
            ("Cross", "Крест", "Xoch"),
            ("Spiral", "Спираль", "Spiral"),
        ],
    },
    "m31": {
        "title": "💻 31. Texnika (Technology)",
        "words": [
            ("Computer", "Компьютер", "Kompyuter"),
            ("Phone", "Телефон", "Telefon"),
            ("Television", "Телевизор", "Televizor"),
            ("Camera", "Камера", "Kamera"),
            ("Radio", "Радио", "Radio"),
            ("Laptop", "Ноутбук", "Noutbuk"),
            ("Watch", "Часы", "Soat"),
            ("Tablet", "Планшет", "Planshet"),
            ("Printer", "Принтер", "Printer"),
            ("Keyboard", "Клавиатура", "Klaviatura"),
            ("Mouse", "Мышь", "Sichqoncha"),
            ("Headphones", "Наушники", "Naushnik"),
            ("Refrigerators", "Холодильник", "Sovutgich"),
            ("Vacuum cleaner", "Пылесос", "Changyutgich"),
            ("Iron", "Утюг", "Dazmol"),
            ("Microwave", "Микроволновка", "Mikroto'lqinli pech"),
        ],
    },
    "m32": {
        "title": "🌳 32. O'rmon va o'simliklar (Forest and Plants)",
        "words": [
            ("Tree", "Дерево", "Daraxt"),
            ("Flower", "Цветок", "Gul"),
            ("Grass", "Трава", "O't"),
            ("Leaf", "Лист", "Barg"),
            ("Root", "Корень", "Ildiz"),
            ("Branch", "Ветка", "Shox"),
            ("Bush", "Куст", "Buta"),
            ("Mushroom", "Гриб", "Qo'ziqorin"),
            ("Log", "Пенёк", "To'nka"),
            ("Seed", "Семечко", "Urug'"),
            ("Stem", "Стебель", "Poya"),
            ("Pine", "Сосна", "Qarag'ay"),
            ("Oak", "Дуб", "Emak"),
            ("Rose", "Роза", "Atirgul"),
            ("Tulip", "Тюльпан", "Lola"),
            ("Cactus", "Кактус", "Kaktus"),
        ],
    },
    "m33": {
        "title": "🌙 33. Vaqt tushunchalari (Time concepts)",
        "words": [
            ("Morning", "Утро", "Tong"),
            ("Day", "День", "Kun"),
            ("Evening", "Вечер", "Kechqurun"),
            ("Night", "Ночь", "Tun"),
            ("Today", "Сегодня", "Bugun"),
            ("Tomorrow", "Завтра", "Ertaga"),
            ("Yesterday", "Вчера", "Kecha"),
            ("Hour", "Час", "Soat"),
            ("Minute", "Минута", "Daqiqa"),
            ("Second", "Секунда", "Soniya"),
            ("Clock", "Настенные часы", "Devoriy soat"),
            ("Time", "Время", "Vaqt"),
            ("Century", "Век", "Asr"),
            ("Past", "Прошлое", "O'tmish"),
            ("Future", "Будущее", "Kelajak"),
            ("Moment", "Момент", "Lahza"),
        ],
    }
}

class QuizState(StatesGroup):
    in_quiz = State()

router = Router()

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📚 Lug'at"), KeyboardButton(text="🎮 Test (Viktorina)")],
        [KeyboardButton(text="ℹ️ Bot haqida")]
    ],
    resize_keyboard=True
)

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "✨ <b>Assalomu alaykum!</b> <i>«English in Pictures»</i> kitobidagi to'liq va mukammal lug'at botiga xush kelibsiz! 🚀\n\n"
        "Quyidagi menyu tugmalari yordamida kerakli bo'limni tanlang:",
        reply_markup=main_menu_keyboard,
        parse_mode="HTML"
    )

@router.message(F.text == "ℹ️ Bot haqida")
async def about_bot(message: Message):
    await message.answer(
        "💡 <b>Bot haqida ma'lumot:</b>\n\n"
        "Ushbu bot Nargiza Nurmuhamedovaning <b>«English in Pictures»</b> kitobidagi barcha 33 ta mavzu va ularning to'liq so'zlarini o'z ichiga oladi.",
        parse_mode="HTML"
    )

@router.message(F.text == "📚 Lug'at")
async def show_dictionary_categories(message: Message):
    keyboard_builder = []
    for key, data in DICTIONARY.items():
        keyboard_builder.append([InlineKeyboardButton(text=data["title"], callback_data=f"cat_{key}")])
    
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard_builder)
    await message.answer("📂 O'rganish uchun kitobdagi kerakli mavzuni tanlang:", reply_markup=markup)

@router.callback_query(F.data.startswith("cat_"))
async def show_category_words(callback: CallbackQuery):
    cat_key = callback.data.split("_")[1]
    if cat_key not in DICTIONARY:
        await callback.answer("⚠️ Mavzu topilmadi!", show_alert=True)
        return
    
    cat_data = DICTIONARY[cat_key]
    text = f"<b>{cat_data['title']}</b>\n\n"
    for idx, (eng, rus, uz) in enumerate(cat_data["words"], 1):
        text += f"<code>{idx}.</code> <b>{eng}</b> — {rus} — <i>{uz}</i>\n"
    
    back_button = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⬅️ Ortga qaytish", callback_data="back_to_cats")]]
    )
    
    # Xabar uzunligi oshib ketmasligi uchun tekshiruv (Telegram limiti 4096 belgi)
    if len(text) > 4000:
        text = text[:4000] + "\n\n... (davomi bor)"
        
    await callback.message.edit_text(text, reply_markup=back_button, parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "back_to_cats")
async def back_to_categories(callback: CallbackQuery):
    keyboard_builder = []
    for key, data in DICTIONARY.items():
        keyboard_builder.append([InlineKeyboardButton(text=data["title"], callback_data=f"cat_{key}")])
    
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard_builder)
    await callback.message.edit_text("📂 O'rganish uchun kitobdagi kerakli mavzuni tanlang:", reply_markup=markup)
    await callback.answer()

@router.message(F.text == "🎮 Test (Viktorina)")
async def choose_quiz_category(message: Message):
    keyboard_builder = []
    for key, data in DICTIONARY.items():
        keyboard_builder.append([InlineKeyboardButton(text=data["title"], callback_data=f"quizcat_{key}")])
    
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard_builder)
    await message.answer("🎯 Sinovdan o'tmoqchi bo'lgan mavzuni tanlang:", reply_markup=markup)

@router.callback_query(F.data.startswith("quizcat_"))
async def start_category_quiz(callback: CallbackQuery, state: FSMContext):
    cat_key = callback.data.split("_")[1]
    if cat_key not in DICTIONARY:
        await callback.answer("⚠️ Mavzu topilmadi!", show_alert=True)
        return
    
    words = list(DICTIONARY[cat_key]["words"])
    random.shuffle(words)
    
    await state.set_state(QuizState.in_quiz)
    await state.update_data(
        words=words,
        total=len(words),
        current_index=0,
        correct_count=0,
        cat_key=cat_key
    )
    
    try:
        await callback.message.delete()
    except:
        pass
    await send_next_question(callback.message, state)
    await callback.answer()

async def send_next_question(message: Message, state: FSMContext):
    data = await state.get_data()
    words = data["words"]
    index = data["current_index"]
    
    if index >= len(words):
        total = data["total"]
        correct = data["correct_count"]
        wrong = total - correct
        
        percentage = int((correct / total) * 100) if total > 0 else 0
        medal = "🥇" if percentage >= 80 else ("🥈" if percentage >= 50 else "🥉")
        
        finish_text = (
            f"🎉 <b>Tabriklayman! Test yakunlandi!</b> {medal}\n\n"
            f"📊 <b>Sizning statistikangiz:</b>\n"
            f"✅ To'g'ri javoblar: <b>{correct} ta</b>\n"
            f"❌ Xato javoblar: <b>{wrong} ta</b>\n"
            f"🎯 Natija: <b>{percentage}%</b>\n"
            f"📌 Jami savollar: <b>{total} ta</b>"
        )
        
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔁 Yana test qilish", callback_data=f"quizcat_{data['cat_key']}")],
                [InlineKeyboardButton(text="🏠 Menyuga o'tish", callback_data="back_to_main_menu")]
            ]
        )
        await message.answer(finish_text, reply_markup=markup, parse_mode="HTML")
        await state.clear()
        return

    eng, rus, uz = words[index]
    
    all_uz_words = [w[2] for cat in DICTIONARY.values() for w in cat["words"]]
    other_words = [w for w in all_uz_words if w != uz]
    wrong_options = random.sample(other_words, min(3, len(other_words)))
    options = wrong_options + [uz]
    random.shuffle(options)
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=opt, callback_data=f"ans_{opt}")] for opt in options
        ]
    )
    
    await message.answer(
        f"📝 <b>Savol {index + 1} / {len(words)}</b>\n\n"
        f"Inglizcha <b>'{eng}'</b> so'zining o'zbekcha tarjimasi qaysi?",
        reply_dagari=keyboard,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@router.callback_query(QuizState.in_quiz, F.data.startswith("ans_"))
async def handle_quiz_answer(callback: CallbackQuery, state: FSMContext):
    selected_answer = callback.data.split("_", 1)[1]
    
    data = await state.get_data()
    words = data["words"]
    index = data["current_index"]
    
    _, _, correct_uz = words[index]
    
    correct_count = data["correct_count"]
    if selected_answer == correct_uz:
        correct_count += 1
        await state.update_data(correct_count=correct_count)
        feedback = f"✅ <b>Ajoyib, To'g'ri!</b> 🎉 ({correct_uz})"
    else:
        feedback = f"❌ <b>Xato!</b> To'g'ri javob: <b>{correct_uz}</b>"
    
    try:
        await callback.message.edit_text(f"{callback.message.text}\n\n{feedback}", parse_mode="HTML")
    except:
        pass
    
    await state.update_data(current_index=index + 1)
    await send_next_question(callback.message, state)
    await callback.answer()

@router.callback_query(F.data == "back_to_main_menu")
async def back_to_main_menu_cb(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        "🏠 Asosiy menyuga qaytdingiz. Kerakli bo'limni tanlang:",
        reply_markup=main_menu_keyboard
    )
    await callback.answer()

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    print("Bot muvaffaqiyatli ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())