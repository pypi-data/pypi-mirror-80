import cv2
import numpy as np
import os
from typing import List, Tuple, Callable, Callable, NoReturn, Union
import threading
import json
import colorsys

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

default_config_path = os.path.join(mydir, "config.json")

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

def to_hsv(im: TColorImage) -> TColorImage:
    if len(im.shape) == 3:
        return cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    else:
        return to_hsv(to_color(im))

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

def image_to_mask(image: TGrayImage) -> TMask:
    mask = np.zeros(image.shape, dtype=np.bool)
    mask[image > 127] = True
    return mask

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

def detect_color_hsv(color_img, detection_low, detection_high):
    hsv_img = to_hsv(color_img)
    detection_low_arr = np.array(detection_low, dtype=np.uint8)
    detection_high_arr = np.array(detection_high, dtype=np.uint8)
    correct_color_mask = cv2.inRange(hsv_img, detection_low_arr, detection_high_arr)
    return image_to_mask(cv2.blur(correct_color_mask, (7,7)))
    

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

def save_required_checkerboard(fpath = None):
    return make_checkerboard(CHECKER_DIMS[0] + 1, CHECKER_DIMS[1] + 1, 100, fpath)

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
        # Should we render different than what's printed?
        render_image_fp = os.path.join(root_dir, f"{self.name}_render.png")
        if os.path.isfile(render_image_fp):
            render_image = to_color(cv2.imread(render_image_fp))
        else:
            render_image = to_color(myui)

        # Make mask by finding discrete colors in sorted order
        # Quantize to multiples of 10
        mask_raw = mask_raw // 10
        mask_levels = sorted(set(mask_raw.ravel()))
        mask = np.zeros(mask_raw.shape, dtype=np.int)
        for (level_ix, each_level) in enumerate(mask_levels):
            mask[mask_raw == each_level] = level_ix
        
        # Find the chessboard in the UI
        og_corners_found, og_corners = cv2.findChessboardCorners(myui, CHECKER_DIMS)
        assert og_corners_found, "UI image must contain chessboard"

        # Save button names, if they exist
        name_fp = os.path.join(root_dir, f"{self.name}_names.txt")
        if os.path.isfile(name_fp):
            with open(name_fp,'r') as name_f:
                self.names = [
                    stripped_line for stripped_line in 
                    [
                        line.strip() for line in name_f.read().splitlines()
                    ] 
                    if len(stripped_line) > 0
                ]
                assert len(self.names) >= len(mask_levels), (
                    "Name file must name every button 0 going up")
        else:
            self.names = list(range(len(mask_levels)))

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

    def get_known_pointers(self):
        return self.pointers.keys()
    
    def get_position(self, pointer_name):
        if pointer_name in self.pointers:
            return self.pointers[pointer_name][0]
        else:
            return None

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
                on_enter_args = (pointer_name, *new_position, self.ui.width, self.ui.height, self.ui.names[new_button])
            if prev_button is not None:
                # Don't call exit when pointer wasn't there before
                on_exit_args = (pointer_name, *prev_position, self.ui.width, self.ui.height, self.ui.names[prev_button])

        # Check for on_hover
        else:
            if new_position is not None:
                on_hover_args = (pointer_name, *new_position, self.ui.width, self.ui.height, self.ui.names[new_button])
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

def IOU(a, b):
    return area(intersection(a,b)) / max(0.0001, area(union(a,b)))

def area(bbox):
    return bbox[2] * bbox[3]

def union(a,b):
    x = min(a[0], b[0])
    y = min(a[1], b[1])
    w = max(a[0]+a[2], b[0]+b[2]) - x
    h = max(a[1]+a[3], b[1]+b[3]) - y
    return (x, y, w, h)

def intersection(a,b):
    x = max(a[0], b[0])
    y = max(a[1], b[1])
    w = min(a[0]+a[2], b[0]+b[2]) - x
    h = min(a[1]+a[3], b[1]+b[3]) - y
    if w<0 or h<0:
        return (0, 0, 0, 0)
    else:
        return (x, y, w, h)

def is_central(bbox, w, h, margin = 0.05):
    x, y, bw, bh = bbox
    xmin_allowed = round(margin * w)
    xmax_allowed = w - xmin_allowed
    ymin_allowed = round(margin * h)
    ymax_allowed = h - ymin_allowed
    if (x >= xmax_allowed or x + bw <= xmin_allowed) or (y >= ymax_allowed or y + bh <= ymin_allowed):
        return False
    else:
        return True

def sqrDistance(pointA, pointB):
    (Ax, Ay) = pointA
    (Bx, By) = pointB
    return (Ax - Bx) ** 2 + (Ay - By) ** 2

class ColorPointer(object):
    def __init__(self, manager: UIManager,
                 color_low = (0, 120, 30),
                 color_high = (33, 255, 255),
                 contour_threshold = 100):
        self.manager = manager
        self.color_low = color_low
        self.color_high = color_high
        self.contour_threshold = contour_threshold
        self.mask = None
        self.mask_drawn = None
    
    def update(self, unwarped_frame):
        found_fingers = False
        finger_tips = []
        if unwarped_frame is not None:
            # We can do detection
            color_mask = detect_color_hsv(unwarped_frame, self.color_low, self.color_high)
            self.mask = color_mask
            #self.mask_drawn = to_color(mask_to_image(self.mask))
            contours, contour_hierarchy = cv2.findContours(mask_to_image(self.mask), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            self.mask_drawn = np.zeros(unwarped_frame.shape, dtype=np.uint8)
            # Now let's filter to only big contours
            good_contours = [c for c in contours if cv2.contourArea(c) > self.contour_threshold]
            # Then, let's filter to only contours in the central area
            (h,w) = color_mask.shape
            contour_bboxes = [cv2.boundingRect(c) for c in good_contours]
            central_contours = [good_contours[i] for i in range(len(good_contours)) if is_central(contour_bboxes[i], w, h)]
            if len(central_contours) > 0:
                hand_contour = max(central_contours, key=lambda ctr: cv2.contourArea(ctr))
            else:
                hand_contour = None

            if hand_contour is not None:
                hand_hull = cv2.convexHull(hand_contour, returnPoints=False)
                # Find defects from the convex hull - these are the indents between
                # fingers
                #cv2.drawContours(self.mask_drawn, [hand_contour], -1, (0, 255, 0), 3)
                defects = cv2.convexityDefects(hand_contour, hand_hull)
                points_to_draw = []
                # It should be at least 5% of the smaller screen dim
                defect_distance_thres = min(h,w) // 20
                n_lines = 0
                finger_defects = []
                for defect_ix, each_defect in enumerate(defects):
                    start_point_ix, end_point_ix, farthest_point_ix, distance_to_farthest = each_defect.ravel()
                    start_px = tuple(hand_contour[start_point_ix].ravel())
                    middle_px = tuple(hand_contour[farthest_point_ix].ravel())
                    end_px = tuple(hand_contour[end_point_ix].ravel())
                    # Change from fixed to floating point
                    distance_to_farthest = distance_to_farthest / 256
                    # This has our fingers, perfectly, but also a bit of noise.
                    # Let's filter by distance_to_farthest
                    if distance_to_farthest > defect_distance_thres:
                        finger_defects.append((start_px, middle_px, end_px, distance_to_farthest))
                # In the most common case, the  hand is coming in from the bottom
                # so let's sort by middle-X to get the convexity defect on the edges of each finger in order
                finger_defects.sort(key=lambda defect: defect[1][0])
                
                # List comprehension to make a 10 color palette
                known_colors = [
                    (int(255 * col_b), int(255 * col_g), int(255 * col_r))
                    for (col_r, col_g, col_b) in [
                        colorsys.hsv_to_rgb(palette_hue, 0.9, 0.8)
                        for palette_hue in np.linspace(0, 0.8, 10)
                    ]
                ]

                # Now, we have the "defects", which specify start/end as the finger
                # tips, and middle as the space between fingers. We want the opposite -
                # start / end between fingers, and middle as the tip

                fingers_merged = []
                
                # The width of the finger should be at most 20% of the screen
                finger_merge_distance = (max(h,w) // 10) ** 2
                # So, let's merge adjacent defects
                for defect_ix in range(len(finger_defects)-1):
                    L_start, L_middle, L_end, L_distance = finger_defects[defect_ix]
                    R_start, R_middle, R_end, R_distance = finger_defects[defect_ix+1]
                    # start/end are arbitrary here. Let's collect them both into small lists
                    L_points = [L_start, L_end]
                    R_points = [R_start, R_end]
                    possible_adjacent_pairs = [(0,0), (0,1), (1,0), (1,1)]
                    # Find the best one
                    # pair_poss is an index into L_points, then R_points, which contains tuples
                    # Using sqr distance
                    best_pair = min(possible_adjacent_pairs, key=lambda pair_poss:sqrDistance(L_points[pair_poss[0]], R_points[pair_poss[1]]))
                    
                    # This gets us the best pairing! Use the closer points
                    # as start/end respectively
                    # We know these are length 2, so we can do 1 - INDEX to get "the other point"
                    L_start, L_end = (L_points[1 - best_pair[0]], L_points[best_pair[0]])
                    R_start, R_end = (R_points[best_pair[1]], R_points[1-best_pair[1]])

                    if sqrDistance(L_end, R_start) < finger_merge_distance:
                        # Just average L end with R start to find the shared point!
                        new_start = L_middle
                        # Hack - just take the bigger y
                        new_middle = tuple([round((L_end[coord] + R_start[coord]) / 2) for coord in range(2)])
                        new_end = R_middle
                        fingers_merged.append((new_start, new_middle, new_end))

                # Draw the detected fingers
                for finger_ix, (start_px, middle_px, end_px) in enumerate(fingers_merged):
                    # Drawing with color, because now they are stable-ish
                    color = known_colors[min(len(known_colors), finger_ix)]
                    cv2.line(self.mask_drawn, start_px, middle_px, color, 2)
                    cv2.line(self.mask_drawn, middle_px, end_px, color, 2)

                # Simplify for just finger tips
                finger_tips = [middle_px for (start_px, middle_px, end_px) in fingers_merged]
                found_fingers = True

        if found_fingers:
            # If we found fingers, then we assigned to finger tips.
            # We'll call our fingers finger0...fingerN
            # First let's get which ones we need to update,
            # and their finger numbers
            existing_pointers = [
                (pointer_name, self.manager.get_position(pointer_name))
                for pointer_name in self.manager.get_known_pointers()
                if pointer_name.startswith('finger')
            ]
            
            # Everything we've found this frame must be assigned / added
            found_not_assigned = set(range(len(finger_tips)))
            
            # Anything we had previous must be deleted, if it wasn't assigned
            prev_not_found = set([ptr_name for (ptr_name, ptr_loc) in existing_pointers])

            for (ptr_name, prev_loc) in existing_pointers:
                if len(found_not_assigned) == 0:
                    # We've assigned everything we've got
                    break
                # Find the closest detected pointer
                best_match = min(found_not_assigned, key=lambda finger_ix:sqrDistance(finger_tips[finger_ix], prev_loc))
                # Move this pointer to the newly detected location
                self.manager.update_pointer(ptr_name, finger_tips[best_match])
                # And mark that we've assigned it
                found_not_assigned.remove(best_match)
                prev_not_found.remove(ptr_name)
            
            # We have 3 cases (at the start)
            # len(found_not_assigned) > len(prev_not_found):
            #   -- We assign every prev pointer then add some
            #   -- So now, prev_not_found is empty
            # len(prev_not_found) > len(found_not_assigned):
            #   -- prev_not_found has stale pointers
            #   -- Nothing left in found_not_assigned
            # len(prev_not_found) == len(found_not_assigned):
            #   -- They're both done!
            # Thus, the order of add/remove doesn't really matter, as only
            # one will happen

            # Delete stale pointers
            for ptr_name in prev_not_found:
                self.manager.update_pointer(ptr_name, None)
            
            # Add newly found pointers
            for finger_ix in found_not_assigned:
                # Get a pointer name we haven't used yet
                N = 0
                next_pointer_name = f"finger{N}"
                while next_pointer_name in self.manager.pointers:
                    N += 1
                    next_pointer_name = f"finger{N}"
                self.manager.update_pointer(next_pointer_name, finger_tips[finger_ix])
            
            # Now we've updated all the finger pointers!    
            

            

class UserSettings(object):
    def __init__(self, 
            webcam: Union[int, str], 
            hflip: bool, 
            vflip: bool,
            skintone_low: TBGR8Color,
            skintone_high: int):
        self.webcam = webcam
        self.hflip = hflip
        self.vflip = vflip
        self.skintone_low = skintone_low
        self.skintone_high = skintone_high
    def save(self, fpath: str):
        with open(fpath, 'w') as f:
            json.dump({
                "webcam": self.webcam, 
                "hflip": self.hflip, 
                "vflip": self.vflip, 
                "skintone_low": self.skintone_low, 
                "skintone_high": self.skintone_high
            }, f, indent=4, sort_keys=True)
    @staticmethod
    def load(fpath: str):
        assert os.path.isfile(fpath), f"Config file {fpath} doesn't exist. Please use UserSetup to make one."
        with open(fpath, 'r') as f:
            dct = json.load(f)
        # Make sure it's valid
        assert tuple(sorted(dct.keys())) == tuple(
            sorted([
                "webcam", 
                "hflip", 
                "vflip", 
                "skintone_low", 
                "skintone_high"])
            ), "Config file is invalid"
        return UserSettings(**dct)
    @staticmethod
    def get_default():
        return UserSettings(0, False, False, (0, 120, 30), (33, 255, 255))
    
    @staticmethod
    def load_global_settings():
        return UserSettings.load(default_config_path)

    @staticmethod
    def load_or_default(fpath: str):
        try:
            return UserSettings.load(fpath)
        except:
            return UserSettings.get_default()
    def transform_feed(self, color_img):
        (h,w,c) = color_img.shape
        if self.hflip:
            color_img = color_img[:,::-1,:]
        if self.vflip:
            color_img = color_img[::-1, :, :]
        return color_img


class ARTable(object):
    def __init__(self, ui_name, on_key, user_settings: UserSettings):
        self.window_name = "ARTable"
        self.webcam_id = user_settings.webcam
        self.settings = user_settings
        self.ui = UIInfo(ui_name)
        self.detector = UIDetector(self.ui)
        self.manager = UIManager(self.ui)
        self.finger = ColorPointer(self.manager, self.settings.skintone_low, self.settings.skintone_high)
        self.on_key = on_key
        self.is_running = False
        self.thread = None
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
        is_paused = False
        while not self.stop_event.is_set():
            if not is_paused:
                ret, frame = cam.read(1)
                if not ret:
                    break
                # Apply flips as needed
                frame = self.settings.transform_feed(frame)
            self.detector.update_calibration(frame)
            unwarped = self.detector.unwarp_frame(frame)
            self.finger.update(unwarped)
            rendered = self.manager.draw()
            finger_mask = self.finger.mask_drawn#to_color(mask_to_image(self.finger.mask))
            black = np.zeros_like(frame)
            output_image = vcat(
                hcat(frame, unwarped if unwarped is not None else black),
                hcat(finger_mask if finger_mask is not None else black, rendered)
            )
            cv2.imshow(self.window_name, output_image)
            keys = cv2.waitKey(1) & 0xFF
            if keys in map(ord,'qcp'):
                if not has_pressed:
                    has_pressed = True
                    if keys == ord('p'):
                        is_paused = not is_paused
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
        if not self.is_running:
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.run()
    def start_threaded(self):
        if not self.is_running:
            self.thread = threading.Thread(target=self._run, daemon=True)
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

def main(ui_name = 'piano'):
    def on_enter(pointer_name, x, y, w, h, button):
        print(f"Pointer {pointer_name} entered {button} @ ({x} / {w}, {y} / {h})")
    
    settings = UserSettings.load_global_settings()
    table = ARTable(ui_name, None, settings)
    table.on_enter(on_enter)
    table.start_sync()

if __name__ == '__main__':
    main()