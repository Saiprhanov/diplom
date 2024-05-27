import logging
import asyncio
import config
from language.TRL import tran
from aiogram import Bot,F, Router
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup ,KeyboardButton,InlineKeyboardMarkup, InlineKeyboardButton,callback_query
import psycopg2
from main import user_sessions

def language_markup():
    markup_lang = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
        [InlineKeyboardButton(text='🇷🇺 Русский', callback_data='ru')],
        [InlineKeyboardButton(text='🇬🇧 English', callback_data='en')],
        [InlineKeyboardButton(text='🇰🇿 Қазақша', callback_data='kk')]
    ])
    return markup_lang



def get_on_start_kb(language:str):
    butons_help = KeyboardButton(text=tran[language]['HELP'])
    button_sso= KeyboardButton(text=tran[language]['OR'])
    button_politech= KeyboardButton(text=tran[language]['OB'])
    button_korpusa= KeyboardButton(text=tran[language]['LIST'])
    button_GAL= KeyboardButton(text=tran[language]['GL'])
    button_faq=KeyboardButton(text=tran[language]['FAQ'])
    button_ins=KeyboardButton(text=tran[language]['INS'])
    button_onai=KeyboardButton(text=tran[language]['ONAI'])
    b2=[butons_help]
    b3=[button_sso]
    b4=[button_politech]
    b5=[button_korpusa]
    b6=[button_faq]
    b7=[button_ins]
    b8=[button_onai]
    b9=[button_GAL]
    markup=ReplyKeyboardMarkup(keyboard=[b5,b7,b3,b8,b4,b6,b9,b2])
    return markup


def get_on_ob(language:str): ##Бұл жатахананың перне тақтасын
    bt_one=KeyboardButton(text=tran[language]['OB1'])
    bt_two=KeyboardButton(text=tran[language]['OB2'])
    bt_three=KeyboardButton(text=tran[language]['OB3'])
    bt_ob_help=KeyboardButton(text=tran[language]['OBHELP'])
    bt_ob_revers=KeyboardButton(text=tran[language]['TWO'])
    ob1=[bt_one]
    ob2=[bt_two]
    ob3=[bt_three]
    ob_help=[bt_ob_help]
    ob_revers=[bt_ob_revers]
    get_ob=ReplyKeyboardMarkup(keyboard=[ob1,ob2,ob3,ob_help,ob_revers])
    return get_ob



def get_on_gal(language:str): ## Бұл голоссари
    bt_gal1=KeyboardButton(text=tran[language]['GAL1'])
    bt_gal2=KeyboardButton(text=tran[language]['GAL2'])
    bt_gal3=KeyboardButton(text=tran[language]['GAL3'])
    bt_gal4=KeyboardButton(text=tran[language]['GAL4'])
    bt_gal5=KeyboardButton(text=tran[language]['GAL5'])
    bt_gal6=KeyboardButton(text=tran[language]['GAL6'])
    bt_gal7=KeyboardButton(text=tran[language]['GAL7'])
    bt_gal8=KeyboardButton(text=tran[language]['GAL8'])
    bt_gal9=KeyboardButton(text=tran[language]['GAL9'])
    bt_gal10=KeyboardButton(text=tran[language]['GAL10'])
    bt_gal11=KeyboardButton(text=tran[language]['GAL11'])
    bt_gal12=KeyboardButton(text=tran[language]['GAL12'])
    bt_gal13=KeyboardButton(text=tran[language]['GAL13'])
    bt_gal14=KeyboardButton(text=tran[language]['GAL14'])
    bt_gal15=KeyboardButton(text=tran[language]['GAL15'])
    bt_gal16=KeyboardButton(text=tran[language]['GAL16'])
    bt_gal17=KeyboardButton(text=tran[language]['GAL17'])
    bt_gal18=KeyboardButton(text=tran[language]['GAL18'])
    bt_gal19=KeyboardButton(text=tran[language]['GAL19'])
    bt_gal20=KeyboardButton(text=tran[language]['GAL20'])
    bt_gal21=KeyboardButton(text=tran[language]['GAL21'])
    bt_gal22=KeyboardButton(text=tran[language]['GAL22'])
    bt_gal23=KeyboardButton(text=tran[language]['GAL23'])
    bt_gal24=KeyboardButton(text=tran[language]['GAL24'])
    bt_galone=KeyboardButton(text=tran[language]['ONE'])
    gl1=[bt_gal1,bt_gal2]
    gl2=[bt_gal3,bt_gal4]
    gl3=[bt_gal5,bt_gal6]
    gl4=[bt_gal7,bt_gal8]
    gl5=[bt_gal9,bt_gal10]
    gl6=[bt_gal11,bt_gal12]
    gl7=[bt_gal13,bt_gal14]
    gl8=[bt_gal15,bt_gal16]
    gl9=[bt_gal17,bt_gal18]
    gl10=[bt_gal19,bt_gal20]
    gl11=[bt_gal21,bt_gal22]
    gl12=[bt_gal23,bt_gal24]
    gl13=[bt_galone]
    get_gal=ReplyKeyboardMarkup(keyboard=[gl1,gl2,gl3,gl4,gl5,gl6,gl7,gl8,gl9,gl10,gl11,gl2,gl13])
    return get_gal





def get_on_faq(language:str): ## Бұл жерде көп қойылатын сұрақтар
    bt_faq1=KeyboardButton(text=tran[language]['faq1'])
    bt_faq2=KeyboardButton(text=tran[language]['faq2'])
    bt_faq3=KeyboardButton(text=tran[language]['faq3'])
    bt_faq4=KeyboardButton(text=tran[language]['faq4'])
    bt_faq5=KeyboardButton(text=tran[language]['faq5'])
    bt_faq6=KeyboardButton(text=tran[language]['faq6'])
    bt_faq7=KeyboardButton(text=tran[language]['ONE'])
    f1=[bt_faq1]
    f2=[bt_faq2]
    f3=[bt_faq3]
    f4=[bt_faq4]
    f5=[bt_faq5]
    f6=[bt_faq6]
    f7=[bt_faq7]
    get_faq=ReplyKeyboardMarkup(keyboard=[f1,f2,f3,f4,f5,f6,f7])
    return get_faq





def get_on_korpusa(language:str): ##Бұл жерде корпустар реттестіреуге болады
    bt_guk=KeyboardButton(text=tran[language]['GUK'])
    bt_gmk=KeyboardButton(text=tran[language]['GMK'])
    bt_nk=KeyboardButton(text=tran[language]['NK'])
    bt_muk=KeyboardButton(text=tran[language]['MUK'])
    bt_tk=KeyboardButton(text=tran[language]['TK'])
    bt_start=KeyboardButton(text=tran[language]['ONE'])
    k1=[bt_guk]
    k2=[bt_gmk]
    k3=[bt_muk]
    k4=[bt_nk]
    k5=[bt_tk]
    k6=[bt_start]
    korpys=ReplyKeyboardMarkup(keyboard=[k1,k2,k3,k4,k5,k6])
    return korpys




def get_on_ins(language:str):## Интитуттарды реттейтін бөлім
    bt_in1=KeyboardButton(text=tran[language]['IN1'])
    bt_in2=KeyboardButton(text=tran[language]['IN2'])
    bt_in3=KeyboardButton(text=tran[language]['IN3'])
    bt_in4=KeyboardButton(text=tran[language]['IN4'])
    bt_in5=KeyboardButton(text=tran[language]['IN5'])
    bt_in6=KeyboardButton(text=tran[language]['IN6'])
    bt_in7=KeyboardButton(text=tran[language]['IN7'])
    bt_one=KeyboardButton(text=tran[language]['ONE'])
    k_in1=[bt_in1]
    k_in2=[bt_in2]
    k_in3=[bt_in3]
    k_in4=[bt_in4]
    k_in5=[bt_in5]
    k_in6=[bt_in6]
    k_in7=[bt_in7]
    k_in8=[bt_one]
    ins=ReplyKeyboardMarkup(keyboard=[k_in1,k_in2,k_in3,k_in4,k_in5,k_in6,k_in7,k_in8])
    return ins
