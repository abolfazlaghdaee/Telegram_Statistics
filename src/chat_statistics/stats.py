import json
from pathlib import Path
from typing import Union

import arabic_reshaper
from arabic_reshaper import arabic_reshaper
from bidi.algorithm import get_display
from hazm import Normalizer, word_tokenize
from loguru import logger
from src.data import DATA_DIR
from wordcloud import WordCloud


class ChatStatistics:
    """Generate chat statistics from a telegram chat jason file
    """


    def __init__(self, chat_json : Union[str, Path]):


        logger.info(f"loadin chat data from {chat_json}")
        #load chat data
        with open(chat_json) as f:
            self.chat_data = json.load(f)

        self.normalizer = Normalizer()


        #load stopwords
        logger.info(f"loading stopwords from {DATA_DIR / 'stopword.txt'}")
        stop_words = open(DATA_DIR /'stopwords.txt').readlines()
        stop_words = list(map(str.strip, stop_words))
        self.stop_words = list(map(self.normalizer.normalize, stop_words))
        

    def generate_word_cloud(self, output_dir: Union[str, Path]):
        text_content = ''


        for msg in self.chat_data['messages']:
            if type(msg['text']) is str: 
               tokens  =  word_tokenize(msg['text'])
               tokens= filter(lambda item:item  not in  self.stop_words, tokens)
            
            
            
               text_content += f"{' '.join(tokens)}"
    
        #normaalize reshape for word cloud
        text_content = self.normalizer.normalize(text_content)
        text_content = arabic_reshaper.reshape(text_content)
        #text_content = get_display(text_content)
        

        #generate word cloud
        wordcloud = WordCloud( 
            width=1200,
            height=1200,
            font_path= str(DATA_DIR / "BHoma.ttf"),
            background_color = 'white'
        ).generate(text_content)

        wordcloud.to_file(str(Path(output_dir) / 'wordcloud.png'))


if __name__ =='__main__':
    chat_stats = ChatStatistics(chat_json= DATA_DIR / 'online.json')
    chat_stats.generate_word_cloud(output_dir=DATA_DIR)

    print('done')
