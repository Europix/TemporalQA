import spacy
import re

nlp = spacy.load("en_core_web_sm")


def check_time_reference(target_question):
    key = None
    doc = nlp(target_question)
    flag = False
    for token in doc:
        if token.pos_ == "DATE" or token.pos_ == "TIME":
            flag = True
            key = token
    for ent in doc.ents:
        if ent.label_ == "DATE" or ent.label_ == "TIME":
            flag = True
            key = ent
    target_question = target_question.lower()

    pattern = r'\b(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-](\d{4}|\d{2})\b'
    # Search for dd/mm/yyyy or dd-mm-yyyy
    match = re.search(pattern, target_question)
    if match:
        flag = True
        key = match
        return flag, key

    pattern2 = re.compile(r"\b\d{1,4}-\d{1,4}-\d{1,4}\b")
    # Search for yyyy-mm-dd
    match2 = pattern2.findall(target_question)
    if match2:
        flag = True
        key = match2
        return flag, key

    pattern3 = re.compile(r"\b\d{3,4}\b")
    # Search for year
    match3 = pattern3.findall(target_question)
    if match3:
        if "on" in target_question or "in" in target_question:
            flag = True
            key = match3
            # return flag,key

    # if "what" in target_question:
    #    if "year" in target_question or "time" in target_question:
    #       return True
    # What time? what year?

    anti_words = ['boeing', '$']
    for words in anti_words:
        if words in target_question and flag == True:
            flag = False  # Extract other numerical items.
            key = None

    pattern_pop = re.compile(r"\b\d{5,}\b")
    if pattern_pop.findall(target_question) and "population" in target_question and flag == True:
        flag = False
        key = None
        key = str(key) + "-0-0"

    return flag, key


def check_implicit(target_question):
    # doc = nlp(target_question.title())
    # 全部大写 方便表达式比对
    # List A 是要进行比对的短语/词句
    listA = []
    # listA.append('When')
    # listA.append('What Time')
    # listA.append('What Year')
    # listA.append('Now')
    # listA.append('During')
    time_references = []
    keywords = ['after', 'precede', 'before', 'when', 'during']

    # Iterate through the list of keywords and check if they are present in the sentence
    for keyword in keywords:
        if keyword in target_question.lower():
            # time_references.append(keyword)
            return True, keyword
    # if time_references:
    #    return True
    return False, None
    # return time_references


def ordinal_check(target_question):
    ordinal = []
    ordinal_words = re.findall(r'\b[0-9]+(st|nd|rd|th)\b', target_question.lower())
    if ordinal_words:
        return True, ordinal_words
    ordinal_words = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth",
                     "eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth", "sixteenth", "seventeenth",
                     "eighteenth", "nineteenth", "twentieth", "twenty-first", "twenty-second", "twenty-third",
                     "twenty-fourth", "twenty-fifth", "twenty-sixth", "twenty-seventh", "twenty-eighth",
                     "twenty-ninth", "thirtieth", "thirty-first", '1st', '2nd', '3rd', '4th', '5th', '6th', '7th',
                     '8th', '9th', '10th',
                     'precede', 'oldest', 'last', 'latest', 'earliest', 'ordinal', 'most recent', 'eldest', 'youngest']

    # [ last ] instead of [last] for a single word.

    for words in ordinal_words:
        if words in target_question.lower():
            # ordinal.append(words)
            return True, words

    return False, None
    # if time_references:
    #    return True

    # return time_references
    # return re.search(ordinal_question_pattern, sentence, re.IGNORECASE) is not None

