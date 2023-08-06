import numpy as np

__all__ = [
  'eval_on_grid',
  'get_background',
  'animate'
]

def eval_on_grid(f, range_x, range_y, steps=128):
  (min_x, max_x), (min_y, max_y) = range_x, range_y

  xs = np.linspace(min_x, max_x, num=steps)
  ys = np.linspace(min_y, max_y, num=steps)

  X_grid, Y_grid = np.meshgrid(xs, ys)
  XY_grid = np.stack([X_grid.ravel(), Y_grid.ravel()], axis=1)

  return xs, ys, np.array(f(XY_grid)).reshape((xs.shape[0], ys.shape[0]))

def get_background(xs, ys, F, optimal=None, levels=20, figsize=(9, 9)):
  import matplotlib.pyplot as plt

  fig = plt.figure(figsize=figsize)

  f_min, f_max = np.min(F), np.max(F)
  levels = np.linspace(f_min, f_max, num=levels + 2)[1:-1]

  plt.contour(xs, ys, F, levels=levels, colors='black', zorder=0)

  if optimal is not None:
    opt_x, opt_y = optimal
    plt.scatter(opt_x, opt_y, marker='*', s=200, color='red', zorder=2)

  plt.xlim([xs[0], xs[-1]])
  plt.ylim([ys[0], ys[-1]])

  plt.axis('off')
  fig.tight_layout(pad=0)

  fig.canvas.draw()

  data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
  data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

  plt.close(fig)

  return data

def point_cloud_stream(samples, range_x, range_y, background, progress=lambda x: x):
  x_min, x_max = range_x
  y_min, y_max = range_y

  image = np.zeros_like(background)

  for i in progress(range(samples.shape[0])):
    image[:] = background

    for j in range(samples.shape[1]):
      x, y = samples[i, j]
      pixel_y = int((x - x_min) / (x_max - x_min) * background.shape[1])
      pixel_x = background.shape[0] - int((y - y_min) / (y_max - y_min) * background.shape[0])

      image[pixel_x - 2: pixel_x + 2, pixel_y - 2: pixel_y + 2] = (0, 0, 255)

    yield image.tobytes()

def trajectory_stream(samples, range_x, range_y, background, colors=None, progress=lambda x: x):
  from PIL import Image, ImageDraw

  range_min = np.array([range_x[0], range_y[0]])
  range_max = np.array([range_x[1], range_y[1]])

  image = Image.fromarray(background)
  draw = ImageDraw.Draw(image)

  coordinates = (samples - range_min[None, :]) / (range_max - range_min)[None, :]
  coordinates = coordinates * np.array(background.shape[:2])[None, :]
  coordinates = coordinates.astype('int32')

  if colors is None:
    colors = [(0, 0, 255) for _ in range(samples.shape[1])]

  for i in progress(range(samples.shape[0])):
    if i == 0:
      continue

    for j in range(samples.shape[1]):
      x0, y0 = coordinates[i - 1, j]
      x1, y1 = coordinates[i, j]

      draw.line((x0, background.shape[1] - y0, x1, background.shape[1] - y1), fill=colors[j], width=2)

    yield image.tobytes()

def animate(samples, range_x, range_y, background, filename, trajectory=False, colors=None, frames_per_second=32, progress=lambda x: x):
  import ffmpeg

  width = background.shape[1]
  height = background.shape[0]

  ff = ffmpeg.input(
    'pipe:', format='rawvideo', pix_fmt='rgb24',
    s='{}x{}'.format(width, height),
    r='%d' % (frames_per_second, )
  ).output(
    filename, pix_fmt='yuv420p', f='mp4'
  ).overwrite_output().run_async(
    pipe_stdin=True, quiet=True
  )

  if trajectory:
    for frame in trajectory_stream(samples, range_x, range_y, background, colors=colors, progress=progress):
      ff.stdin.write(frame)
  else:
    for frame in point_cloud_stream(samples, range_x, range_y, background, progress=progress):
      ff.stdin.write(frame)

  ff.stdin.close()
  ff.wait()

  return filename







