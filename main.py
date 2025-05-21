import os
import asyncio
import random
import telegram.error
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")

print("TOKEN:", TOKEN)
if TOKEN is None:
    raise Exception("❌ Railway не бачить змінну TOKEN")
    
SMART_LINK = "https://securesmdtlink.com/s?a=267695&sm=49040&co=328937&mt=29"
VIDEO_NOTE_IDS = [
    "DQACAgIAAxkBAAIC_mgk9c-RV4i4OGfdi-0CnKlnF0-BAAILbgACMOvwS7l2ZKjRmAstNgQ",
    "DQACAgIAAxkBAAIDAAFoJPYOtw5s3_xYE_geYnx6cKSP0AAC11QAAoE1UEruSdsu0gABkGg2BA",
    "DQACAgIAAxkBAAIDAmgk9jsxyW3h4q-VvJ_sDHN2OQABqgACQGkAAr2QKEliJ2CZBng4DTYE"
]

user_lang = {}

LANGUAGES = {
    "🇷🇺 Русский": "ru", "🇬🇧 English": "en", "🇪🇸 Español": "es",
    "🇩🇪 Deutsch": "de", "🇫🇷 Français": "fr", "🇵🇱 Język polski": "pl",
    "🇮🇹 Italiano": "it", "🇮🇩 Bahasa Indonesia": "id", "🇧🇬 Български": "bg",
    "🇨🇿 Čeština": "cs", "🇩🇰 Dansk": "da", "🇬🇷 Ελληνικά": "el",
    "🇫🇮 Suomi": "fi", "🇭🇺 Magyar": "hu", "🇯🇵 日本語": "ja",
    "🇰🇷 한국어": "ko", "🇱🇹 Lietuvių": "lt", "🇱🇻 Latviešu": "lv",
    "🇳🇴 Norsk Bokmål": "no", "🇳🇱 Nederlands": "nl", "🇵🇹 Português": "pt",
    "🇷🇴 Română": "ro", "🇸🇰 Slovenčina": "sk", "🇸🇮 Slovenščina": "sl",
    "🇸🇪 Svenska": "sv", "🇹🇷 Türkçe": "tr", "🇺🇦 Українська": "uk",
    "🇨🇳 中文": "zh-cn", "🇸🇦 العربية": "ar", "🇮🇱 עברית": "he",
    "🇮🇳 हिन्दी": "hi", "🇹🇭 ไทย": "th", "🇻🇳 Tiếng Việt": "vi"
}

FAKE_USERNAMES = [
    "SweetMia22", "AnnaXx_91", "RealJane99", "Sasha_777", "LoveLera_21",
    "EvaMoon92", "Tanya123x", "HotNika44", "DashaLuv88", "CuteKira_07"
]

TRANSLATIONS = {
    "uk": {
        "Йде пошук співрозмовника": "Йде пошук співрозмовника",
        "Зараз спілкуються": "Зараз спілкуються",
        "Співрозмовник знайдений!": "Співрозмовник знайдений!",
        "Відео не знайдено.": "Відео не знайдено.",
        "Співрозмовник покинув чат": "Співрозмовник покинув чат",
        "Пошук нового співрозмовника": "Пошук нового співрозмовника",
        "Пошук нового співрозмовника ⬇️": "Пошук нового співрозмовника ⬇️",
        "Авторизуватись": "Авторизуватись",
        "Зареєструватись": "Зареєструватись",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "Щоб продовжити, авторизуйтесь або зареєструйтесь:",
        "Мову встановлено": "Мову встановлено",
        "👋": "👋",
        "Давай розслабимось": "Давай розслабимось",
        "Продовжимо?": "Продовжимо?",
        "Подобається?": "Подобається?"
    },
    "en": {
        "Йде пошук співрозмовника": "Searching for a partner",
        "Зараз спілкуються": "Currently chatting",
        "Співрозмовник знайдений!": "Partner found!",
        "Відео не знайдено.": "Video not found.",
        "Співрозмовник покинув чат": "Partner left the chat",
        "Пошук нового співрозмовника": "Find new partner",
        "Пошук нового співрозмовника ⬇️": "Find a new partner ⬇️",
        "Авторизуватись": "Login",
        "Зареєструватись": "Sign up",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "To continue, please log in or sign up:",
        "Мову встановлено": "Language set",
        "👋": "👋",
        "Давай розслабимось": "Let's relax",
        "Продовжимо?": "Shall we continue?",
        "Подобається?": "Do you like it?"
    },
    "fr": {
        "Йде пошук співрозмовника": "Recherche d’un partenaire",
        "Зараз спілкуються": "Actuellement en discussion",
        "Співрозмовник знайдений!": "Partenaire trouvé!",
        "Відео не знайдено.": "Vidéo non trouvée.",
        "Співрозмовник покинув чат": "Le partenaire a quitté le chat",
        "Пошук нового співрозмовника": "Trouver un nouveau partenaire",
        "Пошук нового співрозмовника ⬇️": "Trouver un nouveau partenaire ⬇️",
        "Авторизуватись": "Connexion",
        "Зареєструватись": "S'inscrire",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "Veuillez vous connecter ou vous inscrire pour continuer :",
        "Мову встановлено": "Langue définie",
        "👋": "👋",
        "Давай розслабимось": "Détendons-nous",
        "Продовжимо?": "On continue ?",
        "Подобається?": "Tu aimes ?"
    },
    "es": {
        "Йде пошук співрозмовника": "Buscando un compañero",
        "Співрозмовник знайдений!": "¡Compañero encontrado!",
        "Відео не знайдено.": "Video no encontrado.",
        "Співрозмовник покинув чат": "El compañero ha salido del chat",
        "Пошук нового співрозмовника": "Buscar nuevo compañero",
        "Пошук нового співрозмовника ⬇️": "Buscar nuevo compañero ⬇️",
        "Авторизуватись": "Iniciar sesión",
        "Зареєструватись": "Registrarse",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "Para continuar, inicie sesión o regístrese:",
        "Мову встановлено": "Idioma establecido",
        "👋": "👋",
        "Давай розслабимось": "Relajémonos",
        "Продовжимо?": "¿Continuamos?",
        "Подобається?": "¿Te gusta?"
    },
    "ru": {
        "Йде пошук співрозмовника": "Поиск собеседника",
        "Зараз спілкуються": "Сейчас общаются",
        "Співрозмовник знайдений!": "Собеседник найден!",
        "Відео не знайдено.": "Видео не найдено.",
        "Співрозмовник покинув чат": "Собеседник покинул чат",
        "Пошук нового співрозмовника": "Найти нового собеседника",
        "Пошук нового співрозмовника ⬇️": "Найти нового собеседника ⬇️",
        "Авторизуватись": "Войти",
        "Зареєструватись": "Зарегистрироваться",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "Чтобы продолжить, войдите или зарегистрируйтесь:",
        "Мову встановлено": "Язык установлен",
        "👋": "👋",
        "Давай розслабимось": "Давай расслабимся",
        "Продовжимо?": "Продолжим?",
        "Подобається?": "Нравится?"
    },
    "de": {
        "Йде пошук співрозмовника": "Suche nach einem Partner",
        "Співрозмовник знайдений!": "Partner gefunden!",
        "Відео не знайдено.": "Video nicht gefunden.",
        "Співрозмовник покинув чат": "Partner hat den Chat verlassen",
        "Пошук нового співрозмовника": "Neuen Partner finden",
        "Пошук нового співрозмовника ⬇️": "Neuen Partner finden ⬇️",
        "Авторизуватись": "Anmelden",
        "Зареєструватись": "Registrieren",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "Bitte anmelden oder registrieren, um fortzufahren:",
        "Мову встановлено": "Sprache festgelegt",
        "👋": "👋",
        "Давай розслабимось": "Lass uns entspannen",
        "Продовжимо?": "Machen wir weiter?",
        "Подобається?": "Gefällt dir das?"
    },
    "pl": {
        "Йде пошук співрозмовника": "Trwa wyszukiwanie partnera",
        "Співрозмовник знайдений!": "Znaleziono partnera!",
        "Відео не знайдено.": "Nie znaleziono wideo.",
        "Співрозмовник покинув чат": "Partner opuścił czat",
        "Пошук нового співрозмовника": "Znajdź nowego partnera",
        "Пошук нового співрозмовника ⬇️": "Znajdź nowego partnera ⬇️",
        "Авторизуватись": "Zaloguj się",
        "Зареєструватись": "Zarejestruj się",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "Aby kontynuować, zaloguj się lub zarejestruj:",
        "Мову встановлено": "Język ustawiony",
        "👋": "👋",
        "Давай розслабимось": "Zrelaksujmy się",
        "Продовжимо?": "Kontynuujemy?",
        "Подобається?": "Podoba Ci się?"
    },
    "it": {
        "Йде пошук співрозмовника": "Ricerca di un partner in corso",
        "Співрозмовник знайдений!": "Partner trovato!",
        "Відео не знайдено.": "Video non trovato.",
        "Співрозмовник покинув чат": "Il partner ha lasciato la chat",
        "Пошук нового співрозмовника": "Trova un nuovo partner",
        "Пошук нового співрозмовника ⬇️": "Trova un nuovo partner ⬇️",
        "Авторизуватись": "Accedi",
        "Зареєструватись": "Registrati",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "Per continuare, accedi o registrati:",
        "Мову встановлено": "Lingua impostata",
        "👋": "👋",
        "Давай розслабимось": "Rilassiamoci",
        "Продовжимо?": "Continuiamo?",
        "Подобається?": "Ti piace?"
    },
    "id": {
        "Йде пошук співрозмовника": "Sedang mencari pasangan",
        "Співрозмовник знайдений!": "Pasangan ditemukan!",
        "Відео не знайдено.": "Video tidak ditemukan.",
        "Співрозмовник покинув чат": "Pasangan meninggalkan obrolan",
        "Пошук нового співрозмовника": "Cari pasangan baru",
        "Пошук нового співрозмовника ⬇️": "Cari pasangan baru ⬇️",
        "Авторизуватись": "Masuk",
        "Зареєструватись": "Daftar",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "Untuk melanjutkan, masuk atau daftar:",
        "Мову встановлено": "Bahasa disetel",
        "👋": "👋",
        "Давай розслабимось": "Mari bersantai",
        "Продовжимо?": "Lanjutkan?",
        "Подобається?": "Suka?"
    },
    "bg": {
        "Йде пошук співрозмовника": "Търси се събеседник",
        "Співрозмовник знайдений!": "Събеседникът е намерен!",
        "Відео не знайдено.": "Видеото не е намерено.",
        "Співрозмовник покинув чат": "Събеседникът напусна чата",
        "Пошук нового співрозмовника": "Намерете нов събеседник",
        "Пошук нового співрозмовника ⬇️": "Намерете нов събеседник ⬇️",
        "Авторизуватись": "Вход",
        "Зареєструватись": "Регистрация",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "За да продължите, влезте или се регистрирайте:",
        "Мову встановлено": "Езикът е зададен",
        "👋": "👋",
        "Давай розслабимось": "Нека се отпуснем",
        "Продовжимо?": "Да продължим ли?",
        "Подобається?": "Харесва ли ти?"
    },
    "cs": {
        "Йде пошук співрозмовника": "Hledání partnera",
        "Співрозмовник знайдений!": "Partner nalezen!",
        "Відео не знайдено.": "Video nenalezeno.",
        "Співрозмовник покинув чат": "Partner opustil chat",
        "Пошук нового співрозмовника": "Najít nového partnera",
        "Пошук нового співрозмовника ⬇️": "Najít nového partnera ⬇️",
        "Авторизуватись": "Přihlásit se",
        "Зареєструватись": "Zaregistrovat se",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "Pro pokračování se přihlaste nebo zaregistrujte:",
        "Мову встановлено": "Jazyk nastaven",
        "👋": "👋",
        "Давай розслабимось": "Odpočiňme si",
        "Продовжимо?": "Pokračujeme?",
        "Подобається?": "Líbí se ti to?"
    },
    "da": {
        "Йде пошук співрозмовника": "Søger efter en partner",
        "Співрозмовник знайдений!": "Partner fundet!",
        "Відео не знайдено.": "Video ikke fundet.",
        "Співрозмовник покинув чат": "Partneren har forladt chatten",
        "Пошук нового співрозмовника": "Find ny partner",
        "Пошук нового співрозмовника ⬇️": "Find ny partner ⬇️",
        "Авторизуватись": "Log ind",
        "Зареєструватись": "Tilmeld dig",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "Log ind eller tilmeld dig for at fortsætte:",
        "Мову встановлено": "Sprog indstillet",
        "👋": "👋",
        "Давай розслабимось": "Lad os slappe af",
        "Продовжимо?": "Skal vi fortsætte?",
        "Подобається?": "Kan du lide det?"
    },
    "el": {
        "Йде пошук співрозмовника": "Αναζήτηση συνομιλητή",
        "Співрозмовник знайдений!": "Ο συνομιλητής βρέθηκε!",
        "Відео не знайдено.": "Το βίντεο δεν βρέθηκε.",
        "Співрозмовник покинув чат": "Ο συνομιλητής αποχώρησε από τη συνομιλία",
        "Пошук нового співрозмовника": "Βρείτε νέο συνομιλητή",
        "Пошук нового співрозмовника ⬇️": "Βρείτε νέο συνομιλητή ⬇️",
        "Авторизуватись": "Σύνδεση",
        "Зареєструватись": "Εγγραφή",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "Για να συνεχίσετε, συνδεθείτε ή εγγραφείτε:",
        "Мову встановлено": "Η γλώσσα ορίστηκε",
        "👋": "👋",
        "Давай розслабимось": "Ας χαλαρώσουμε",
        "Продовжимо?": "Συνεχίζουμε;",
        "Подобається?": "Σου αρέσει;"
    },
    "fi": {
        "Йде пошук співрозмовника": "Etsitään keskustelukumppania",
        "Співрозмовник знайдений!": "Keskustelukumppani löytyi!",
        "Відео не знайдено.": "Videota ei löytynyt.",
        "Співрозмовник покинув чат": "Keskustelukumppani poistui keskustelusta",
        "Пошук нового співрозмовника": "Etsi uusi keskustelukumppani",
        "Пошук нового співрозмовника ⬇️": "Etsi uusi keskustelukumppani ⬇️",
        "Авторизуватись": "Kirjaudu sisään",
        "Зареєструватись": "Rekisteröidy",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "Jatka kirjautumalla sisään tai rekisteröitymällä:",
        "Мову встановлено": "Kieli asetettu",
        "👋": "👋",
        "Давай розслабимось": "Rentoudutaan",
        "Продовжимо?": "Jatketaanko?",
        "Подобається?": "Pidätkö siitä?"
    },
    "hu": {
        "Йде пошук співрозмовника": "Beszélgetőtárs keresése folyamatban",
        "Співрозмовник знайдений!": "Beszélgetőtárs megtalálva!",
        "Відео не знайдено.": "Videó nem található.",
        "Співрозмовник покинув чат": "A beszélgetőtárs elhagyta a csevegést",
        "Пошук нового співрозмовника": "Új beszélgetőtárs keresése",
        "Пошук нового співрозмовника ⬇️": "Új beszélgetőtárs keresése ⬇️",
        "Авторизуватись": "Bejelentkezés",
        "Зареєструватись": "Regisztráció",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "A folytatáshoz jelentkezzen be vagy regisztráljon:",
        "Мову встановлено": "A nyelv beállítva",
        "👋": "👋",
        "Давай розслабимось": "Lazítsunk",
        "Продовжимо?": "Folytatjuk?",
        "Подобається?": "Tetszik?"
    },
    "ja": {
        "Йде пошук співрозмовника": "相手を探しています",
        "Співрозмовник знайдений!": "相手が見つかりました！",
        "Відео не знайдено.": "ビデオが見つかりません。",
        "Співрозмовник покинув чат": "相手がチャットを離れました",
        "Пошук нового співрозмовника": "新しい相手を探す",
        "Пошук нового співрозмовника ⬇️": "新しい相手を探す ⬇️",
        "Авторизуватись": "ログイン",
        "Зареєструватись": "登録",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "続けるには、ログインまたは登録してください：",
        "Мову встановлено": "言語が設定されました",
        "👋": "👋",
        "Давай розслабимось": "リラックスしましょう",
        "Продовжимо?": "続けましょうか？",
        "Подобається?": "気に入りましたか？"
    },
    "ko": {
        "Йде пошук співрозмовника": "상대방을 찾는 중",
        "Співрозмовник знайдений!": "상대방을 찾았습니다!",
        "Відео не знайдено.": "비디오를 찾을 수 없습니다.",
        "Співрозмовник покинув чат": "상대방이 채팅을 나갔습니다",
        "Пошук нового співрозмовника": "새로운 상대방 찾기",
        "Пошук нового співрозмовника ⬇️": "새로운 상대방 찾기 ⬇️",
        "Авторизуватись": "로그인",
        "Зареєструватись": "가입하기",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "계속하려면 로그인하거나 가입하세요:",
        "Мову встановлено": "언어가 설정되었습니다",
        "👋": "👋",
        "Давай розслабимось": "편안히 쉬어요",
        "Продовжимо?": "계속할까요?",
        "Подобається?": "마음에 드시나요?"
    },
    "lt": {
        "Йде пошук співрозмовника": "Ieškomas pašnekovas",
        "Співрозмовник знайдений!": "Pašnekovas rastas!",
        "Відео не знайдено.": "Vaizdo įrašas nerastas.",
        "Співрозмовник покинув чат": "Pašnekovas paliko pokalbį",
        "Пошук нового співрозмовника": "Rasti naują pašnekovą",
        "Пошук нового співрозмовника ⬇️": "Rasti naują pašnekovą ⬇️",
        "Авторизуватись": "Prisijungti",
        "Зареєструватись": "Registruotis",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "Norėdami tęsti, prisijunkite arba užsiregistruokite:",
        "Мову встановлено": "Kalba nustatyta",
        "👋": "👋",
        "Давай розслабимось": "Atsipalaiduokime",
        "Продовжимо?": "Tęsiame?",
        "Подобається?": "Patinka?"
    },
    "lv": {
        "Йде пошук співрозмовника": "Tiek meklēts sarunu biedrs",
        "Співрозмовник знайдений!": "Sarunu biedrs atrasts!",
        "Відео не знайдено.": "Video nav atrasts.",
        "Співрозмовник покинув чат": "Sarunu biedrs pameta tērzēšanu",
        "Пошук нового співрозмовника": "Meklēt jaunu sarunu biedru",
        "Пошук нового співрозмовника ⬇️": "Meklēt jaunu sarunu biedru ⬇️",
        "Авторизуватись": "Pieslēgties",
        "Зареєструватись": "Reģistrēties",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "Lai turpinātu, pieslēdzieties vai reģistrējieties:",
        "Мову встановлено": "Valoda iestatīta",
        "👋": "👋",
        "Давай розслабимось": "Atslābstam",
        "Продовжимо?": "Turpinām?",
        "Подобається?": "Patīk?"
    },
    "no": {
        "Йде пошук співрозмовника": "Søker etter samtalepartner",
        "Співрозмовник знайдений!": "Samtalepartner funnet!",
        "Відео не знайдено.": "Video ikke funnet.",
        "Співрозмовник покинув чат": "Samtalepartner har forlatt chatten",
        "Пошук нового співрозмовника": "Finn ny samtalepartner",
        "Пошук нового співрозмовника ⬇️": "Finn ny samtalepartner ⬇️",
        "Авторизуватись": "Logg inn",
        "Зареєструватись": "Registrer deg",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "Logg inn eller registrer deg for å fortsette:",
        "Мову встановлено": "Språk satt",
        "👋": "👋",
        "Давай розслабимось": "La oss slappe av",
        "Продовжимо?": "Skal vi fortsette?",
        "Подобається?": "Liker du det?"
    },
    "nl": {
        "Йде пошук співрозмовника": "Zoekt naar een gesprekspartner",
        "Співрозмовник знайдений!": "Gesprekspartner gevonden!",
        "Відео не знайдено.": "Video niet gevonden.",
        "Співрозмовник покинув чат": "Gesprekspartner heeft de chat verlaten",
        "Пошук нового співрозмовника": "Zoek een nieuwe gesprekspartner",
        "Пошук нового співрозмовника ⬇️": "Zoek een nieuwe gesprekspartner ⬇️",
        "Авторизуватись": "Inloggen",
        "Зареєструватись": "Registreren",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "Log in of registreer om door te gaan:",
        "Мову встановлено": "Taal ingesteld",
        "👋": "👋",
        "Давай розслабимось": "Laten we ontspannen",
        "Продовжимо?": "Gaan we verder?",
        "Подобається?": "Vind je het leuk?"
    },
    "pt": {
        "Йде пошук співрозмовника": "Procurando por um parceiro",
        "Співрозмовник знайдений!": "Parceiro encontrado!",
        "Відео не знайдено.": "Vídeo não encontrado.",
        "Співрозмовник покинув чат": "O parceiro saiu do chat",
        "Пошук нового співрозмовника": "Encontrar novo parceiro",
        "Пошук нового співрозмовника ⬇️": "Encontrar novo parceiro ⬇️",
        "Авторизуватись": "Entrar",
        "Зареєструватись": "Registrar-se",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "Para continuar, faça login ou registre-se:",
        "Мову встановлено": "Idioma definido",
        "👋": "👋",
        "Давай розслабимось": "Vamos relaxar",
        "Продовжимо?": "Continuamos?",
        "Подобається?": "Você gostou?"
    },
    "ro": {
        "Йде пошук співрозмовника": "Căutare partener de conversație",
        "Співрозмовник знайдений!": "Partener găsit!",
        "Відео не знайдено.": "Video negăsit.",
        "Співрозмовник покинув чат": "Partenerul a părăsit chatul",
        "Пошук нового співрозмовника": "Găsește un nou partener",
        "Пошук нового співрозмовника ⬇️": "Găsește un nou partener ⬇️",
        "Авторизуватись": "Autentificare",
        "Зареєструватись": "Înregistrare",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "Pentru a continua, autentifică-te sau înregistrează-te:",
        "Мову встановлено": "Limba setată",
        "👋": "👋",
        "Давай розслабимось": "Hai să ne relaxăm",
        "Продовжимо?": "Continuăm?",
        "Подобається?": "Îți place?"
    },
    "sk": {
        "Йде пошук співрозмовника": "Hľadá sa partner na rozhovor",
        "Співрозмовник знайдений!": "Partner nájdený!",
        "Відео не знайдено.": "Video nebolo nájdené.",
        "Співрозмовник покинув чат": "Partner opustil chat",
        "Пошук нового співрозмовника": "Nájsť nového partnera",
        "Пошук нового співрозмовника ⬇️": "Nájsť nového partnera ⬇️",
        "Авторизуватись": "Prihlásiť sa",
        "Зареєструватись": "Zaregistrovať sa",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "Na pokračovanie sa prihláste alebo zaregistrujte:",
        "Мову встановлено": "Jazyk nastavený",
        "👋": "👋",
        "Давай розслабимось": "Poďme sa uvoľniť",
        "Продовжимо?": "Pokračujeme?",
        "Подобається?": "Páči sa ti to?"
    },
    "sl": {
        "Йде пошук співрозмовника": "Iskanje sogovornika v teku",
        "Співрозмовник знайдений!": "Sogovornik najden!",
        "Відео не знайдено.": "Video ni bilo najdeno.",
        "Співрозмовник покинув чат": "Sogovornik je zapustil klepet",
        "Пошук нового співрозмовника": "Najdi novega sogovornika",
        "Пошук нового співрозмовника ⬇️": "Najdi novega sogovornika ⬇️",
        "Авторизуватись": "Prijava",
        "Зареєструватись": "Registracija",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "Za nadaljevanje se prijavite ali registrirajte:",
        "Мову встановлено": "Jezik nastavljen",
        "👋": "👋",
        "Давай розслабимось": "Sprostimo se",
        "Продовжимо?": "Nadaljujemo?",
        "Подобається?": "Ti je všeč?"
    },
    "sv": {
        "Йде пошук співрозмовника": "Söker efter samtalspartner",
        "Співрозмовник знайдений!": "Samtalspartner hittad!",
        "Відео не знайдено.": "Video hittades inte.",
        "Співрозмовник покинув чат": "Samtalspartnern lämnade chatten",
        "Пошук нового співрозмовника": "Hitta ny samtalspartner",
        "Пошук нового співрозмовника ⬇️": "Hitta ny samtalspartner ⬇️",
        "Авторизуватись": "Logga in",
        "Зареєструватись": "Registrera dig",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "För att fortsätta, logga in eller registrera dig:",
        "Мову встановлено": "Språk inställt",
        "👋": "👋",
        "Давай розслабимось": "Låt oss slappna av",
        "Продовжимо?": "Ska vi fortsätta?",
        "Подобається?": "Gillar du det?"
    },
    "tr": {
        "Йде пошук співрозмовника": "Bir partner aranıyor",
        "Співрозмовник знайдений!": "Partner bulundu!",
        "Відео не знайдено.": "Video bulunamadı.",
        "Співрозмовник покинув чат": "Partner sohbeti terk etti",
        "Пошук нового співрозмовника": "Yeni bir partner bul",
        "Пошук нового співрозмовника ⬇️": "Yeni bir partner bul ⬇️",
        "Авторизуватись": "Giriş yap",
        "Зареєструватись": "Kaydol",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "Devam etmek için giriş yapın veya kaydolun:",
        "Мову встановлено": "Dil ayarlandı",
        "👋": "👋",
        "Давай розслабимось": "Rahatlayalım",
        "Продовжимо?": "Devam edelim mi?",
        "Подобається?": "Beğendin mi?"
    },
    "zh-cn": {
        "Йде пошук співрозмовника": "正在寻找聊天对象",
        "Співрозмовник знайдений!": "已找到聊天对象！",
        "Відео не знайдено.": "未找到视频。",
        "Співрозмовник покинув чат": "聊天对象已离开",
        "Пошук нового співрозмовника": "寻找新聊天对象",
        "Пошук нового співрозмовника ⬇️": "寻找新聊天对象 ⬇️",
        "Авторизуватись": "登录",
        "Зареєструватись": "注册",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "请登录或注册以继续：",
        "Мову встановлено": "语言已设置",
        "👋": "👋",
        "Давай розслабимось": "让我们放松一下",
        "Продовжимо?": "我们继续？",
        "Подобається?": "你喜欢吗？"
    },
    "ar": {
        "Йде пошук співрозмовника": "جاري البحث عن شريك",
        "Співрозмовник знайдений!": "تم العثور على شريك!",
        "Відео не знайдено.": "لم يتم العثور على الفيديو.",
        "Співрозмовник покинув чат": "غادر الشريك الدردشة",
        "Пошук нового співрозмовника": "ابحث عن شريك جديد",
        "Пошук нового співрозмовника ⬇️": "ابحث عن شريك جديد ⬇️",
        "Авторизуватись": "تسجيل الدخول",
        "Зареєструватись": "إنشاء حساب",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "للمتابعة، يرجى تسجيل الدخول أو إنشاء حساب:",
        "Мову встановлено": "تم تعيين اللغة",
        "👋": "👋",
        "Давай розслабимось": "دعنا نسترخي",
        "Продовжимо?": "هل نتابع؟",
        "Подобається?": "هل أعجبك؟"
    },
    "he": {
        "Йде пошук співрозмовника": "מחפש שותף לשיחה",
        "Співрозмовник знайдений!": "שותף לשיחה נמצא!",
        "Відео не знайдено.": "הווידאו לא נמצא.",
        "Співрозмовник покинув чат": "השותף עזב את הצ'אט",
        "Пошук нового співрозмовника": "מצא שותף חדש",
        "Пошук нового співрозмовника ⬇️": "מצא שותף חדש ⬇️",
        "Авторизуватись": "התחבר",
        "Зареєструватись": "הירשם",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "כדי להמשיך, התחבר או הירשם:",
        "Мову встановлено": "השפה הוגדרה",
        "👋": "👋",
        "Давай розслабимось": "בוא נירגע",
        "Продовжимо?": "נמשיך?",
        "Подобається?": "אהבת את זה?"
    },
    "hi": {
        "Йде пошук співрозмовника": "साथी की तलाश जारी है",
        "Співрозмовник знайдений!": "साथी मिल गया!",
        "Відео не знайдено.": "वीडियो नहीं मिला।",
        "Співрозмовник покинув чат": "साथी ने चैट छोड़ दी",
        "Пошук нового співрозмовника": "नया साथी खोजें",
        "Пошук нового співрозмовника ⬇️": "नया साथी खोजें ⬇️",
        "Авторизуватись": "लॉग इन करें",
        "Зареєструватись": "पंजीकरण करें",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "जारी रखने के लिए लॉग इन करें या पंजीकरण करें:",
        "Мову встановлено": "भाषा सेट की गई",
        "👋": "👋",
        "Давай розслабимось": "चलिए आराम करें",
        "Продовжимо?": "क्या हम जारी रखें?",
        "Подобається?": "क्या आपको पसंद आया?"
    },
    "th": {
        "Йде пошук співрозмовника": "กำลังค้นหาคู่สนทนา",
        "Співрозмовник знайдений!": "พบคู่สนทนาแล้ว!",
        "Відео не знайдено.": "ไม่พบวิดีโอ",
        "Співрозмовник покинув чат": "คู่สนทนาออกจากแชทแล้ว",
        "Пошук нового співрозмовника": "ค้นหาคู่สนทนาใหม่",
        "Пошук нового співрозмовника ⬇️": "ค้นหาคู่สนทนาใหม่ ⬇️",
        "Авторизуватись": "เข้าสู่ระบบ",
        "Зареєструватись": "สมัครสมาชิก",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "หากต้องการดำเนินการต่อ โปรดเข้าสู่ระบบหรือสมัครสมาชิก:",
        "Мову встановлено": "ตั้งค่าภาษาแล้ว",
        "👋": "👋",
        "Давай розслабимось": "มาผ่อนคลายกันเถอะ",
        "Продовжимо?": "ไปต่อไหม?",
        "Подобається?": "คุณชอบไหม?"
    },
    "vi": {
        "Йде пошук співрозмовника": "Đang tìm đối tác trò chuyện",
        "Співрозмовник знайдений!": "Đã tìm thấy đối tác!",
        "Відео не знайдено.": "Không tìm thấy video.",
        "Співрозмовник покинув чат": "Đối tác đã rời khỏi cuộc trò chuyện",
        "Пошук нового співрозмовника": "Tìm đối tác mới",
        "Пошук нового співрозмовника ⬇️": "Tìm đối tác mới ⬇️",
        "Авторизуватись": "Đăng nhập",
        "Зареєструватись": "Đăng ký",
        "Щоб продовжити, авторизуйтесь або зареєструйтесь:": "Để tiếp tục, vui lòng đăng nhập hoặc đăng ký:",
        "Мову встановлено": "Ngôn ngữ đã được thiết lập",
        "👋": "👋",
        "Давай розслабимось": "Hãy thư giãn nào",
        "Продовжимо?": "Tiếp tục nhé?",
        "Подобається?": "Bạn có thích không?"
    }
}

def translate(text, lang_code):
    return TRANSLATIONS.get(lang_code, {}).get(text, text)

completed_chats = set()
chat_search_count = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🌍 Choose language", callback_data="select_language")]]
    try:
        await update.message.reply_text("❗ The bot automatically translates messages", reply_markup=InlineKeyboardMarkup(keyboard))
    except telegram.error.Forbidden:
        print(f"[start] User {update.effective_user.id} blocked the bot.")

async def full_sequence(update: Update, context: ContextTypes.DEFAULT_TYPE, lang_code):
    try:
        message = await update.message.reply_text("⏳")
    except telegram.error.Forbidden:
        return

    for percent in range(10, 101, 10):
        blocks = "🟩" * (percent // 10) + "▫️" * (10 - percent // 10)
        try:
            await message.edit_text(f"⚙️ {translate('Йде пошук співрозмовника', lang_code)}: {percent}%\n\n{blocks}")
        except telegram.error.Forbidden:
            return
        await asyncio.sleep(0.5)

    try:
        await update.message.reply_text(translate("Співрозмовник знайдений!", lang_code))
    except telegram.error.Forbidden:
        return
    await asyncio.sleep(1)

    try:
        video_id = random.choice(VIDEO_NOTE_IDS)
        await context.bot.send_video_note(chat_id=update.effective_chat.id, video_note=video_id)
    except Exception:
        try:
            await update.message.reply_text(translate("Відео не знайдено.", lang_code))
        except telegram.error.Forbidden:
            return

    await asyncio.sleep(2)
    nickname = random.choice(FAKE_USERNAMES)
    try:
        await update.message.reply_text(f"```💬 {nickname}\n\n👋```", parse_mode="MarkdownV2")
        await asyncio.sleep(2)
        phrases = ["Давай розслабимось", "Продовжимо?", "Подобається?"]
        random_phrase = random.choice(phrases)
        translated_phrase = translate(random_phrase, lang_code)
        await update.message.reply_text(f"```💬 {nickname}\n\n{translated_phrase}```", parse_mode="MarkdownV2")
    except telegram.error.Forbidden:
        return

    await asyncio.sleep(4)
    try:
        await update.message.reply_text("🔚 " + translate("Співрозмовник покинув чат", lang_code))
        keyboard = [[InlineKeyboardButton("🔄 " + translate("Пошук нового співрозмовника", lang_code), callback_data="new_search")]]
        await update.message.reply_text("🔄 " + translate("Пошук нового співрозмовника ⬇️", lang_code), reply_markup=InlineKeyboardMarkup(keyboard))
    except telegram.error.Forbidden:
        return

    chat_id = update.effective_chat.id
    chat_search_count[chat_id] = chat_search_count.get(chat_id, 0) + 1

async def half_sequence(update: Update, context: ContextTypes.DEFAULT_TYPE, lang_code):
    try:
        message = await update.callback_query.message.reply_text("⏳")
    except telegram.error.Forbidden:
        return
    for percent in range(10, 51, 10):
        blocks = "🟩" * (percent // 10) + "▫️" * (10 - percent // 10)
        try:
            await message.edit_text(f"⚙️ {translate('Йде пошук співрозмовника', lang_code)}: {percent}%\n\n{blocks}")
        except telegram.error.Forbidden:
            return
        await asyncio.sleep(0.5)

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_search_count.get(chat_id, 0) >= 2:
        try:
            await update.message.reply_text(translate("Щоб продовжити, авторизуйтесь або зареєструйтесь:", user_lang.get(chat_id, 'uk')))
        except telegram.error.Forbidden:
            return
        return
    if chat_id not in user_lang:
        try:
            await update.message.reply_text("First, choose a language")
        except telegram.error.Forbidden:
            return
        return
    return

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat.id
    data = query.data

    if chat_search_count.get(chat_id, 0) >= 2 and data != "new_search":
        try:
            await query.answer()
            await query.message.reply_text(translate("Щоб продовжити, авторизуйтесь або зареєструйтесь:", user_lang.get(chat_id, 'uk')))
        except telegram.error.BadRequest:
            return
        except telegram.error.Forbidden:
            return
        return

    if data == "select_language":
        keyboard, row = [], []
        for i, (lang, code) in enumerate(LANGUAGES.items(), 1):
            row.append(InlineKeyboardButton(lang, callback_data=code))
            if i % 3 == 0:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        try:
            await query.answer()
            await query.message.reply_text("⬇️ Select a language from the list below:", reply_markup=InlineKeyboardMarkup(keyboard))
        except telegram.error.BadRequest:
            return
        except telegram.error.Forbidden:
            return
        return

    if data == "new_search":
        try:
            await query.answer()
        except telegram.error.BadRequest:
            return
        except telegram.error.Forbidden:
            return
        await half_sequence(update, context, user_lang.get(chat_id, 'uk'))
        chat_search_count[chat_id] = chat_search_count.get(chat_id, 0) + 1
        if chat_search_count[chat_id] >= 2:
            buttons = [
                [InlineKeyboardButton(translate("Авторизуватись", user_lang.get(chat_id, 'uk')), url=SMART_LINK)],
                [InlineKeyboardButton(translate("Зареєструватись", user_lang.get(chat_id, 'uk')), url=SMART_LINK)],
            ]
            try:
                await query.message.reply_text(
                    translate("Щоб продовжити, авторизуйтесь або зареєструйтесь:", user_lang.get(chat_id, 'uk')),
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
            except telegram.error.Forbidden:
                return
        return

    user_lang[chat_id] = data
    lang_name = next((k for k, v in LANGUAGES.items() if v == data), "")
    try:
        await query.answer()
        await query.message.reply_text(f"✅ {translate('Мову встановлено', data)}: {lang_name}")
    except telegram.error.BadRequest:
        return
    except telegram.error.Forbidden:
        return

    dummy_update = Update(update.update_id, message=query.message)
    await full_sequence(dummy_update, context, data)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_callback))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_msg))
app.run_polling()
