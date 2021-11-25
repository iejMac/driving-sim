import cv2

WINDOW_SIZE = (160, 320)

class Simulator:
  def __init__(self, environment_path):
    self.cap = cv2.VideoCapture(environment_path)
    self.active = self.cap.isOpened()
    if self.active:
      self.active, self.x = self.cap.read()

    sh = self.x.shape
    self.wp = [(sh[0]-WINDOW_SIZE[0])//2, (sh[1]-WINDOW_SIZE[1])//2] # window position
    self.pan_speed = 5

  def step(self, action):
    # TODO: probably add some boundaries for window
    if action == 0: # up
      self.wp[0] -= self.pan_speed
    elif action == 1: # down
      self.wp[0] += self.pan_speed
    elif action == 2: # left
      self.wp[1] -= self.pan_speed
    elif action == 3: # right
      self.wp[1] += self.pan_speed
    elif action == 32: # forward
      self.active, self.x = self.cap.read()

  def get_state(self):
    return self.x[self.wp[0]:self.wp[0]+WINDOW_SIZE[0], self.wp[1]:self.wp[1]+WINDOW_SIZE[1], :]

if __name__ == "__main__":
  env_path = "environment.mp4"
  sim = Simulator(env_path)
  cv2.namedWindow("simulator")

  while sim.active:
    state = sim.get_state()
    state = cv2.resize(state, (640, 320))
    cv2.imshow("simulator", state)
    key = cv2.waitKey(25)
    if key == ord('q'):
      break
    sim.step(key)

  sim.cap.release()
  cv2.destroyWindow("simulator")
