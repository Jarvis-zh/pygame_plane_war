#-*- coding: utf-8 -*-
__metatype__ = type
import pygame #导入pygame库
import random
from sys import exit #向sys模块借一个exit函数用来退出程序

#定义一个Bullet类，封装子弹相关的数据和方法
class Bullet:
	def __init__(self):
		#初始化成员变量 x, y, image
		self.x = 0
		self.y = -1
		self.image = pygame.image.load('bullet.png').convert_alpha()
		#默认不激活
		self.active = False

	def move(self):
		#处理子弹运动
		if self.active:
			self.y -=3
			
		if self.y < 0:
			self.active = False

	def restart(self):
		#重置子弹位置
		mouseX, mouseY = pygame.mouse.get_pos()
		self.x = mouseX - self.image.get_width() / 2
		self.y = mouseY - self.image.get_height() / 2
		#激活子弹
		self.active = True

class Enemy:
	def restart(self):
		#重置敌机位置和速度
		self.x = random.randint(50, 400)
		self.y = random.randint(-200, -50)
		self.speed = random.random() + 0.1

	def __init__(self):
		#初始化
		self.restart()
		self.image = pygame.image.load('enemy_plane.jpg').convert_alpha()

	def move(self):
		if self.y < 800:
			#向下移动
			self.y += self.speed
		else:
			#重置
			self.restart()


class Plane:
	def restart(self):
		self.x = 200
		self.y = 600

	def __init__(self):
		self.restart()
		self.image = pygame.image.load('plane1.jpg').convert_alpha()

	def move(self):
		x, y = pygame.mouse.get_pos()
		x -= self.image.get_width() / 2
		y -= self.image.get_height() / 2
		self.x = x
		self.y = y


#判断是否命中目标
def checkHit(enemy, bullet):
	if (bullet.x > enemy.x \
		and bullet.x < enemy.x + enemy.image.get_width() \
		and bullet.y > enemy.y \
		and bullet.y < enemy.y + enemy.image.get_height()):
		enemy.restart()
		bullet.active = False
		return True
	return False

#判断我方战机是否壮烈牺牲
def checkCrash(enemy, plane):
	'''
	这里的判断比之前要复杂一些，因为敌机和本体都有一定的面积，
	不能像子弹一样忽略长宽。但如果两张图片一旦有重合就算是碰撞，
	会让游戏看上去有些奇怪：有时候你觉得并没有撞上，而实际已经
	有了重合，游戏就失败了。所以为了避免这一现象，我们要给plane
	的长宽打上一点折扣。这也就是代码中判断条件里“0.3”“0.7”的意
	义所在。
	'''
	if (plane.x + 0.7*plane.image.get_width() > enemy.x \
		and plane.x + 0.3*plane.image.get_width() < enemy.x + enemy.image.get_width() \
		and plane.y + 0.7*plane.image.get_height() > enemy.y \
		and plane.y + 0.3*plane.image.get_height() < enemy.y + enemy.image.get_height()):
		return True
	return False



pygame.init() #初始化pygame,为使用硬件做准备

#创建了一个窗口,窗口大小和背景图片大小一样
screen = pygame.display.set_mode((450,800), 0, 32)
#设置窗口标题
pygame.display.set_caption('飞机大战')
#加载并转换图像
background = pygame.image.load('bg4.jpg').convert()

#创建多个子弹
bullets = []
for i in range(5):
	bullets.append(Bullet())
count_b = len(bullets)#子弹总数
index_b = 0 #即将发射的子弹序号
interval_b = 0 #发射子弹的间隔


#创建多个敌机
enemies = []
for i in range(5):
	enemies.append(Enemy())

#创建我方战机
plane = Plane()

#创建显示分数的字体
font = pygame.font.Font(None, 32)

score = 0
gameover = False
#游戏主循环
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			#接收到退出事件后退出程序
			pygame.quit()
			exit()
		if gameover and event.type == pygame.MOUSEBUTTONUP:
			#重置游戏
			plane.restart()
			for enemy in enemies:
				enemy.restart()
			for bullet in bullets:
				bullet.restart()
			score = 0
			gameover = False

	#将背景图画上去
	screen.blit(background, (0,0))

	
	if not gameover:
		#子弹
		interval_b -= 1
		if interval_b < 0:
			bullets[index_b].restart()
			interval_b = 100
			index_b = (index_b + 1) % count_b

		for bullet in bullets:
			if bullet.active:
				#判断是否击中敌机
				for enemy in enemies:
					if checkHit(enemy, bullet):
						score += 100 #命中敌机分数加100
				bullet.move()
				screen.blit(bullet.image, (bullet.x, bullet.y))
		#敌机		
		for enemy in enemies:
			if checkCrash(enemy, plane):
				gameover = True
			enemy.move()
			screen.blit(enemy.image, (enemy.x, enemy.y))

		#战机
		plane.move()
		screen.blit(plane.image, (plane.x, plane.y))

		text = font.render('Score:%d' %score, 1, (0, 0, 0))
		screen.blit(text, (0, 0))#左上角显示分数
	else:
		text = font.render('Score:%d' %score, 1, (0, 0, 0))
		screen.blit(text, (190, 400))#显示在屏幕中间
		#pygame.quit()
		#exit()

	#刷新一下画面
	pygame.display.update()
