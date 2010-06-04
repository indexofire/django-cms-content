#!/usr/bin/python
#
# Copyright (C) 2009, DaNmarner danmarner(at)gmail dot com
#
# Originally written by Peteris Krumins (peter@catonmat.net)
# http://www.catonmat.net/blog/python-library-for-google-translate/
#
# Code is licensed under MIT license.

''' A wrapper for Google AJAX Langugae API with GAE support '''
import urllib2
from urllib import quote_plus

try:
    import simplejson
except ImportError:
    try:
        from django.utils import simplejson
    except ImportError:
        pass

# support Google App Engine.  GAE does not have a working urllib.urlopen.
try:
    from google.appengine.api import urlfetch

    def urlread(url, data=None):
        if data is not None:
            headers = {"Content-type": "application/x-www-form-urlencoded"}
            method = urlfetch.POST
        else:
            headers = {}
            method = urlfetch.GET

        result = urlfetch.fetch(url, method=method,
                                payload=data, headers=headers)
        
        if result.status_code == 200:
            return result.content
        else:
            raise urllib2.URLError("fetch error url=%s, code=%d" % (url, result.status_code))

except ImportError:
    def urlread(url, data=None):
        res = urllib2.urlopen(url, data=data)
        return res.read()
 

class TranslationError(Exception):
    pass

class Translator(object):
    ''' Wrapper for Google AJAX Language API.'''

    translate_url = "http://ajax.googleapis.com/ajax/services/language/translate?v=1.0&q=%(message)s&langpair=%(from)s%%7C%(to)s"
    detect_url = "http://ajax.googleapis.com/ajax/services/language/detect?v=1.0&q=%(message)s"

    def __init__(self):
        self.urlread = urlread

    def translate(self, message, lang_to='en', lang_from=''):
        """
        Given a 'message' translate it from 'lang_from' to 'lang_to'.
        If 'lang_from' is empty, auto-detects the language.
        Returns the translated message.
        """
        if lang_to not in _languages:
            raise TranslationError, "Language %s is not supported as lang_to." % lang_to
        if lang_from not in _languages and lang_from != '':
            raise TranslationError, "Language %s is not supported as lang_from." % lang_from

        message = quote_plus(message)
        real_url = Translator.translate_url % { 'message': message,
                                                'from':    lang_from,
                                                'to':      lang_to }

        try:
            translation = self.urlread(real_url)
            data = simplejson.loads(translation)

            if data['responseStatus'] != 200:
                raise TranslationError, "Failed translating: %s" % data['responseDetails']

            return data['responseData']['translatedText']

        except ValueError, e:
            raise TranslationError, "Failed translating (json failed): %s" % e.message
        except KeyError, e:
            raise TranslationError, "Failed translating, response didn't contain the translation"

        return None

    def detect(self, message):
        """
        Given a 'message' detects its language.
        Returns Language object.
        """

        message = quote_plus(message)
        real_url = Translator.detect_url % { 'message': message }

        try:
            detection = self.urlread(real_url)
            data = simplejson.loads(detection)

            if data['responseStatus'] != 200:
                raise DetectError, "Failed detecting language: %s" % data['responseDetails']

            rd = data['responseData']
            return Language(rd['language'], rd['confidence'], rd['isReliable'])

        except ValueError, e:
            raise DetectErrro, "Failed detecting language (json failed): %s" % e.message
        except KeyError, e:
            raise DetectError, "Failed detecting language, response didn't contain the necessary data"

        return None

class DetectionError(Exception):
    pass

class Language(object):
    def __init__(self, lang, confidence, is_reliable):
        self.lang_code = lang
        self.lang = _languages[lang]
        self.confidence = confidence
        self.is_reliable = is_reliable

    def __repr__(self):
        return '<Language: %s (%s)>' % (self.lang_code, self.lang)


_languages = {
  'af': 'Afrikaans',
  'sq': 'Albanian',
  'am': 'Amharic',
  'ar': 'Arabic',
  'hy': 'Armenian',
  'az': 'Azerbaijani',
  'eu': 'Basque',
  'be': 'Belarusian',
  'bn': 'Bengali',
  'bh': 'Bihari',
  'bg': 'Bulgarian',
  'my': 'Burmese',
  'ca': 'Catalan',
  'chr': 'Cherokee',
  'zh': 'Chinese',
  'zh-CN': 'Chinese_simplified',
  'zh-TW': 'Chinese_traditional',
  'hr': 'Croatian',
  'cs': 'Czech',
  'da': 'Danish',
  'dv': 'Dhivehi',
  'nl': 'Dutch',
  'en': 'English',
  'eo': 'Esperanto',
  'et': 'Estonian',
  'tl': 'Filipino',
  'fi': 'Finnish',
  'fr': 'French',
  'gl': 'Galician',
  'ka': 'Georgian',
  'de': 'German',
  'el': 'Greek',
  'gn': 'Guarani',
  'gu': 'Gujarati',
  'iw': 'Hebrew',
  'hi': 'Hindi',
  'hu': 'Hungarian',
  'is': 'Icelandic',
  'id': 'Indonesian',
  'iu': 'Inuktitut',
  'ga': 'Irish',
  'it': 'Italian',
  'ja': 'Japanese',
  'kn': 'Kannada',
  'kk': 'Kazakh',
  'km': 'Khmer',
  'ko': 'Korean',
  'ku': 'Kurdish',
  'ky': 'Kyrgyz',
  'lo': 'Laothian',
  'lv': 'Latvian',
  'lt': 'Lithuanian',
  'mk': 'Macedonian',
  'ms': 'Malay',
  'ml': 'Malayalam',
  'mt': 'Maltese',
  'mr': 'Marathi',
  'mn': 'Mongolian',
  'ne': 'Nepali',
  'no': 'Norwegian',
  'or': 'Oriya',
  'ps': 'Pashto',
  'fa': 'Persian',
  'pl': 'Polish',
  'pt-PT': 'Portuguese',
  'pa': 'Punjabi',
  'ro': 'Romanian',
  'ru': 'Russian',
  'sa': 'Sanskrit',
  'sr': 'Serbian',
  'sd': 'Sindhi',
  'si': 'Sinhalese',
  'sk': 'Slovak',
  'sl': 'Slovenian',
  'es': 'Spanish',
  'sw': 'Swahili',
  'sv': 'Swedish',
  'tg': 'Tajik',
  'ta': 'Tamil',
  'tl': 'Tagalog',
  'te': 'Telugu',
  'th': 'Thai',
  'bo': 'Tibetan',
  'tr': 'Turkish',
  'uk': 'Ukrainian',
  'ur': 'Urdu',
  'uz': 'Uzbek',
  'ug': 'Uighur',
  'vi': 'Vietnamese',
  'cy': 'Welsh',
  'yi': 'Yiddish'
};
