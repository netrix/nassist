__author__ = 'Netrix'

import platform
import PyQt5.QtCore as qtcore

if platform.system() == "Linux":
    # requires python-xlib
    from Xlib.display import Display
    from Xlib import X
    from Xlib.XK import string_to_keysym

    class HotkeyThread(qtcore.QThread):
        hotkeySignal = qtcore.pyqtSignal()

        def __init__(self, mod = 'MOD_SHIFT', key = 'VK_SPACE'):
            qtcore.QThread.__init__(self)

            keysym = string_to_keysym('space')
            self.modifiers = X.ShiftMask | X.ControlMask

            self.disp = Display()
            self.key = self.disp.keysym_to_keycode(keysym)

            self.root = self.disp.screen().root
            self.root.change_attributes(event_mask=X.KeyPressMask)
            self.root.grab_key(self.key, self.modifiers, 0, False, X.GrabModeAsync, X.GrabModeAsync)
            self.root.grab_key(self.key, self.modifiers | X.LockMask, 0, False, X.GrabModeAsync, X.GrabModeAsync)
            self.root.grab_key(self.key, self.modifiers | X.Mod2Mask, 0, False, X.GrabModeAsync, X.GrabModeAsync)
            self.root.grab_key(self.key, self.modifiers | X.LockMask | X.Mod2Mask, 0, False, X.GrabModeAsync, X.GrabModeAsync)
            self.root.grab_key(self.key, self.modifiers | X.Mod3Mask | X.LockMask, 0, False, X.GrabModeAsync, X.GrabModeAsync)
            self.root.grab_key(self.key, self.modifiers | X.Mod3Mask | X.Mod2Mask, 0, False, X.GrabModeAsync, X.GrabModeAsync)
            self.root.grab_key(self.key, self.modifiers | X.Mod3Mask | X.LockMask | X.Mod2Mask, 0, False, X.GrabModeAsync, X.GrabModeAsync)

        def dispatch_hotkey(self, msg):
            if msg.type == X.KeyPress:
                self.hotkeySignal.emit()

        def __del__(self):
            self.terminate()

        def run(self):
            while True:
                event = self.root.display.next_event()
                self.dispatch_hotkey(event)

            print('finished loop')

elif platform.system() == "Windows":
    #requires pywin
    import win32con
    import ctypes, ctypes.wintypes

    class HotkeyThread(qtcore.QThread):

        hotkeySignal = qtcore.pyqtSignal()

        def __init__(self, mod = 'MOD_SHIFT', key = 'VK_SPACE'):
            qtcore.QThread.__init__(self)
            self.registered = False

            mods = {}
            keys = {}
            for item in dir(win32con):
                if item.startswith("MOD_"):
                    exec("mods[item] = win32con." + item)
                    exec("mods[win32con." + item + "] = '" + item + "'")
                if item.startswith("VK_"):
                    exec("keys[item] = win32con." + item)
                    exec("keys[win32con." + item + "] = '" + item + "'")

            self.key = keys[key]
            self.mod = mods[mod] + mods['MOD_CONTROL']
            print(self.mod)

        def dispatch_hotkey(self, msg):
            self.hotkeySignal.emit()

        def __del__(self):
            if self.registered:
                ctypes.windll.user32.UnregisterHotKey(None, 1)
            self.terminate()

        def run(self):
            try:
                ctypes.windll.user32.RegisterHotKey(None, 1, self.mod, self.key)
                self.registered = True

                msg = ctypes.wintypes.MSG()
                while ctypes.windll.user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
                    if msg.message == win32con.WM_HOTKEY:
                        self.dispatch_hotkey(msg)
                    else:
                        ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
                        ctypes.windll.user32.DispatchMessageA(ctypes.byref(msg))

            # Unregister hotkey
            finally:
                ctypes.windll.user32.UnregisterHotKey(None, 1)
                self.registered = False
else:
    raise "Not implemented"
