import random
import role as R

class zbrist:
    def init(self, size):
        self.com = []
        self.hum = []
        self.code = random.randint(1, 10000000000)
        for i in range(size*size):
            self.com.append(random.randint(1, 10000000000))
            self.hum.append(random.randint(1, 10000000000))
    def go(self,x,y,role):
        index = x*15+y
        self.code ^= self.com[index] if role==R.com else self.hum[index]
        return self.code
    #init(15)
z = zbrist()
z.init(15)