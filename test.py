import unittest
from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
      self.client = app.test_client()
      app.config['TESTING'] = True
      

    def test_show_board(self):
        with self.client:
          res = self.client.get('/')
          self.assertIsNone(session.get('highscore'))
          self.assertIn(b'<p>Highscore:',res.data)
          self.assertIn(b'<p>Number of play:',res.data)
            
    
    def test_count_play(self):
        with self.client as client:
          with client.session_transaction() as sess:
             sess['nOfPlay'] = 10
      
          self.client.get('/')
          self.assertEqual(session['nOfPlay'],10)
            

    def test_valid_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["D", "O", "G", "G", "G"], 
                                 ["D", "O", "G", "G", "G"], 
                                 ["D", "O", "G", "G", "G"], 
                                 ["D", "O", "G", "G", "G"], 
                                 ["D", "O", "G", "G", "G"]]
        response = self.client.get('/check-word?word=dog')
        self.assertEqual(response.json['result'], 'ok')
            
    
    def test_invalid_word(self):
        self.client.get('/')
        response = self.client.get('/check-word?word=beautiful')
         
        self.assertEqual(response.json['result'], 'not-on-board')

            

    def test_valid_english(self):
        self.client.get('/')
        response = self.client.get('/check-word?word=osldjedjbf')
        self.assertEqual(response.json['result'],'not-word')
         




if __name__ =='__main__':
    unittest.main()