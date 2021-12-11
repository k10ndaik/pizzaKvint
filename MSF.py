from transitions import Machine, State
from baza import *
import pickle

class Zakaz(object):
    def __init__(self):
        self.otvet = 'Какую вы хотите пиццу? Большую или маленькую?'
    def on_enter_size(self): self.otvet = 'Какую вы хотите пиццу? Большую или маленькую?'
    def on_enter_money(self): self.otvet = 'Как вы будете платить?'
    def on_enter_confirmation(self): self.otvet = 'Вы хотите большую пиццу, оплата - наличкой?'
    def on_enter_stop(self): self.otvet = 'Спасибо за заказ'
    def on_enter_start(self): self.otvet = 'Какую вы хотите пиццу? Большую или маленькую?'

class Pizza():
    def __init__(self):
        self.zakaz = Zakaz()
        self.states = ['start', 'size', 'money', 'confirmation', 'stop']
        self.transitions = [
            { 'trigger': 'start', 'source': 'start', 'dest': 'size' },
            { 'trigger': 'size', 'source': 'size', 'dest': 'money' },
            { 'trigger': 'money', 'source': 'money', 'dest': 'confirmation' },
            { 'trigger': 'confirmation', 'source': 'confirmation', 'dest': 'stop' },
            { 'trigger': 'stop', 'source': 'stop', 'dest': 'start' }
            ]
        self.machine = Machine(self.zakaz,states=self.states, transitions=self.transitions, initial='start' )

class Otvet():
    def __init__(self, user_id, text):
        self.user_id = user_id
        self.text = text
        self.state_ID = cur.execute('SELECT state FROM states WHERE id == ?', (self.user_id,))
        if self.state_ID.fetchone() is None:
            self.newZacaz = Pizza()
            cur.execute('INSERT INTO states VALUES(?,?)', (self.user_id, pickle.dumps(self.newZacaz)))
            base.commit()
        else:
            self.oldZacaz = pickle.loads(cur.execute('SELECT state FROM states WHERE id == ?', (self.user_id,)).fetchone()[0])
            if self.oldZacaz.zakaz.is_start():
                self.oldZacaz.zakaz.start()
                self.otvet = self.oldZacaz.zakaz.otvet
                cur.execute('UPDATE states SET state = ? WHERE id == ?', (pickle.dumps(self.oldZacaz), self.user_id))
                base.commit()
            elif self.oldZacaz.zakaz.is_size() and 'бол' in self.text.lower():
                self.oldZacaz.zakaz.size()
                self.otvet = self.oldZacaz.zakaz.otvet
                cur.execute('UPDATE states SET state = ? WHERE id == ?', (pickle.dumps(self.oldZacaz), self.user_id))
                base.commit()
            elif self.oldZacaz.zakaz.is_money() and 'нал' in self.text.lower():
                self.oldZacaz.zakaz.money()
                self.otvet = self.oldZacaz.zakaz.otvet
                cur.execute('UPDATE states SET state = ? WHERE id == ?', (pickle.dumps(self.oldZacaz), self.user_id))
                base.commit()
            elif self.oldZacaz.zakaz.is_confirmation() and 'да' in self.text.lower():
                self.oldZacaz.zakaz.confirmation()
                self.otvet = self.oldZacaz.zakaz.otvet
                cur.execute('UPDATE states SET state = ? WHERE id == ?', (pickle.dumps(self.oldZacaz), self.user_id))
                base.commit()
            elif self.oldZacaz.zakaz.is_stop():
                self.oldZacaz.zakaz.stop()
                self.otvet = self.oldZacaz.zakaz.otvet
                cur.execute('UPDATE states SET state = ? WHERE id == ?', (pickle.dumps(self.oldZacaz), self.user_id))
                base.commit()

        self.otvet = pickle.loads(cur.execute('SELECT state FROM states WHERE id == ?', (self.user_id,)).fetchone()[0]).zakaz.otvet





