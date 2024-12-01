from moduls.ner_natasha import NER_NATASHA

object_ner = NER_NATASHA()
text = open('../data/test_chat/chat_example.txt', 'r', encoding='utf-8').read()

doc_spans = object_ner.extract_ner(text)
for span in doc_spans:
    print(f"Сущность: {span.text}, Тип: {span.type}")

zamena = object_ner.replace_words(text, doc_spans)
print(zamena)