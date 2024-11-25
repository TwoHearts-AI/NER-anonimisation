from moduls.ner_natasha import NER_NATASHA

object_ner = NER_NATASHA()
text = "Москва — столица России, а Владимир Путин — президент страны. номер +79174520180, паспорт: 8676 345676"
doc_spans = object_ner.extract_ner(text)
for span in doc_spans:
    print(f"Сущность: {span.text}, Тип: {span.type}")