import logging
import os
import sys


def load_django():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'aruodai.settings'
    sys.path.append(os.getcwd())
    sys.path.append(os.path.join(os.getcwd(), '..'))
    sys.path.append(os.path.join(os.getcwd(), '../..'))
    sys.path.append(os.path.join(os.getcwd(), '../../..'))
    sys.path.append(os.path.join(os.getcwd(), '../../../..'))
    logging.getLogger('django.db.backends').setLevel(logging.ERROR)
    logging.getLogger('django.db.backends').setLevel(logging.INFO)
