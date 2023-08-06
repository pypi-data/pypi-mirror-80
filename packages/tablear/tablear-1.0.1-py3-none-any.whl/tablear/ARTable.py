import cv2
import numpy as np
import os
from typing import List, Tuple, Callable, Callable, NoReturn
import threading
import json

# Virtual Types
# (h,w), np.bool
TMask = np.ndarray
# (h,w,c), np.uint8
TColorImage = np.ndarray
# (h,w), np.uint8
TGrayImage = np.ndarray
# TGrayImage or TColorImage
TAnyImage = np.ndarray
# (h,w), np.int
TIndexImage = np.ndarray
# (4,4), np.float
THomography = np.ndarray
TPiano = THomography
# (x,y)
TPoint = Tuple[int, int]
# (is_same: bool, is_parallel: bool, intersection_point: TPoint or None)
TIntersection = Tuple[bool, bool, TPoint]
# (B,G,R) between [0,255]
TBGR8Color = Tuple[int, int, int]

# A pointer handler is a void fn
# that takes in (pointer_name, x, y, w, h, button_id)
TPointerHandler = Callable[[str, int, int, int, int, int], NoReturn]


mydir = os.path.dirname(os.path.abspath(__file__))

# Constants
CHECKER_DIMS = (5,4)

def hcat(*args) -> TColorImage:
    '''
    Horizontally concats many images, converting them both to color,
    and resizing all images to the shape of the first image
    '''
    (h,w,c) = args[0].shape
    resize_as_needed = lambda im: cv2.resize(im, (w,h)) if (
        im.shape[0] != h or im.shape[1] != w) else im
    return cv2.hconcat([
        resize_as_needed(to_color(im)) for im in args
    ])

def vcat(*args) -> TColorImage:
    '''
    Vertically concats two images, converting them both to color,
    and resizing all images to the shape of the first image
    '''
    (h,w,c) = args[0].shape
    resize_as_needed = lambda im: cv2.resize(im, (w,h)) if (
        im.shape[0] != h or im.shape[1] != w) else im
    return cv2.vconcat([
        resize_as_needed(to_color(im)) for im in args
    ])

def to_color(im: TAnyImage) -> TColorImage:
    '''
    Returns a color copy of the given color or gray image
    '''
    if len(im.shape) == 3:
        # color
        return np.copy(im)
    else:
        # gray
        return cv2.cvtColor(im,cv2.COLOR_GRAY2BGR)

def to_gray(im: TAnyImage) -> TGrayImage:
    '''
    Returns a gray copy of the given color or gray image
    '''
    if len(im.shape) == 3:
        # color
        return cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    else:
        # gray
        return np.copy(im)

def mask_to_image(mask: TMask) -> TGrayImage:
    '''
    Converts a bit mask to a BW grayscale image
    '''
    return mask.astype(np.uint8) * 255

def detect_color(
        color_img: TColorImage, 
        detection_color: TBGR8Color, 
        diff_thres = 30) -> TMask:
    '''
    Detects regions of color_img within diff_thres total color difference
    from the given uint8 BGR detection color.
    '''
    h,w,c = color_img.shape
    # color to subtract, in the right shape
    solidarr = np.broadcast_to(np.array(
        detection_color,
        dtype=np.uint8).reshape((1,1,c)), (h,w,c))
    # Blur the image first, so shadows / other small details are less
    # important
    blurred = cv2.blur(color_img, (3,3))
    # Compute difference
    color_diff = np.abs(blurred.astype(np.int) - solidarr.astype(np.int))
    gray_diff = np.mean(color_diff, axis=2).astype(np.float)
    gray_diff = np.clip(gray_diff, 0, 255).astype(np.uint8)
    # Blur the difference for cleaner regions and to reduce noise
    blurred_diff = cv2.blur(gray_diff, (3,3))
    # Threshold
    color_mask = np.zeros((h,w), dtype=np.bool)
    color_mask[blurred_diff < diff_thres] = True
    # Return the mask
    return color_mask

def make_checkerboard(width, height, res = 100, fname = None):
    total_width = res * width
    total_height = res * height
    img = np.zeros((total_height, total_width), dtype=np.uint8)
    for x in range(total_width):
        for y in range(total_height):
            if ((x // res) % 2) == ((y // res) % 2):
                color = 255
            else:
                color = 0
            img[y, x] = color
    if fname is not None:
        cv2.imwrite(fname, img)
    return img

DEFAULT_UI_DIR = os.path.join(mydir, "ui")

def get_required_checkerboard():
    return make_checkerboard(CHECKER_DIMS[0] + 1, CHECKER_DIMS[1] + 1)

class UIInfo(object):
    def __init__(self, ui_name, root_dir = DEFAULT_UI_DIR):
        if os.path.isfile(ui_name):
            root_dir = os.path.dirname(ui_name)
            self.name = os.path.basename(ui_name)
        else:
            self.name = ui_name

        # Load images
        myui = to_color(cv2.imread(os.path.join(root_dir, f"{self.name}.png")))
        mask_raw = to_gray(cv2.imread(os.path.join(root_dir, f"{self.name}_mask.png")))
        render_image_fp = os.path.join(root_dir, f"{self.name}_render.png")
        if os.path.isfile(render_image_fp):
            render_image = to_color(cv2.imread(render_image_fp))
        else:
            render_image = to_color(myui)
        mask_levels = sorted(set(mask_raw.ravel()))
        mask = np.zeros(mask_raw.shape, dtype=np.int)
        for (level_ix, each_level) in enumerate(mask_levels):
            mask[mask_raw == each_level] = level_ix
        og_corners_found, og_corners = cv2.findChessboardCorners(myui, CHECKER_DIMS)
        assert og_corners_found
        self.raw_image = myui
        self.render_image = render_image
        self.mask = mask
        self.corners = og_corners
        (self.height, self.width, self.image_channels) = myui.shape
        self.mask_channels = 1
        self.n_inputs = len(mask_levels)

class UIDetector(object):
    def __init__(self, ui: UIInfo):
        self.ui = ui
        self.allow_calibration_updates = True
        self.is_calibrated = False
        self.H_feed2ui = None
        self.H_ui2feed = None

    def detect_ui_in_frame(self, frame):
        flags = (cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK +
                cv2.CALIB_CB_NORMALIZE_IMAGE)
        feed_corners_found, feed_corners = cv2.findChessboardCorners(
            frame, CHECKER_DIMS, flags)
        return feed_corners_found, feed_corners

    def calibrate(self, detection_results):
        feed_corners_found, feed_corners = detection_results
        calibration_results = None
        if feed_corners_found:
            ui_corners = self.ui.corners.reshape((-1, 2))
            feed_corners = feed_corners.reshape((-1, 2))
            assert feed_corners.shape == ui_corners.shape
            H_feed2ui, _ = cv2.findHomography(feed_corners, ui_corners)
            H_ui2feed = np.linalg.inv(H_feed2ui)
            self.H_feed2ui = H_feed2ui
            self.H_ui2feed = H_ui2feed
            self.is_calibrated = True
            return True
        else:
            # Keep old calibration
            return False

    def toggle_calibration_allowed(self):
        self.allow_calibration_updates = not self.allow_calibration_updates

    def pause(self):
        self.allow_calibration_updates = False
    def resume(self):
        self.allow_calibration_updates = True

    def reset_calibration(self):
        self.is_calibrated = False
        self.H_feed2ui = None
        self.H_ui2feed = None

    def update_calibration(self, frame):
        if self.allow_calibration_updates:
            detection_results = self.detect_ui_in_frame(frame)
            self.calibrate(detection_results)

    def unwarp_frame(self, frame):
        if not self.is_calibrated:
            return None
        unwarped = cv2.warpPerspective(
            frame, self.H_feed2ui,
            (self.ui.width, self.ui.height),
            flags=cv2.INTER_LINEAR)
        return unwarped

class UIManager(object):
    def __init__(self, ui: UIInfo):
        self.ui = ui
        self.pointers = {}

        self.on_hover_callbacks = []
        self.on_enter_callbacks = []
        self.on_exit_callbacks = []

    # Client fn's
    def on_hover(self, hover_fn: TPointerHandler):
        self.on_hover_callbacks.append(hover_fn)
        return self

    def on_enter(self, enter_fn: TPointerHandler):
        self.on_enter_callbacks.append(enter_fn)
        return self
    
    def on_exit(self, exit_fn: TPointerHandler):
        self.on_exit_callbacks.append(exit_fn)
        return self

    def draw(self):
        output = np.copy(self.ui.render_image)
        for each_pointer in self.pointers:
            pos, button = self.pointers[each_pointer]
            cv2.circle(output, pos, 4, (0, 0, 255), 3)
            cv2.putText(output, f"{each_pointer}:{button}", pos, cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255)) 
        return output   

    # Detector fn's
    def call_all_on_hover(self, args):
        if args is not None:
            for each_callback in self.on_hover_callbacks:
                each_callback(*args)

    def call_all_on_enter(self, args):
        if args is not None:
            for each_callback in self.on_enter_callbacks:
                each_callback(*args)
    
    def call_all_on_exit(self, args):
        if args is not None:
            for each_callback in self.on_exit_callbacks:
                each_callback(*args)

    def update_pointer(self, pointer_name, new_position):
        prev_button = None
        prev_position = None
        if pointer_name in self.pointers:
            (prev_position, prev_button) = self.pointers[pointer_name]
        # Now we know the prev position
        if new_position is None:
            new_button = None
        else:
            x,y = new_position
            if y >= 0 and y < self.ui.height and x >= 0 and x < self.ui.width:
                new_button = self.ui.mask[y,x]
            else:
                new_position = None
                new_button = None
        # Now we know the button

        on_enter_args = None
        on_exit_args = None
        on_hover_args = None
        # Check for on_enter / on_exit
        if new_button != prev_button:
            if new_button is not None:
                # Don't call enter when pointer is gone
                on_enter_args = (pointer_name, *new_position, self.ui.width, self.ui.height, new_button)
            if prev_button is not None:
                # Don't call exit when pointer wasn't there before
                on_exit_args = (pointer_name, *prev_position, self.ui.width, self.ui.height, prev_button)

        # Check for on_hover
        else:
            if new_position is not None:
                on_hover_args = (pointer_name, *new_position, self.ui.width, self.ui.height, new_button)
        # Update the state dictionary
        if new_position is None:
            if prev_position is not None:
                del self.pointers[pointer_name]
        else:
            self.pointers[pointer_name] = (new_position, new_button)
        
        # Call all callbacks
        self.call_all_on_enter(on_enter_args)
        self.call_all_on_hover(on_hover_args)
        self.call_all_on_exit(on_exit_args)

class ColorPointer(object):
    def __init__(self, manager: UIManager,
                 pointer_color: TBGR8Color = (54, 66, 106),
                 threshold = 20):
        self.manager = manager
        self.color = pointer_color
        self.threshold = threshold
    
    def update(self, unwarped_frame):
        if unwarped_frame is not None:
            # We can do detection
            color_mask = detect_color(unwarped_frame, self.color, self.threshold)
            # Find the lowest y (top of image)
            px = np.argwhere(color_mask)
            if len(px) > 0:
                # Just find the top pixel that's true
                (y,x) = px[np.argmin(px, axis=0)[0]]
                self.manager.update_pointer("finger", (x,y))
            else:
                self.manager.update_pointer("finger", None)
        else:
            self.manager.update_pointer("finger", None)

class ARTable(object):
    def __init__(self, ui_name, on_key, webcam_id, finger_color, finger_thres):
        self.window_name = "ARTable"
        self.webcam_id = webcam_id
        self.ui = UIInfo(ui_name)
        self.detector = UIDetector(self.ui)
        self.manager = UIManager(self.ui)
        self.finger = ColorPointer(self.manager, finger_color, finger_thres)
        self.on_key = on_key
        self.is_running = False
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.stop_event = threading.Event()

        # Bubble this up for ease-of-access
        self.on_hover = self.manager.on_hover
        self.on_enter = self.manager.on_enter
        self.on_exit = self.manager.on_exit

    def stop(self):
        self.stop_event.set()
    def _run(self):
        self.is_running = True
        is_file = type(self.webcam_id) is str and os.path.isfile(self.webcam_id)
        additional_args = (cv2.CAP_DSHOW,) if not is_file else tuple([])
        cam = cv2.VideoCapture(self.webcam_id, *additional_args)
        has_pressed = False
        while not self.stop_event.is_set():
            ret, frame = cam.read(1)
            if not ret:
                break
            self.detector.update_calibration(frame)
            unwarped = self.detector.unwarp_frame(frame)
            self.finger.update(unwarped)
            rendered = self.manager.draw()
            cv2.imshow(self.window_name, hcat(unwarped if unwarped is not None else frame, rendered))
            keys = cv2.waitKey(1) & 0xFF
            if keys in map(ord,'qc'):
                if not has_pressed:
                    has_pressed = True
                    if keys == ord('c'):
                        self.detector.toggle_calibration_allowed()
                    if keys == ord('q'):
                        break
            else:
                has_pressed = False
                if self.on_key is not None:
                    self.on_key(keys)
        cam.release()
        cv2.destroyAllWindows()
        self.is_running = False
    def start_sync(self):
        self.thread.run()
    def start_threaded(self):
        self.stop_event.clear()
        self.thread.start()
        return self.stop_event

class MouseTable(object):
    def __init__(self, ui_name, on_key, *args, **kwargs):
        # Substitutes ARTable
        self.window_name = "MouseTable"
        self.ui = UIInfo(ui_name)
        # Only need a UI and manager. Not doing camera detection
        self.manager = UIManager(self.ui)
        self.on_key = on_key
        self.is_running = False
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.stop_event = threading.Event()

        # Bubble this up for ease-of-access
        self.on_hover = self.manager.on_hover
        self.on_enter = self.manager.on_enter
        self.on_exit = self.manager.on_exit
        
    def stop(self):
        self.stop_event.set()
    def _run(self):
        self.is_running = True
        has_pressed = False
        add_mouse_pointer(self.manager, self.window_name)
        while not self.stop_event.is_set():
            rendered = manager.draw()
            cv2.imshow(self.window_name, rendered)
            keys = cv2.waitKey(1) & 0xFF
            if keys in map(ord,'q'):
                if not has_pressed:
                    has_pressed = True
                    if keys == ord('q'):
                        break
            else:
                has_pressed = False
                if self.on_key is not None:
                    self.on_key(keys)
        cam.release()
        cv2.destroyAllWindows()
        self.is_running = False
    def start_sync(self):
        pass
    def start_threaded(self):
        pass


def add_mouse_pointer(manager, window_name):
    def on_mouse(event, x, y, flags, params):
        manager.update_pointer("mouse", (x, y))
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, on_mouse)

def main():
    ui_name = "piano"
    finger_color = (44, 50, 85)
    finger_thres = 11
    webcam_id = 1

    def on_enter(pointer_name, x, y, w, h, button):
        print(f"Pointer {pointer_name} entered {button} @ ({x} / {w}, {y} / {h})")
    
    table = ARTable(ui_name, None, webcam_id, finger_color, finger_thres)
    table.on_enter(on_enter)
    table.start_sync()

if __name__ == '__main__':
    main()