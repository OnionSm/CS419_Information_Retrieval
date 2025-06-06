import unicodedata
import re
import html
from underthesea import text_normalize
import string
from underthesea import word_tokenize
from typing import List, Set

def remove_punctuation(sentence):
    """
    Loại bỏ dấu câu
    """
    result = sentence.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
    return ' '.join(result.split())


def split_words(sentence):
    """
    Phân đoạn text thành các từ, từ kép hoặc từ đơn
    """
    sentence = word_tokenize(sentence, format='text')
    return sentence


def standardize_unicode(sentence: str) -> str:
    """
    Chuẩn hóa chuỗi Unicode về dạng NFC (Normalization Form C).
    NFC là dạng chuẩn hóa kết hợp (Composition), 
    nơi các ký tự cơ sở và dấu phụ (diacritics) được kết hợp thành một ký tự duy nhất
    nếu có thể. Điều này giúp đảm bảo rằng các chuỗi có vẻ giống nhau
    nhưng được biểu diễn khác nhau ở cấp độ byte sẽ được coi là giống nhau.

    Args:
        sentence (str): Chuỗi văn bản đầu vào.

    Returns:
        str: Chuỗi văn bản đã được chuẩn hóa về dạng NFC.
    """
    sentence = unicodedata.normalize('NFC', sentence)
    return sentence


def remove_emoji(sentence: str) -> str:
    """
    Loại bỏ các ký tự emoji khỏi một chuỗi văn bản.
    Sử dụng một pattern regex mở rộng để bắt nhiều loại emoji hơn.
    """
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"  # enclosed alphanumerics, ideographs, etc.
        "\U0001F900-\U0001F9FF"  # supplemental symbols and pictographs
        "\U0001FA00-\U0001FA6F"  # extended A
        "\U000025AA-\U000025FF"  # miscellaneous symbols
        "\U00002B00-\U00002BFF"  # miscellaneous symbols and arrows
        "\U00002300-\U000023FF"  # miscellaneous technical
        "\U0000200D"            # Zero Width Joiner
        "\U0000FE0F"            # Variation Selector-16
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', sentence)

def normalize_bar(sentence):
    """
    Hàm này dùng để chuẩn hóa kiểu gõ dấu
    """
    sentence = text_normalize(sentence)
    return sentence

def normalize_html(text: str) -> str:
    """
    Chuẩn hóa văn bản đầu vào bằng cách thực hiện các bước sau:
    1. Decode các thực thể HTML.
    2. Xóa các thẻ HTML.
    3. Xóa các loại dấu ngoặc kép.
    4. Xóa ký tự tàng hình và ký tự điều khiển.
    5. Chuẩn hóa xuống dòng thành khoảng trắng đơn.
    6. Chuẩn hóa khoảng trắng thành khoảng trắng đơn.
    7. Cắt bỏ khoảng trắng ở đầu và cuối.

    Args:
        text (str): Chuỗi văn bản đầu vào cần chuẩn hóa.

    Returns:
        str: Chuỗi văn bản đã được chuẩn hóa.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")
    if not text: 
        return ""
    decoded_text = html.unescape(text)
    decoded_text = re.sub(r'<[^>]+>', ' ', decoded_text)

    decoded_text = re.sub(r'["\u201C\u201D\u201E\u201F\u2033\u00AB\u00BB]', '', decoded_text)
    decoded_text = re.sub(r'[\x00-\x1F\u200b\u200e\u202c\u2060\u200c\ufeff]', '', decoded_text)

    decoded_text = decoded_text.replace('\r\n', '\n').replace('\r', '\n')
    # Sau đó, thay thế một hoặc nhiều ký tự xuống dòng bằng một khoảng trắng đơn
    decoded_text = re.sub(r'\n+', ' ', decoded_text)

    # 7. Chuẩn hóa khoảng trắng: thay thế nhiều khoảng trắng thành một khoảng trắng duy nhất
    decoded_text = re.sub(r'\s+', ' ', decoded_text)

    # 8. Cắt bỏ khoảng trắng ở đầu và cuối chuỗi
    return decoded_text.strip()


def keep_latin_vietnamese_and_digits(text: str) -> str:
    """
    Giữ lại chỉ các ký tự Latin, tiếng Việt, số và khoảng trắng
    """

    cleaned_text = re.sub(
        r'[^a-zA-Z0-9\s' +
        'áàảãạăằắặẳẵâầấậẩẫđéèẻẽẹêềếệểễíìỉĩịóòỏõọôồốộổỗơờớợởỡúùủũụưừứựửữýỳỷỹỵ' +
        'ÁÀẢÃẠĂẰẮẶẲẴÂẦẤẬẨẪĐÉÈẺẼẸÊỀẾỆỂỄÍÌỈĨỊÓÒỎÕỌÔỒỐỘỔỖƠỜỚỢỞỠÚÙỦŨỤƯỪỨỰỬỮÝỲỶỸỴ' +
        ']',
        '',
        text
    )
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    cleaned_text = cleaned_text.strip()
    
    return cleaned_text


def to_lower(sentence):
    sentence = sentence.lower()
    return sentence

def remove_stopwords(sentence, stop_words):
    filtered_word = [w for w in sentence.split() if not w in stop_words] 
    return " ".join(filtered_word)

def remove_malayalam(text: str) -> str:
    """
    Xóa ký tự Malayalam nhưng giữ nguyên cấu trúc văn bản (xuống dòng, tab)
    """
    # Chỉ xóa ký tự Malayalam, không xử lý khoảng trắng
    cleaned_text = re.sub(r'[\u0D00-\u0D7F]', '', text)
    
    return cleaned_text

def remove_special_characters(text):
    return re.sub(r'[^a-zA-Z0-9À-ỹà-ỹ\s]', '', text)


stop_word_file_path = 'vietnamese-stopwords.txt' 
with open(stop_word_file_path, 'r', encoding='utf-8') as f:
    content = f.read()
list_stop_words = content.split("\n")
VIETNAMESE_STOPWORDS = set(list_stop_words)

def process_text(text: str) -> List[str]:
    """
    Xử lý văn bản đầu vào chứa cả tiếng Việt và tiếng Anh theo pipeline (KHÔNG STEMMING):
    1. Tokenization (Tách từ - Ưu tiên underthesea cho tiếng Việt)
    2. Lowercase (Chuyển chữ hoa về chữ thường)
    3. Punctuations (Loại bỏ dấu câu - Giữ nguyên dấu tiếng Việt)
    4. Stopword (Loại bỏ stopword - Cả tiếng Việt và tiếng Anh)

    Args:
        text (str): Chuỗi văn bản đầu vào.

    Returns:
        List[str]: Danh sách các 'term' đã được xử lý.
    """
    text = normalize_html(text)
    text = remove_malayalam(text)
    text = remove_emoji(text)
    text = remove_punctuation(text)
    text = remove_special_characters(text)
    text = to_lower(text)
    text = standardize_unicode(text)
    text = normalize_bar(text)
    text = split_words(text)
    text = remove_stopwords(text, VIETNAMESE_STOPWORDS)

    final_terms = [w for w in text.split()]
    return final_terms

