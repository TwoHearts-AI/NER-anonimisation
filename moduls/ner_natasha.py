import pymorphy2

from natasha import (
    Segmenter,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    Doc
)
import data.names
class NER_NATASHA:
    def __init__(self):
        self.segmenter = Segmenter()
        self.emb = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(self.emb)
        self.syntax_parser = NewsSyntaxParser(self.emb)
        self.ner_tagger = NewsNERTagger(self.emb)

    def extract_ner(self, text):
        doc = Doc(text)
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)
        doc.parse_syntax(self.syntax_parser)
        doc.tag_ner(self.ner_tagger)
        return doc.spans

    def replace_words(self, text, spans):
        morph = pymorphy2.MorphAnalyzer()

        dict_spans = {}
        spans_type_dict = {
            'female_names': open('../data/names/female_names_rus.txt', 'r', encoding='utf-8').read().split(sep='\n'),
            'male_names': open('../data/names/male_names_rus.txt', 'r', encoding='utf-8').read().split(sep='\n'),
            'male_surnames_names': open('../data/names/male_surnames_rus.txt', 'r', encoding='utf-8').read().split(sep='\n'),
            'company': open('../data/names/company.txt', 'r', encoding='utf-8').read().split(sep='\n'),
            'locations': open('../data/names/location.txt', 'r', encoding='utf-8').read().split(sep='\n'),
        }

        female_names_cnt = 0
        male_names_cnt = 0
        male_surnames_names_cnt = 0
        company_cnt = 0
        locations_cnt = 0

        for span in spans:
            if span.text not in dict_spans:

                if span.type == 'PER':
                    if len(span.text.split()) >= 2:
                        dict_spans[span.text] = spans_type_dict['male_names'][male_names_cnt] + ' ' + spans_type_dict['male_surnames_names'][male_names_cnt]
                        male_names_cnt += 1
                        male_surnames_names_cnt += 1
                        continue

                    parsed_word = morph.parse(span.text)[0]

                    if parsed_word.tag.gender == 'femn':
                        dict_spans[span.text] = spans_type_dict['female_names'][female_names_cnt]
                        female_names_cnt += 1
                        continue

                    if parsed_word.tag.gender == 'masc':
                        dict_spans[span.text] = spans_type_dict['male_names'][male_names_cnt]
                        male_names_cnt += 1
                        continue

                if span.type == 'ORG ':
                    dict_spans[span.text] = spans_type_dict['company'][company_cnt]
                    company_cnt += 1
                    continue

                if span.type == 'LOC':
                    dict_spans[span.text] = spans_type_dict['locations'][locations_cnt]
                    locations_cnt += 1
                    continue
        for old_word, new_word in dict_spans.items():
            text = text.replace(old_word, new_word)

        return text

