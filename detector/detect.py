import os
import sys

import cv2
from dotenv import load_dotenv
from redis import Redis

from accident_detect import AccidentDetector

sys.path.insert(0, "Yolov5_DeepSort_Pytorch/yolov5")
sys.path.append("Yolov5_DeepSort_Pytorch")
sys.path.append("Yolov5_DeepSort_Pytorch/deep_sort")
sys.path.append('Yolov5_DeepSort_Pytorch/deep_sort/deep/reid')

from dataset import LoadMedia

from Yolov5_DeepSort_Pytorch.yolov5.models.common import DetectMultiBackend

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import os
from pathlib import Path
import torch

from Yolov5_DeepSort_Pytorch.yolov5.utils.general import (check_img_size, non_max_suppression, scale_coords, xyxy2xywh,
                                                          LOGGER)
from Yolov5_DeepSort_Pytorch.yolov5.utils.torch_utils import select_device, time_sync
from Yolov5_DeepSort_Pytorch.deep_sort.utils.parser import get_config
from Yolov5_DeepSort_Pytorch.deep_sort.deep_sort import DeepSort
from Yolov5_DeepSort_Pytorch.yolov5.utils.plots import colors, Annotator

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # yolov5 deepsort root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

LOCATION_NAME = 'Brest/Kolesnika.1.(perekrestok)'

load_dotenv()

IMAGE_PATH = os.environ.get('DETECTOR_IMAGE_DIR')
VIDEO_FRAGMENTS_PATH = os.environ.get('DETECTOR_VIDEO_DIR')
SAVE_VIDEO_PATH = os.environ.get('DETECTOR_ACCIDENT_SAVE_DIR')
SAVE_RESULT = os.environ.get('DETECTOR_RESULT_DIR')
MAX_RESULT = int(os.environ.get('DETECTOR_MAX_RESULT'))
REDIS_HOST = os.environ.get('REDIS_HOST')
redis = Redis(host=REDIS_HOST, port=6379, db=0)


def detect():
    device = ''
    config_deepsort = 'Yolov5_DeepSort_Pytorch/deep_sort/configs/deep_sort.yaml'
    deep_sort_model = 'osnet_x0_25'
    half = True
    yolo_model = 'yolov5m.pt'
    conf_thres = 0.3
    iou_thres = 0.5
    classes = [1, 2, 3, 5, 7]
    agnostic_nms = True
    augment = True
    visualize = False
    max_det = 1000
    imgsz = 640
    dnn = True

    accident_detector = AccidentDetector()

    device = select_device(device)
    # initialize deepsort
    cfg = get_config()
    cfg.merge_from_file(config_deepsort)
    deepsort = DeepSort(deep_sort_model,
                        device,
                        max_dist=cfg.DEEPSORT.MAX_DIST,
                        max_iou_distance=cfg.DEEPSORT.MAX_IOU_DISTANCE,
                        max_age=cfg.DEEPSORT.MAX_AGE, n_init=cfg.DEEPSORT.N_INIT, nn_budget=cfg.DEEPSORT.NN_BUDGET,
                        )

    # Initialize

    half &= device.type != 'cpu'  # half precision only supported on CUDA

    # Directories
    # save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
    # save_dir.mkdir(parents=True, exist_ok=True)  # make dir

    # Load model
    device = select_device(device)
    model = DetectMultiBackend(yolo_model, device=device, dnn=dnn)
    stride, names, pt, jit, _ = model.stride, model.names, model.pt, model.jit, model.onnx
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    # Half
    half &= pt and device.type != 'cpu'  # half precision only supported by PyTorch on CUDA
    if pt:
        model.model.half() if half else model.model.float()

    # Dataloader
    dataset = LoadMedia(IMAGE_PATH, img_size=imgsz, stride=stride, auto=pt and not jit)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names

    if pt and device.type != 'cpu':
        model(torch.zeros(1, 3, *imgsz).to(device).type_as(next(model.model.parameters())))  # warmup
    dt, seen = [0.0, 0.0, 0.0, 0.0], 0
    for frame_idx, (path, img, im0s, vid_cap, s) in enumerate(dataset):
        t1 = time_sync()
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        t2 = time_sync()
        dt[0] += t2 - t1

        # Inference
        # visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
        pred = model(img, augment=augment, visualize=visualize)
        t3 = time_sync()
        dt[1] += t3 - t2

        # Apply NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms,
                                   max_det=max_det)
        dt[2] += time_sync() - t3

        # Process detections
        for i, det in enumerate(pred):  # detections per image
            seen += 1
            p, im0, _ = path, im0s.copy(), getattr(dataset, 'frame', 0)

            s += '%gx%g ' % img.shape[2:]  # print string

            annotator = Annotator(im0)

            if det is not None and len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(
                    img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                xywhs = xyxy2xywh(det[:, 0:4])
                confs = det[:, 4]
                clss = det[:, 5]

                # pass detections to deepsort
                t4 = time_sync()
                outputs = deepsort.update(xywhs.cpu(), confs.cpu(), clss.cpu(), im0)
                t5 = time_sync()
                dt[3] += t5 - t4

                if len(outputs) > 0:
                    ids = []
                    for j, (output, conf) in enumerate(zip(outputs, confs)):
                        bboxes = output[0:4]
                        id = output[4]
                        cls = output[5]

                        c = int(cls)  # integer class
                        label = f'{id} {names[c]} {conf:.2f}'
                        annotator.box_label(bboxes, label, color=colors(c, True))
                        ids.append(id)

                    accident_detector.add_time(t1, ids)
                    # if accident_detector.is_accident():
                    #     save_accident_video(VIDEO_FRAGMENTS_PATH, SAVE_VIDEO_PATH)
                redis.set('yolo_time', t3 - t2)
                redis.set('deep_sort_time', t5 - t4)
                redis.set('detect_fps', 1 / (t5 - t1))
                LOGGER.info(f'{s}Done. YOLO:({t3 - t2:.3f}s), DeepSort:({t5 - t4:.3f}s)')

            else:
                deepsort.increment_ages()
                LOGGER.info('No detections')

            im0 = annotator.result()
            cv2.imwrite(os.path.join(SAVE_RESULT, str(t1)) + '.jpg', im0)
            files = os.listdir(SAVE_RESULT)
            files.sort(reverse=True)
            if len(files) > 0:
                for file_to_remove in files[MAX_RESULT:]:
                    os.remove(os.path.join(SAVE_RESULT, file_to_remove))
            # im12 = cv2.resize(im0, (800, 600))
            # cv2.imshow('1', im12)
            # if cv2.waitKey(1) == ord('q'):  # q to quit
            #     raise StopIteration


if __name__ == '__main__':
    detect()
