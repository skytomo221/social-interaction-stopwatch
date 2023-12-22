import cv2

# 動画
LOAD_FILE = 'movie/00050.mp4'
SAVE_FILE = 'movie/00050-trimed.mp4'
THRESHED_SAVE_FILE = 'movie/00050-threshed.mp4'

# ねずみの設定
MOUSE_THRESHOLD = 64
MOUSE_SIZE = 2000

# ぼかしの強さ
BLUR = 15

# 速度
SPEED = 1

CAPTURE = cv2.VideoCapture(LOAD_FILE)
WIDTH = int(CAPTURE.get(cv2.CAP_PROP_FRAME_WIDTH))
HEIGHT = int(CAPTURE.get(cv2.CAP_PROP_FRAME_HEIGHT))
FOURCC = int(CAPTURE.get(cv2.CAP_PROP_FOURCC))
COUNT = int(CAPTURE.get(cv2.CAP_PROP_FRAME_COUNT))
FPS = CAPTURE.get(cv2.CAP_PROP_FPS) / 2
SAVED_FPS = FPS / SPEED
DURATION = COUNT / FPS
WRITER = cv2.VideoWriter(SAVE_FILE, FOURCC, SAVED_FPS, (WIDTH, HEIGHT), 1)
THRESHED_WRITER = cv2.VideoWriter(THRESHED_SAVE_FILE, FOURCC, SAVED_FPS, (WIDTH, HEIGHT), 0)

print(f'入力元：{LOAD_FILE}')
print(f'出力先：{SAVE_FILE}')
print(f'マウスの黒さ：{MOUSE_THRESHOLD}/255')
print(f'マウスの大きさ：{MOUSE_SIZE}ピクセル')
print(f'動画の大きさ（幅×高さ）：{WIDTH} × {HEIGHT}')
print(f'フォーマット：{FOURCC:x}')
print(f'フレーム数：{COUNT}')
print(f'FPS：{FPS}')
print(f'動画の長さ（秒）：{DURATION}')

for frame_index in range(COUNT):
    valid, frame = CAPTURE.read()
    if valid == False:
        break
    if frame_index % 100 == 0:
        print(f'処理：{COUNT}フレームのうち{frame_index}フレーム（{frame_index / FPS:.3f}秒）を処理しました。')
    if frame_index % SPEED != 0:
        continue
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blured_frame = cv2.GaussianBlur(gray_frame, (BLUR, BLUR), 0)
    _, threshed_frame = cv2.threshold(blured_frame, MOUSE_THRESHOLD, 255, cv2.THRESH_BINARY)
    negative_frame = cv2.bitwise_not(threshed_frame)
    contours, hierarchy = cv2.findContours(negative_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered_contours = list(filter(lambda contour: cv2.contourArea(contour) > MOUSE_SIZE, contours))
    MOUSE_COUNT = len(filtered_contours)
    cv2.putText(frame, f'mouse: {MOUSE_COUNT}, frame: {frame_index}', (0, 50), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 5, cv2.LINE_AA)
    cv2.drawContours(frame, filtered_contours, -1, (102, 0, 255), 2)
    for i, contour in enumerate(filtered_contours):
        m = cv2.moments(contour)
        x, y = m['m10'] / m['m00'], m['m01'] / m['m00']
        x, y = round(x), round(y)
        cv2.putText(frame, f'{i + 1}', (x, y), cv2.FONT_HERSHEY_PLAIN, 4, (102, 0, 255), 5, cv2.LINE_AA)
    if (MOUSE_COUNT != 0 and MOUSE_COUNT != 2):
        WRITER.write(frame)
    THRESHED_WRITER.write(negative_frame)

WRITER.release()
THRESHED_WRITER.release()
CAPTURE.release()
cv2.destroyAllWindows()
