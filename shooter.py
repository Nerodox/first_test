from pygame import *
from random import randint
from time import time as timer 
font.init()
font1 = font.SysFont(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))


font2 = font.SysFont(None, 36)


#mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.play()
#fire_sound = mixer.Sound('fire.ogg')
img_back = "galaxy.jpg" #фон игры
img_bullet = "bullet.png" #пуля
img_hero = "rocket.png" #герой
img_enemy = "ufo.png" #враг
img_ast = "asteroid.png" #астероид


score = 0 #сбито кораблей
goal = 20 #столько кораблей нужно сбить для победы
lost = 0 #пропущено кораблей
max_lost = 10 #проиграли, если пропустили столько кораблей
life = 3  #очки жизни


#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
#конструктор класса
  def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
      #вызываем конструктор класса (Sprite):
      sprite.Sprite.__init__(self)
      #каждый спрайт должен хранить свойство image - изображение
      self.image = transform.scale(image.load(player_image), (size_x, size_y))
      self.speed = player_speed
      #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
      self.rect = self.image.get_rect()
      self.rect.x = player_x
      self.rect.y = player_y
#метод, отрисовывающий героя на окне
  def reset(self):
      window.blit(self.image, (self.rect.x, self.rect.y))
#класс главного игрока
class Player(GameSprite):
  #метод для управления спрайтом стрелками клавиатуры
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed


   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)
#класс спрайта-врага 
class Enemy(GameSprite):
  #движение врага
  def update(self):
      self.rect.y += self.speed
      global lost
      #исчезает, если дойдёт до края экрана
      if self.rect.y > win_height:
          self.rect.x = randint(80, win_width - 80)
          self.rect.y = 0
          lost = lost + 1


#класс спрайта-пули 
class Bullet(GameSprite):
  #движение врага
  def update(self):
      self.rect.y += self.speed
      #исчезает, если дойдёт до края экрана
      if self.rect.y < 0:
          self.kill()
  
#создаём окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
#создаём спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)


#создание группы спрайтов-врагов
monsters = sprite.Group()
for i in range(1, 6):
  monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
  monsters.add(monster)


#создание группы спрайтов-астероидов ()
asteroids = sprite.Group()
for i in range(1, 3):
   asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
   asteroids.add(asteroid)

bullets = sprite.Group()


finish = False
#основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна


rel_time = False #флаг, отвечающий за перезарядку


num_fire = 0  #переменная для подсчёта выстрелов
while run:
   #событие нажатия на кнопку “Закрыть”
   for e in event.get():
       if e.type == QUIT:
           run = False
