import pygame,sys
import random
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        flap_1 = pygame.transform.scale2x(pygame.image.load('image/flap_1.png').convert_alpha())
        flap_2 = pygame.transform.scale2x(pygame.image.load('image/flap_2.png').convert_alpha())
        flap_3 = pygame.transform.scale2x(pygame.image.load('image/flap_3.png').convert_alpha())
        self.flap = [flap_1,flap_2,flap_3]
        self.index = 0
        self.image = self.flap[self.index]
        self.rect = self.image.get_rect(center = (100,512))
        self.gravity = 0
        self.movement = 0
    def input(self,true):
        if true :
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                if self.gravity >=-10 and self.rect.top >1 :
                    flap_sound.play()
                self.gravity = -12
    def add_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >950:
            self.rect.bottom = 950
            self.gravity -=1
        if self.rect.top < 0 :
            self.rect.top  = 0
            self.gravity = 0
    def animation(self):
        if self.gravity <=0:
            self.image = self.flap[2]
        else:
            self.index +=0.1
            if self.index >= 2:
                self.index = 0
        self.image = pygame.transform.rotozoom(self.flap[int(self.index)],-self.gravity*2,1)
    def update(self,true):
        self.input(true)
        self.add_gravity()
        self.animation()

class Pipe(pygame.sprite.Sprite):
    def __init__(self,direction,pos_x,pos_y):
        super().__init__()
        pipe = pygame.transform.scale2x(pygame.image.load('image/pipe.png').convert_alpha())
        if direction =='down':
            self.pipe_in = pipe
            self.image = self.pipe_in
            self.rect = pipe.get_rect(midtop = (pos_x,pos_y))
        else:
            pipe = pygame.transform.flip(pipe,False,True)
            self.pipe_in = pipe
            self.image = self.pipe_in
            self.rect = pipe.get_rect(midbottom = (pos_x,pos_y))
    def animation(self):
        self.image = self.pipe_in
    def destroy(self):
        if self.rect.x <= - 100 :
            self.kill()
    def inc_score(self):
        global score, can_inc

        if (10 < self.rect.x <=50) and (can_inc):
            score +=1
            can_inc = False
            point_sound.play()
        if self.rect.x <0:
            can_inc = True
    def update(self):
        self.rect.x -= 5
        self.animation()
        self.destroy()
        self.inc_score()
   
def collistions():
    if pygame.sprite.spritecollide(bird.sprite,pipe_,False):
        death_sound.play()
        return False
    return True   
def display_score():
    font_game = pygame.font.Font('font/04B_19.TTF', 70)
    text = font_game.render(str(int(score)),True,(255,255,255))
    text_rect = text.get_rect(center = (288,100))
    screen.blit(text,text_rect)
def high_score():
    global high_scores
    if high_scores < score :
        high_scores = score
    font_game = pygame.font.Font('font/04B_19.TTF', 20)
    text = font_game.render(f'High Score: {high_scores}',True,(255,255,255))
    text_rect = text.get_rect(center = (480,10))
    screen.blit(text,text_rect)
  
pygame.init()
screen = pygame.display.set_mode((576,1024))
clock = pygame.time.Clock()
pygame.display.set_caption('Flappy Bird')
#backgroud
bg = pygame.image.load('image/bg.png').convert()
bg = pygame.transform.scale2x(bg)
base = pygame.transform.scale2x(pygame.image.load('image/base.png').convert())
base_pos_x = 0
#gameoverMess
gameover = pygame.transform.scale2x(pygame.image.load('image/gameover.png'))
gameover_rect = gameover.get_rect(center = (288,300))
lap =0
#messfirst
mess = pygame.image.load('image/message.png').convert_alpha()
mess = pygame.transform.scale2x(mess)
mess_rect = mess.get_rect(center = (288,512))
#obj
bird = pygame.sprite.GroupSingle()
pipe_ = pygame.sprite.Group()
bird.add(Bird())
#onstart
game_true = False
score  = 0
high_scores = 0
can_inc = True
game_nonstart = True
#sound
flap_sound  = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
point_sound = pygame.mixer.Sound('sound/sfx_point.wav')
#spam_pipe
SPAM = pygame.USEREVENT + 1
pygame.time.set_timer(SPAM , 1200 )
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_true:
            if event.type == SPAM:
                pos_x = random.randint(600,700)
                pos_y = random.randint(400,800)
                pipe_.add(Pipe('down',pos_x,pos_y))
                pipe_.add(Pipe('top',pos_x,pos_y-300))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and lap <=0:
                #ResetGame
                gameover_gravity = 1
                gameover_rect.y = 300
                inc_g = 1
                lap = 3
                game_true = True
                game_nonstart = False
                can_inc = True
                bird.remove()
                pipe_.empty()
                bird.add(Bird())
                score = 0
    #MAIN_GAME
    screen.blit(bg,(0,0))
    if game_nonstart:
        bird.draw(screen)
        screen.blit(mess,mess_rect)

    elif game_true:
        #bird
        bird.draw(screen)
        bird.update(True)
        #pipe
        pipe_.draw(screen)
        pipe_.update()
        #game_true
        game_true = collistions()
        display_score()
        high_score()
    else:
        bird.draw(screen)
        bird.update(False)
        pipe_.draw(screen)
        gameover_gravity+= inc_g
        gameover_rect.y += gameover_gravity
        if gameover_rect.y>=500 and lap>0:
            gameover_gravity = - gameover_gravity+2
            lap -= 1
        elif gameover_rect.y>=500:
            gameover_gravity = 0
            inc_g = 0
        screen.blit(gameover,gameover_rect)
        high_score()
    if game_true:
        base_pos_x -=5
    if base_pos_x <= -576:
        base_pos_x = 0
    screen.blit(base,(base_pos_x,950))
    screen.blit(base,(base_pos_x+576,950))
    pygame.display.update()
    clock.tick(60)