import pygame
import sys

from frame import Frame

class ThermalVideoPlayer:
  def __init__(self, filename, screen, video_width, video_height, tempThreshold=25, tempMax=38, humanAreaMin = 100):
    self.video_height = video_height
    self.video_width = video_width
    self.filename = filename
    self.screen = screen
    self.fps = 10  # Adjust FPS as needed
    self.frame = 0
    self.frames = []
    self.paused = False
    self.tempThreshold = tempThreshold
    self.tempMax = tempMax
    self.humanAreaMin = humanAreaMin
    self.read_frames()
    self.lenght = len(self.frames)

  def read_frames(self):
    with open(self.filename) as f:
      color_v = []
      i = 0
      for line in f:
        for temp in line.strip().split():
          color_v.append(float(temp))
        if len(color_v) % (self.video_height * self.video_width) == 0:
          self.frames.append(Frame(i, self.video_width, self.video_height, self.tempThreshold, self.tempMax, self.humanAreaMin, color_v))
          color_v = []
          i += 1
        
  def draw_frame(self, frame):
    self.screen.fill((0, 0, 0))  # Clear screen
    x, y = 0, 0
    for c_val in frame:
      pygame.draw.rect(self.screen, c_val, (x * scale, y * scale, scale, scale))
      x += 1
      if x == self.video_width:
        x = 0
        y += 1
    pygame.display.flip()

  def play(self):
    clock = pygame.time.Clock()
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          return
        if event.type == pygame.KEYDOWN:

          if event.key == pygame.K_SPACE:
            self.paused = not self.paused

          elif event.key == pygame.K_LEFT and self.paused and self.frame > 0:
            self.frame -= 1
            frame = self.frames[self.frame]
            self.draw_frame(frame.finalFrame)
            print(frame)

          elif event.key == pygame.K_RIGHT and self.paused and self.frame < len(self.frames) - 1:
            self.frame += 1
            frame = self.frames[self.frame]

            self.draw_frame(frame.finalFrame)
            print(frame)

          elif event.key == pygame.K_f and self.paused:
            print(f"Current frame: {self.frame} / {self.lenght}")
      
      if not self.paused:
        self.frame += 1
        if self.frame < len(self.frames):
          frame = self.frames[self.frame]
        else:
          self.paused = True
          continue
        self.draw_frame(frame.finalFrame)
        print(frame)
        
      clock.tick(self.fps)


# Example usage
pygame.init()
scale = 40 # Adjust scale as needed (Eg. 10 for 320x240)
screen_width = 32 * scale
screen_height = 24 * scale

if len(sys.argv) >= 2:
  filename = sys.argv[1]
else:
  filename = "Materiał/H100_F250_16HZ_Normalny3.txt"

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Thermal Video Player")

video_height = 24
video_width = 32
human_temp_min = 23
human_temp_max = 38
min_human_area = 80

video_player = ThermalVideoPlayer(filename, screen, video_width, video_height, human_temp_min, human_temp_max, min_human_area)
video_player.play()
