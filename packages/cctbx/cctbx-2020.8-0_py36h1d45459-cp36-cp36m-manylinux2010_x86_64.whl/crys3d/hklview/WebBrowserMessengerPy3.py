from __future__ import absolute_import, division, print_function
import traceback
from libtbx.utils import Sorry, to_str
import threading, sys
import os.path, time

import asyncio
import websockets
from typing import Optional
from websockets.exceptions import (
  ConnectionClosed,
  ConnectionClosedError,
  ConnectionClosedOK,
)

class MyWebSocketServerProtocol(websockets.server.WebSocketServerProtocol):
  def __init__(self, *args, **kwargs):
    self.client_connected = None
    self.onconnect = None
    self.ondisconnect = None
    self.onlostconnect = None
    super().__init__(*args, max_size=100000000) # allow for saving 100Mb size images
  def connection_open(self) -> None:
    #print("In connection_open()")
    self.client_connected = self.local_address
    if self.onconnect:
      self.onconnect(self.client_connected)
    super().connection_open()
  def connection_lost(self, exc: Optional[Exception]) -> None:
    #print("In connection_lost()")
    self.client_connected = None
    if self.onlostconnect and hasattr(self, "close_code"):
      self.onlostconnect(self.client_connected, self.close_code, self.close_reason)
    super().connection_lost(exc)
  def connection_closed_exc(self) -> ConnectionClosed:
    #print("In connection_closed_exc()")
    self.client_connected = None
    if self.ondisconnect:
      self.ondisconnect(self.client_connected, self.close_code, self.close_reason)
    super().connection_closed_exc()


class WBmessenger(object):
  def __init__(self, viewerparent ):
    self.parent = viewerparent
    self.ProcessMessage = self.parent.ProcessMessage
    self.websockport = self.parent.websockport
    self.sleeptime = self.parent.sleeptime
    self.mprint = self.parent.mprint
    self.parent.lastviewmtrx
    self.browserisopen = False
    self.msgqueue = []
    self.msgdelim = ":\n"
    self.ishandling = False
    self.websockclient = None
    self.isterminating = False
    self.was_disconnected = None
    self.mywebsock = None
    self.websockeventloop = None


  def Sleep(self, t):
    async def asyncsleep(t):
      await asyncio.sleep(t) # time for browser to clean up

    if sys.version_info[0] > 2:
      if threading.current_thread().name == "zmq_thread":
        asyncio.run( asyncsleep(t) )
      else: # is main thread
        time.sleep(t)
    else:
      time.sleep(t)


  def StartWebsocket(self):
    try:
      if self.websockeventloop is not None:
        self.mprint("websockeventloop already running", verbose=1)
        return
      if self.websockeventloop is None:
        self.websockeventloop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.websockeventloop)
        if self.parent.debug is not None:
          self.parent.websockeventloop.set_debug(True)
      self.server = websockets.serve(self.WebSockHandler, '127.0.0.1',
                                      self.websockport,
                                      create_protocol=MyWebSocketServerProtocol
                                      )
      self.websockeventloop.run_until_complete(self.server)
      self.mprint("starting WebSockHandler on port %s" %str(self.websockport), verbose=1)
      # run_forever() blocks execution so put in a separate thread
      self.wst = threading.Thread(target=self.websockeventloop.run_forever)
      self.wst.daemon = True
      self.wst.start()
      if not self.server:
        raise Sorry("Could not connect to web browser")
    except Exception as e:
      self.mprint( to_str(e) + "\n" + traceback.format_exc(limit=10), verbose=0)


  def StopWebsocket(self):
    self.isterminating = True
    self.javascriptcleaned = True
    self.mprint("Shutting down websockeventloop", verbose=1)
    self.websockeventloop.stop()



  async def ReceiveMessage(self):
    while True:
      await asyncio.sleep(self.sleeptime)
      if self.was_disconnected in [4242, # reload
                                    4241, # javascriptcleanup
                                    1006, # WebSocketServerProtocol.close_code is absent
                                    1001, # normal exit
                                    1005,
                                    1000
                                    ]:
        return # shutdown
      if self.parent.viewerparams.scene_id is None or self.parent.miller_array is None \
          or self.websockclient is None or self.mywebsock.client_connected is None:
        await asyncio.sleep(self.sleeptime)
        continue
      message = ""
      try: # use EAFP rather than LBYL style with websockets
        message = await self.mywebsock.recv()
      except Exception as e:
        if self.was_disconnected != 4242:
          self.mprint( to_str(e) + "\n" + traceback.format_exc(limit=10), verbose=1)
        continue
      await self.OnWebsocketClientMessage(None, None, message)


  async def OnWebsocketClientMessage(self, client, server, message):
    self.ProcessMessage(message)


  def AddToBrowserMsgQueue(self, msgtype, msg=""):
    self.msgqueue.append( (msgtype, msg) )


  async def WebSockHandler(self, mywebsock, path):
    self.mprint("Entering WebSockHandler", verbose=1)
    #if self.was_disconnected == 1006:
    #  await mywebsock.close()
    if hasattr(self.mywebsock, "state") and self.mywebsock.state == 2 and self.websockclient is not None:
      await self.mywebsock.wait_closed()

    if self.websockclient is not None or self.ishandling:
      #self.was_disconnected = 1006
      #await mywebsock.wait_closed()
      await asyncio.sleep(0.5)
      return
    self.ishandling = True
    mywebsock.onconnect = self.OnConnectWebsocketClient
    self.OnConnectWebsocketClient(mywebsock.client_connected)
    mywebsock.ondisconnect = self.OnDisconnectWebsocketClient
    mywebsock.onlostconnect = self.OnLostConnectWebsocketClient
    self.mywebsock = mywebsock
    getmsgtask = asyncio.ensure_future(self.ReceiveMessage())
    sendmsgtask = asyncio.ensure_future(self.WebBrowserMsgQueue())
    await getmsgtask
    await sendmsgtask
    self.mprint("Exiting WebSockHandler", verbose=1)
    self.ishandling = False


  async def WebBrowserMsgQueue(self):
    while True:
      try:
        nwait = 0.0
        await asyncio.sleep(self.sleeptime)
        if self.was_disconnected in [4242, # reload
                                      4241, # javascriptcleanup
                                      1006, # WebSocketServerProtocol.close_code is absent
                                      1001, # normal exit
                                      1005,
                                      1000
                                      ]:
          return # shutdown
        if self.parent.javascriptcleaned or self.was_disconnected == 4241: # or self.was_disconnected == 1001:
          self.mprint("Shutting down WebBrowser message queue", verbose=1)
          return
        if len(self.msgqueue):
          pendingmessagetype, pendingmessage = self.msgqueue[0]
          gotsent = await self.send_msg_to_browser(pendingmessagetype, pendingmessage)
          while not self.browserisopen:  #self.websockclient:
            await asyncio.sleep(self.sleeptime)
            nwait += self.sleeptime
            if nwait > self.parent.handshakewait or self.parent.javascriptcleaned or not self.parent.viewerparams.scene_id is not None:
              continue
          if gotsent:
            self.msgqueue.remove( self.msgqueue[0] )
      except Exception as e:
        self.mprint( str(e) + traceback.format_exc(limit=10), verbose=0)


  def OnConnectWebsocketClient(self, client):
    self.websockclient = client
    self.mprint( "Browser connected " + str( self.websockclient ), verbose=1 )
    self.was_disconnected = None
    if self.parent.lastviewmtrx and self.parent.viewerparams.scene_id is not None:
      self.parent.set_volatile_params()
      self.mprint( "Reorienting client after refresh:" + str( self.websockclient ), verbose=2 )
      self.AddToBrowserMsgQueue("ReOrient", self.parent.lastviewmtrx)
    else:
      self.parent.SetAutoView()


  def OnLostConnectWebsocketClient(self, client, close_code, close_reason):
    msg =  "Browser lost connection %s, code %d, reason: %s" %(str(self.websockclient), close_code, close_reason)
    self.mprint(msg , verbose=1 )
    self.was_disconnected = close_code
    self.websockclient = None
    self.ishandling = False


  def OnDisconnectWebsocketClient(self, client, close_code, close_reason):
    msg =  "Browser disconnected %s, code %d, reason: %s" %(str(self.websockclient), close_code, close_reason)
    self.mprint(msg , verbose=1 )
    self.was_disconnected = close_code
    self.websockclient = None
    self.ishandling = False


  async def send_msg_to_browser(self, msgtype, msg=""):
    message = u"" + msgtype + self.msgdelim + str(msg)
    nwait = 0.0
    while isinstance(self.parent.lastmsg, str) and \
      not ("Ready" in self.parent.lastmsg or "tooltip_id" in self.parent.lastmsg \
      or "CurrentViewOrientation" in self.parent.lastmsg or "AutoViewSet" in self.parent.lastmsg \
      or "ReOrient" in self.parent.lastmsg) or self.websockclient is None:
      await asyncio.sleep(self.sleeptime)
      nwait += self.sleeptime
      if self.was_disconnected != None:
        return False
      if nwait > 2.0 and self.browserisopen:
        self.mprint("ERROR: No handshake from browser!", verbose=0 )
        self.mprint("failed sending " + msgtype, verbose=1)
        self.was_disconnected = 1005
        #break
        return False
    if self.browserisopen and self.websockclient is not None or self.mywebsock.client_connected is not None:
      try: # use EAFP rather than LBYL style with websockets
        await self.mywebsock.send( message )
        return True
      except Exception as e:
        if self.was_disconnected != 4242:
          self.mprint( str(e) + "\n" + traceback.format_exc(limit=10), verbose=1)
        self.websockclient = None
        return False
    else:
      return self.parent.OpenBrowser()
    #return False
