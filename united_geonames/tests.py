"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

"""
 Todo:
1. sukurti aruodai.Vietos irasus:
  A) Su pavadinimu Vilnius, ir sinonimu Wilno
  B) Su pavadinimu TestTrakai ir trakų koordinatėmis
  C) Su 
  D) Su 
  
  
2. 
"""


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
