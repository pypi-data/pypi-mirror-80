
import numpy as np 
import pandas as pd
from inltk.inltk import setup
import warnings
warnings.filterwarnings('ignore')


# In[5]:


def similar_Text_Generation():
   
    text=input("\n<<<<<<<<<<<Enter Your Text to Generate similar kind of text>>>>>>>>>\n")
    print('\n')
    from inltk.inltk import get_similar_sentences
    print("<<<<<<<Your generated 5 similar sentences>>>>>>>>>>")
    df=get_similar_sentences(text, 5, 'en', degree_of_aug = 0.1)
    return df
## Text Generation based on Previous Words
def text_Generation_Based_on_Previous_Words():
    text1=input("\n<<<<<<<<<<<Enter Your Text to Generate words based on Previous Words>>>>>>>>>\n")
    print('\n')
    from inltk.inltk import predict_next_words
    print("<<<<<<<Your generated similar Words>>>>>>>>>>")
    df1=predict_next_words(text1 , 6, 'en') 
    return df1

##Nepali text generation
def nepali_Similar_Text_Generation():
   
    text2=input("\n<<<<<<<<<<<Enter Your Nepali Text to Generate similar kind of text>>>>>>>>>\n")
    print('\n')
    from inltk.inltk import get_similar_sentences
    print("<<<<<<<Your generated 5 similar Nepali sentences>>>>>>>>>>")
    df2=get_similar_sentences(text2, 5, 'ne', degree_of_aug = 0.1)
    return df2
## Text Generation based on Previous Words
def nepali_Text_Generation_Based_on_Previous_Words():
    text3=input("\n<<<<<<<<<<<Enter Your Nepali  Text to Generate words based on Previous Words>>>>>>>>>\n")
    print('\n')
    from inltk.inltk import predict_next_words
    print("<<<<<<<Your generated Nepali similar Words>>>>>>>>>>")
    df3=predict_next_words(text3 , 6, 'ne') 
    return df3





#nepali_Similar_Text_Generation()

