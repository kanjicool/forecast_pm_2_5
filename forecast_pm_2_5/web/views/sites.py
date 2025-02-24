from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import current_user
# from forecast_pm_2_5.models import (
#     predict_sequence,
#     text_to_sequence,
#     get_vocab,
#     load_translation_model,
#     translate_text,
# )
import logging
# import numpy as np
# import sentencepiece as spm


module = Blueprint("site", __name__)


# โหลดโมเดลและ tokenizer
# model = load_translation_model()
# en_sp = spm.SentencePieceProcessor()
# th_sp = spm.SentencePieceProcessor()
# en_sp.load("rnn_translate/utils/data/en_sp.model")
# th_sp.load("rnn_translate/utils/data/th_sp.model")

logging.basicConfig(level=logging.DEBUG)


@module.route("/")
def index():
    return render_template("/site/index.html")
