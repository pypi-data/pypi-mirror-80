try:
    import cv2
except ImportError:
    cv2_found = False
else:
    cv2_found = True

try:
    from . import ARTable
except ImportError:
    tablefound = False
else:
    tablefound = True

import numpy as np
import time
import os
import sys
import json

def clear_screen():
    if sys.platform == "win32":
        os.system("cls")
    else:
        os.system("clear")

def introduction():
    clear_screen()
    print("Julie Ganeshan - Table AR")
    print("Welcome to the guided setup of TableAR!")
    print("This is a paper-printed UI that can be interacted with when tracked with a webcam")
    print("This setup will get all the calibration info necessary for TableAR to work")
    print("You'll see several text prompts in your console, and some graphical windows.")
    print("Keep an eye on your console for instructions!")
    conf = wait_for_confirmation("I'll use brackets whenever I'm expecting input. Ready?")
    if conf:
        print("Great!")
        return True
    else:
        print("Okay, doing nothing. Re-run whenever you're ready!")
        return False

def check_cv2():
    print("First, let's check if you have OpenCV installed: ")
    if cv2_found:
        print("You do! Let's move on.")
        return True
    else:
        print("I couldn't find OpenCV. Please install it using the following command:")
        print("$ python -m pip install opencv-python")
        print("When it's installed, re-run the setup.")
        return False

def check_running_as_module():
    if not tablefound:
        print("Right now the guided setup is running incorrectly. Please run it as a module.")
        print("Exiting...")
        return False
    else:
        return True

def ask_for_print(ui_path):
    print("TableAR tracks a checkerboard pattern. Any UI you make MUST include this.")
    print("Every UI consists of 2 or 3 images, a printable sheet, a mask, and an optional rendered view")
    print("Please print this. Do NOT resize it - let the printer clip it. You can find it here:")
    print(f"{ui_path}.png")
    conf = wait_for_confirmation("Have you printed the UI?")
    if conf:
        print("Lovely! I also recommend having tape. Otherwise, the UI shifts as you use it.")
        return True
    else:
        print("Okay, re-run setup when you're ready to print.")
        return False

def preview_video(cam_id, settings = None, on_key = None, on_mouse = None):
    if type(cam_id) is int:
        additional_args = (cv2.CAP_DSHOW,)
    else:
        additional_args = tuple([])
    vid = cv2.VideoCapture(cam_id, *additional_args)
    valid_input = False
    print("Press 'p' to pause, 'q' within the window to finish...")
    img_to_send = [None]
    def wrapped_on_mouse(event, x, y, flags, params):
        if on_mouse is not None and event == cv2.EVENT_LBUTTONDOWN:
            on_mouse(x,y, img_to_send[0])
    cv2.namedWindow("Preview")
    cv2.setMouseCallback("Preview", wrapped_on_mouse)
    is_paused = False
    has_pressed = False
    while(True):
        if not is_paused:
            ret, color_img = vid.read()
            if not ret:
                break
            valid_input = True
            if settings is not None:
                if 'hflip' in settings and settings['hflip']:
                    color_img = color_img[:,::-1,:]
                if 'vflip' in settings and settings['vflip']:
                    color_img = color_img[::-1, :, :]
                (h,w,c) = color_img.shape
            img_to_send[0] = color_img
        # Update hand mask even if paused
        if settings is not None:
            if 'skintone' in settings:
                mask = ARTable.detect_color(color_img, settings['skintone'], settings['skintone_thresh'])
                mask_img = ARTable.to_color(ARTable.mask_to_image(mask))
                img_to_show = ARTable.hcat(color_img, mask_img)
            else:
                img_to_show = color_img
        else:
            img_to_show = color_img   
        cv2.imshow("Preview", img_to_show)
        keys = cv2.waitKey(16) & 0xFF
        if keys == ord('q'):
            break
        elif keys == ord('p'):
            if not has_pressed:
                is_paused = not is_paused
                has_pressed = True
        else:
            has_pressed = False
        
        if on_key is not None:
            on_key(keys)
    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
    return valid_input

def find_webcam(settings):
    print("TableAR relies on a webcam (internal or external) to track your piano.")
    print("You can also use a pre-recorded video, though this won't be interactive.")
    conf = wait_for_confirmation("Do you have a webcam or video to use?")
    if not conf:
        print("Sorry, you need a camera or video to use TableAR")
        return False
    print("Let's find it!")
    print("TableAR supports 3 types of input:")
    print("1) An internal or external webcam, connected to your computer")
    print("2) An IP camera (like a phone w/app)")
    print("3) A video file")
    mode_input = input("[1/2/3] Which are you using? -> ")
    should_quit = False
    while mode_input.strip() not in ["1", "2", "3"] and not should_quit:
        print("Sorry, that's not a valid mode!")
        mode_input = input("[1 / 2 / 3 / Q] Which would you like? (Q to quit) -> ")
        if mode_input.lower().startswith('q'):
            should_quit = True
    if should_quit:
        print("Quitting. Re-run when you're ready.")
        return False
    webcam_id = None
    mode_input_int = int(mode_input)
    while webcam_id is None:
        if mode_input_int == 1:
            print("Each camera connected to your computer has a unique # id.")
            print("The first camera (often front facing) has ID 0. The next (rear or external) has ID 1, and so on.")
            webcam_id_inp = input("[#] Please enter the webcam ID. We'll then check to make sure it's valid. -> ")
            try:
                webcam_id_inp = int(webcam_id_inp)
            except:
                if wait_for_confirmation("That's not a number. Try again?"):
                    continue
                else:
                    break
            print("Now, I'm going to show a window with the stream from that webcam. It may be minimized.")
            is_valid_video = preview_video(webcam_id_inp)
            if not is_valid_video:
                if wait_for_confirmation("Oops! Looks like that's not a valid webcam. Try again?"):
                    continue
                else:
                    break
            conf = wait_for_confirmation("Is this the right webcam?")
            if conf:
                print("Okay! Let me save that...")
                webcam_id = webcam_id_inp
            else:
                clear_screen()
                print("Okay, let's try finding your integrated/USB webcam again.")

        elif mode_input_int == 2:
            webcam_id_inp = input("[url] Every IP camera has a URL that connects directly to the stream. What's that URL?\n-> ")
            print("I'm going to try showing this stream")
            is_valid_video = preview_video(webcam_id_inp)
            if not is_valid_video:
                if wait_for_confirmation("Oops! Looks like that's not a valid stream. Try again?"):
                    continue
                else:
                    break
            conf = wait_for_confirmation("Is this the right webcam?")
            if conf:
                print("Okay! Let me save that...")
                webcam_id = webcam_id_inp
            else:
                clear_screen()
                print("Okay, let's try finding your IP webcam again.")

        elif mode_input_int == 3:
            webcam_id_inp = os.path.abspath(input("[filepath] Please enter the path to the video file:\n-> "))
            if not os.path.isfile(webcam_id_inp):
                if wait_for_confirmation("That's not a file on your system. Try again?"):
                    continue
                else:
                    break
            print("I found the file. I'm going to play some of it.")
            is_valid_video = preview_video(webcam_id_inp)
            if not is_valid_video:
                print("Looks like that's an unsupported format.")
                if wait_for_confirmation("Try again?"):
                    continue
                else:
                    break
            conf = wait_for_confirmation("Is this the right video?")
            if conf:
                print("Okay! Let me save that...")
                webcam_id = webcam_id_inp
            else:
                clear_screen()
                print("Okay, let's try finding your video file again...")
        else:
            print("Invalid mode detected. Quitting.")
            return False
    if webcam_id is not None:
        settings['webcam'] = webcam_id
        return True
    else:
        print("No webcam found. Quitting.")
        return False

def guide_positioning(settings):
    webcam_id = settings['webcam']
    print("Now that we have your webcam, we need to position the camera and paper.")
    print("Please place (preferably tape) your UI to a clean surface. The less cluttered, the better.")
    print("Then, position your camera so that **it can see the whole checkerboard**, and all 4 corners of the page. Anything not visible won't be trackable!")
    print("Additionally, the vertical / horizontal direction of the pattern must be maintained (longer H than V)")
    preview_video(webcam_id)
    return wait_for_confirmation("Okay to move on?")

def find_flips(settings):
    settings['hflip'] = False
    settings['vflip'] = False
    print("TableAR needs the checker pattern to be right-side up (wide, top-left is white)")
    print("I'm going to show you a preview stream. In the window,")
    print("Press 'H' to flip horizontally, and 'V' to flip vertically")
    print("Until the pattern looks right.")
    def on_key(k):
        if k == ord('v'):
            settings['vflip'] = not settings['vflip']
        if k == ord('h'):
            settings['hflip'] = not settings['hflip']
    preview_video(settings['webcam'], settings, on_key)
    conf = wait_for_confirmation("Is the pattern right side-up (roughly)?")
    if conf:
        print("Great!")
        return True
    else:
        print("Sorry. You need to have a right-side up view. Quitting.")
        return False


def find_skintone(settings):
    # Just a silly initialization
    settings['skintone'] = (0,0,0)
    settings['skintone_thresh'] = 10
    settings['has_pressed'] = False
    def on_mouse(x, y, img):
        settings['skintone'] = tuple(map(int, img[y, x]))
    def on_key(k):
        if k in map(ord, '[]'):
            if not settings['has_pressed']:
                if k == ord('['):
                    settings['skintone_thresh'] -= 1
                elif k == ord(']'):
                    settings['skintone_thresh'] += 1
                settings['skintone_thresh'] = min(max(0, settings['skintone_thresh']), 255)
                settings['has_pressed'] = True
        else:
            settings['has_pressed'] = False
    print("Find your skintone by clicking it. RH image shows detected fingers")
    print("Use [ and ] to adjust threshold. P to pause is useful, here")
    preview_video(settings['webcam'], settings, on_key, on_mouse)
    del settings['has_pressed']
    conf = wait_for_confirmation("Skintone OK?")
    if conf:
        print("Saving skintone")
        return True
    else:
        print("Exiting.")
        return False

def save_settings(settings):
    with open(ARTable.default_config_path, 'w') as f:
        json.dump(settings, f, sort_keys=True, indent=4)

def wait_for_confirmation(prompt):
    user_inp = input(f"[Y/N] {prompt} -> ")
    if user_inp.lower().startswith('y') or len(user_inp.strip()) == 0:
        return True
    else:
        return False

def print_divider(step_num):
    print("%s STEP %d %s" % ('-' * 15,step_num,'-' * 15))


def main(ui_path):
    settings = {}
    module_success = check_running_as_module()
    if not module_success:
        return
    clear_screen()
    print_divider(1)
    intro_success = introduction()
    if not intro_success:
        return
    clear_screen()
    print_divider(2)
    cv2_success = check_cv2()
    if not cv2_success:
        return
    clear_screen()
    print_divider(3)
    print_success = ask_for_print(ui_path)
    if not print_success:
        return
    clear_screen()
    print_divider(4)
    find_webcam_success = find_webcam(settings)
    if not find_webcam_success:
        return
    clear_screen()
    print_divider(5)
    positioning_success = guide_positioning(settings)
    if not positioning_success:
        print("Quitting")
        return
    clear_screen()
    print_divider(6)
    flips_success = find_flips(settings)
    if not flips_success:
        return
    clear_screen()
    print_divider(7)
    skintone_success = find_skintone(settings)
    if not skintone_success:
        return
    clear_screen()
    print("Fully calibrated! Saving to disk.")
    save_settings(settings)
    print("Calibration saved to disk!")

if __name__ == '__main__':
    default_ui = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui", "base")
    main(default_ui)