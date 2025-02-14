import mvsdk
import cv2
import numpy as np

def connect():
    DevList = mvsdk.CameraEnumerateDevice()
    nDev = len(DevList)
    if nDev < 1:
        print("Camera is not found")
        return

    DevInfo = DevList[0]

    hCamera = 0
    try:
        hCamera = mvsdk.CameraInit(DevInfo, -1, -1)
    except mvsdk.CameraException as e:
        print("Error ({}): {}".format(e.error_code, e.message))
        return
    
    mvsdk.CameraSetTriggerMode(hCamera, 0)

    mvsdk.CameraSetAeState(hCamera, 0)
    mvsdk.CameraSetExposureTime(hCamera, 30 * 1000)

    mvsdk.CameraPlay(hCamera)
    
    return (hCamera, mvsdk.CameraGetCapability(hCamera))

def get_frame(hCamera, cap):
    FrameBufferSize = cap.sResolutionRange.iWidthMax * cap.sResolutionRange.iHeightMax * 3

    pFrameBuffer = mvsdk.CameraAlignMalloc(FrameBufferSize, 16)

    pRawData, FrameHead = mvsdk.CameraGetImageBuffer(hCamera, 200)
    mvsdk.CameraImageProcess(hCamera, pRawData, pFrameBuffer, FrameHead)
    mvsdk.CameraReleaseImageBuffer(hCamera, pRawData)

    mvsdk.CameraFlipFrameBuffer(pFrameBuffer, FrameHead, 1)

    frame_data = (mvsdk.c_ubyte * FrameHead.uBytes).from_address(pFrameBuffer)
    frame = np.frombuffer(frame_data, dtype=np.uint8)
    frame = frame.reshape((FrameHead.iHeight, FrameHead.iWidth, 1 if FrameHead.uiMediaType == mvsdk.CAMERA_MEDIA_TYPE_MONO8 else 3))

    frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_LINEAR)
    mvsdk.CameraAlignFree(pFrameBuffer)

    return frame

def fps_to_delay(fps): # ms
    return 1000//fps

if __name__ == "__main__":
    FPS = 5
    hCamera, cap = connect()
    delay = fps_to_delay(FPS)

    fourcc = cv2.VideoWriter.fourcc('X', 'V', 'I', 'D')
    out = cv2.VideoWriter('Sources/4.avi', fourcc, 5.0, (640, 480))

    while True:
        frame = get_frame(hCamera, cap)
        out.write(frame)
        cv2.imshow('Grab', frame) 

        if cv2.waitKey(delay) & 0xFF == ord('q'):
                break

    out.release()
    cv2.destroyAllWindows() 