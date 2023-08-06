#TODO: remove os.path.insert
import sys, os
sys.path.insert(1, os.path.dirname(os.path.realpath(__file__))+"/../../pbose-python")

class I4TException(Exception):
  pass
