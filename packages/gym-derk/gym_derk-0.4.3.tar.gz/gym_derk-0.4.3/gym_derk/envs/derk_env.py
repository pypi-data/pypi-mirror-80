import gym
import asyncio
import os
from typing import List, Dict, Tuple
import sys
import http.server
import socketserver
import urllib
import posixpath
import threading
import json

# This is a copy of the pyppeteer function in pyppeteer/chromium_downloader,
# but since we're trying to update the environment variables which are read in that file
# we can't import it
def pyppeteer_current_platform() -> str:
    if sys.platform.startswith('linux'):
        return 'linux'
    elif sys.platform.startswith('darwin'):
        return 'mac'
    elif (sys.platform.startswith('win') or
          sys.platform.startswith('msys') or
          sys.platform.startswith('cyg')):
        if sys.maxsize > 2 ** 31 - 1:
            return 'win64'
        return 'win32'
    raise OSError('Unsupported platform: ' + sys.platform)

if not ('PYPPETEER_CHROMIUM_REVISION' in os.environ):
  plt = pyppeteer_current_platform()
  if plt == 'win32':
    os.environ['PYPPETEER_CHROMIUM_REVISION'] = '798057'
  elif plt == 'win64':
    os.environ['PYPPETEER_CHROMIUM_REVISION'] = '803555'
  elif plt == 'linux':
    os.environ['PYPPETEER_CHROMIUM_REVISION'] = '798580'
  elif plt == 'mac':
    os.environ['PYPPETEER_CHROMIUM_REVISION'] = '798027'
if not ('PYPPETEER_DOWNLOAD_HOST' in os.environ):
  os.environ['PYPPETEER_DOWNLOAD_HOST'] = 'http://storage.googleapis.com'
import pyppeteer
import numpy as np
from random import random
import webbrowser
import base64
import logging

logger = logging.getLogger(__name__)

app_build_path = os.path.abspath(os.path.expanduser(__file__ + '/../../app_build'))
app_build_index_html = os.path.join(app_build_path, 'index.html')

class AppBuildRequestHandler(http.server.SimpleHTTPRequestHandler):
  def translate_path(self, path):
      path = path.split('?',1)[0]
      path = path.split('#',1)[0]
      if path == '/':
        path = '/index.html'
      return app_build_path + '/' + path


class EnvServer(http.server.HTTPServer):
  def __init__(self, *args, **kwargs):
    http.server.HTTPServer.__init__(self, *args, **kwargs)
    self.last_request_path = ''
    self.last_request_data = None
    self.next_response_data = ''

class EnvServerRequestHandler(http.server.BaseHTTPRequestHandler):
  def _set_response(self):
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()

  def do_GET(self):
    self.server.last_request_path = self.path
    logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
    self._set_response()
    self.wfile.write(self.server.next_response_data.encode('utf-8'))

  def do_POST(self):
    self.server.last_request_path = self.path
    content_length = int(self.headers['Content-Length'])
    self.server.last_request_data = self.rfile.read(content_length)
    self._set_response()
    self.wfile.write(self.server.next_response_data.encode('utf-8'))


class BattleConnectionError(Exception):
  def __init__(self):
    pass

class EpisodeResetError(Exception):
  def __init__(self):
    pass

class DerkEnv(gym.Env):
  """Reinforcement Learning environment for "Dr. Derk's Mutant Battlegrounds"

  The environment can be run in one of two modes: 'train' or 'battle'. In 'train'
  you control both the home and away team. In 'battle' you are matched against
  an opponent on the internet, to see how well your agent performs compared to
  that agent.

  Args:
    server_port: Start the environment in server mode. This can the be connect to from other environments. (Environment variable: DERK_SERVER_PORT)
    opponent_host: Connect to an environment started with server_port
    app_host: Configure an alternative app bundle host. (Environment variable: DERK_APP_HOST)
    home_team: Home team creatures
    away_team: Away team creatures
    reward_function: Reward function. See :ref:`reward-function` for available options
    dummy_mode: Don't actually run the game, but just return random outputs
    n_arenas: Number of parallel arenas to run
    substeps: Number of game steps to run for each call to step
    turbo_mode: Skip rendering to the screen to run as fast as possible. (Environment variable: DERK_TURBO_MODE)
    interleaved: Run each step in the background, returning the previous steps observations
    headless: Run in headless mode
    chrome_executable: Path to chrome or chromium. (Environment variable: DERK_CHROME_EXECUTABLE)
    chrome_args: List of command line switches passed to chrome
    browser: A pyppeteer browser instance
    browser_logs: Show log output from browser
    safe_reset: A safer but slower version of reset. Use this if you get CONTEXT_LOST errors. (Environment variable: DERK_SAFE_RESET)
    no_init_browser: You need to run env.async_init_browser() manually to launch the browser if this is set to true

  With the interleaved mode on, there's a delay between observation and action of size substeps.
  E.g. if substeps=8 there's an 8*16ms = 128ms "reaction time" from observation to action. This means
  that the game and the python code can in effect run in parallel. This is always enabled in battles.

  Attributes:
    n_arenas: Number of arenas
    n_agents_per_arena: Number of agents per arena

  """
  def __init__(self,
      server_port: int=None, opponent_host: str=None,
      app_host: str=None,
      home_team: List[Dict] = None, away_team: List[Dict] = None, reward_function: Dict=None,
      dummy_mode: bool=False, n_arenas: int=1, substeps: int=8, turbo_mode: bool=False,
      interleaved: bool=True,
      headless: bool=False, chrome_executable: str=None, chrome_args: List[str]=[], browser: pyppeteer.browser.Browser=None,
      safe_reset: bool=None, no_init_browser: bool=False, browser_logs: bool=False,
      debug_no_observations: bool=False, internal_http_server: bool = False):

    self.server_port = server_port if server_port is not None else os.environ.get('DERK_SERVER_PORT', None)
    self.opponent_host = opponent_host
    self.app_host = app_host if app_host is not None else os.environ.get('DERK_APP_HOST', ('file://' + app_build_index_html))
    self.home_team = home_team
    self.away_team = away_team
    self.reward_function = reward_function
    self.dummy_mode = dummy_mode
    self.n_arenas = n_arenas
    self.substeps = substeps
    self.turbo_mode = turbo_mode if turbo_mode is not None else (os.environ.get('DERK_TURBO_MODE', 'False').lower() == 'true')
    self.interleaved = interleaved
    self.headless = headless
    self.chrome_executable = chrome_executable if chrome_executable is not None else os.environ.get('DERK_CHROME_EXECUTABLE', None)
    self.chrome_args = chrome_args
    self.browser = browser
    self.browser_logs = browser_logs
    self.safe_reset = safe_reset if safe_reset is not None else (os.environ.get('DERK_SAFE_RESET', 'False').lower() == 'true')
    self.debug_no_observations = debug_no_observations
    self.internal_http_server = internal_http_server

    if self.internal_http_server:
      self.bundle_server = socketserver.TCPServer(('', 0), AppBuildRequestHandler)
      threading.Thread(target=self.bundle_server.serve_forever, daemon=True).start()
      self.app_host = 'http://localhost:' + str(self.bundle_server.server_address[1])

    self.env_server = None
    if self.server_port:
      self.env_server = EnvServer(('', self.server_port), EnvServerRequestHandler)
      self.server_port = self.env_server.server_address[1]
      print('Serving on http://localhost:' + str(self.server_port))

    self.n_agents_per_arena = (6 if (self.server_port is None and self.opponent_host is None) else 3)

    self.n_senses = 64

    self.observation_space = gym.spaces.Box(low=-1, high=1, shape=[self.n_senses])
    self.action_space = gym.spaces.Tuple((
      gym.spaces.Box(low=-1, high=1, shape=[]), # MoveX
      gym.spaces.Box(low=-1, high=1, shape=[]), # Rotate
      gym.spaces.Box(low=0, high=1, shape=[]), # ChaseFocus
      gym.spaces.Discrete(4), # CastingSlot
      gym.spaces.Discrete(8), # ChangeFocus
    ))

    if (not self.dummy_mode and not no_init_browser and not self.server_port):
      asyncio.get_event_loop().run_until_complete(self.async_init_browser())

  @property
  def n_agents(self):
    """Total number of agents

    I.e. ``env.n_agents_per_arena * env.n_arenas``
    """
    return self.n_agents_per_arena * self.n_arenas

  def reset(self) -> np.ndarray:
    """Resets the state of the environment and returns an initial observation.

    Returns:
      The initial observation for each agent, with shape (n_agents, n_senses). See :ref:`senses`

    Raises:
      BattleConnectionError: If there was a connection error in battle mode
    """
    return asyncio.get_event_loop().run_until_complete(self.async_reset())

  def step(self, action_n: List[List[float]] = None) -> Tuple[np.ndarray, np.ndarray, List[bool], List[Dict]]:
    """Run one timestep.

    Accepts a list of actions, one for each agent, and returns the current state.
    Agents are layed out as follows: ``[arena1-home1, arena1-home2, .., arena1-away1, ..., arena2-home1, ...]``
    Actions can be passed as either a list of list of numbers, or a numpy array of shape (n_agents, n_actions),
    or a numpy array of shape (n_arenas, n_agents_per_arena, n_actions).

    The returned observations can be reshaped like this: ``observations.reshape((env.n_arenas, env.n_agents_per_arena, -1))``

    If you are running against another environment (server_port or opponent_host specified), then the away team
    will be omitted.

    Args:
      action_n: A list of actions (one per "creature" agent). Can also be a numpy array. See :ref:`actions`

    Returns:
      A tuple of (observation_n, reward_n, done_n, info). See :ref:`senses`.
      observation_n has shape (n_agents, n_senses)

    Raises:
      BattleConnectionError: If there was a connection error in battle mode
      EpisodeResetError: If the episode was reset while in server mode
    """
    return asyncio.get_event_loop().run_until_complete(self.async_step(action_n))

  def close(self):
    """Shut down environment
    """
    return asyncio.get_event_loop().run_until_complete(self.async_close())

  def get_total_reward(self) -> np.ndarray:
    """Total reward earned throughout the entire session for each agent
    """
    return asyncio.get_event_loop().run_until_complete(self.async_get_total_reward())

  def get_round_stats(self) -> np.ndarray:
    """Get wins, ties and losses for all arenas
    """
    return asyncio.get_event_loop().run_until_complete(self.async_get_round_stats())

  async def async_init_browser(self):
    """Creates a browser instance. This only needs to be invoked if no_init_browser was passed to the constructor"""
    logger.info('[init] Using bundle host: ' + self.app_host)
    if not self.browser:
      logger.info('[init] Creating browser')
      chromium_args = [
        '--app=' + self.app_host,
        '--allow-file-access-from-files',
        '--disable-web-security',
        '--no-sandbox',
        '--ignore-gpu-blacklist',
        '--user-data-dir=' + os.environ.get('DERK_CHROMEDATA', './chromedata')
      ] + self.chrome_args
      if (self.headless):
        chromium_args.append('--use-gl=egl')
      self.browser = await pyppeteer.launch(
        ignoreHTTPSErrors=True,
        headless=self.headless,
        executablePath=self.chrome_executable,
        args=chromium_args,
        defaultViewport=None
      )
      logger.info('[init] Creating browser ok')
    logger.info('[init] Getting page')
    self.page = (await self.browser.pages())[0]
    backend = os.environ.get('DERK_BACKEND', 'production')
    if backend is not None:
      logger.info('[init] Setting backend')
      await self.page.evaluateOnNewDocument('''(backend) => window.localStorage.setItem('backend', backend)''', backend)
    if self.browser_logs:
      logger.info('[init] Setting up logs')
      self.page.on('console', self._handle_console)
      self.page.on('error', lambda m: logger.error('[error] %s', m))
      self.page.on('pageerror', lambda m: logger.error('[pageerror] %s', m))
      self.page.on('requestfailed', lambda m: logger.error('[requestfailed] %s', m))
    logger.info('[init] Navigating to bundle host')
    await self.page.goto(self.app_host)
    logger.info('[init] Waiting for GymLoaded')
    await self.page.waitForSelector('.GymLoaded')
    logger.info('[init] Gym loaded ok')
    logger.info('[init] Getting sense count')
    self.n_senses = await self.page.evaluate('''() => window.derk.nSenses''')
    logger.info('[init] Done!')

  def _handle_console(self, m):
    if m.type == 'error':
      logger.error('[console] %s', m.text)
    elif m.type == 'warning':
      logger.warning('[console] %s', m.text)
    else:
      logger.info('[console] %s', m.text)

  async def async_reset(self):
    """Async version of :meth:`reset`"""
    logger.info('[reset] Resetting...')
    if self.dummy_mode:
      return [self.observation_space.sample() for i in range(self.n_agents)]
    if self.env_server is not None:
      if self.env_server.last_request_path != '/reset':
        self.env_server.handle_request()
      res = json.loads(self.env_server.last_request_data.decode('utf-8'))
      self.n_arenas = res['nArenas']
      return self._decode_observations(res['observations'])
    if self.safe_reset:
      logger.info('[reset] Running safe reset (reload page)')
      await self.page.reload()
      logger.info('[reset] Waiting for GymLoaded')
      await self.page.waitForSelector('.GymLoaded')
    config = {
      'home': self.home_team,
      'away': self.away_team,
      'rewardFunction': self.reward_function,
      'nArenas': self.n_arenas,
      'substeps': self.substeps,
      'turboMode': self.turbo_mode,
      'interleaved': self.interleaved,
      'debugNoObservations': self.debug_no_observations,
      'opponentHost': self.opponent_host
    }
    observations = self._unwrap_result(await self.page.evaluate('''(config) => window.derk.reset(config)''', config))
    logger.info('[reset] Reset done, decoding observations and returning')
    return self._decode_observations(observations)

  def _unwrap_result(self, res):
    if res['result'] != 'ok':
      if res['error'] == 'connection-error':
        raise BattleConnectionError()
      else:
        raise Exception(res['error'])
    else:
      return res['value']

  async def async_close(self):
    """Async version of :meth:`close`"""
    if not self.dummy_mode:
      await self.browser.close()
    if self.internal_http_server:
      self.bundle_server.shutdown()

  async def async_step(self, action_n: List[List[float]] = None):
    """Async version of :meth:`step`"""
    if action_n is not None:
      actions_arr = np.asarray(action_n, dtype='float32').reshape((self.n_agents, -1))
      actions_arr[:, 3] -= 1 # CastingSlot. -1 means no action, but gym.spaces.Discrete starts at 0
      actions_arr[:, 4] -= 1 # ChangeFocus. Same as above

      # Transpose so we get things layer by layer for WebGL
      actions_arr = actions_arr.transpose().reshape(-1)
      base64_actions = base64.b64encode(actions_arr).decode('utf-8')
    else:
      base64_actions = None
    if self.dummy_mode:
      return (
        [self.observation_space.sample() for i in range(self.n_agents)],
        [random() for i in range(self.n_agents)],
        [False for i in range(self.n_agents)],
        [{} for i in range(self.n_agents)],
      )
    if self.env_server is not None:
      self.env_server.next_response_data = base64_actions
      self.env_server.handle_request() # GET step
      if self.env_server.last_request_path == '/reset':
        raise EpisodeResetError()
      self.env_server.handle_request() # POST step
      if self.env_server.last_request_path == '/reset':
        raise EpisodeResetError()
      res = json.loads(self.env_server.last_request_data.decode('utf-8'))
    else:
      res = self._unwrap_result(await self.page.evaluate('''(actions) => window.derk.step(actions)''', base64_actions))
    return self._decode_observations(res['observations']), self._decode_reward(res['reward']), res['done'], res['info']

  async def async_get_total_reward(self):
    """Async version of :meth:`get_total_reward`"""
    reward = await self.page.evaluate('''() => window.derk.getTotalReward()''')
    return self._decode_reward(reward)

  async def async_get_round_stats(self):
    """Async version of :meth:`get_round_stats`"""
    return await self.page.evaluate('''() => window.derk.getRoundStats()''')

  def get_webgl_renderer(self) -> str:
    """Return which webgl renderer is being used by the game"""
    return asyncio.get_event_loop().run_until_complete(self.async_get_webgl_renderer())

  async def async_get_webgl_renderer(self):
    """Async version of :meth:`get_webgl_renderer`"""
    return await self.page.evaluate('''() => window.derk.getWebGLRenderer()''')

  def _decode_observations(self, observations):
    obs = np.frombuffer(base64.b64decode(observations), dtype='float32')
    # Images/textures in WebGL are layed out in layer for z, and 4 components per channel
    return obs.reshape((int(self.n_senses / 4), -1, 4)).swapaxes(0, 1).reshape((-1, self.n_senses))

  def _decode_reward(self, reward):
    return np.frombuffer(base64.b64decode(reward), dtype='float32')
