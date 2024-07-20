from model_infer import infer
from ultralytics import YOLO
import cv2
import numpy as np

def draw_boxes(image, boxes, names, cls_id, c_dict, conf):
    img_copy = image.copy()
    objects = []
    for i in range(len(cls_id)):
        x, y, w, h = list(map(int,boxes[i]))
        x1 = int(x - w / 2)
        y1 = int(y - h / 2)
        x2 = int(x + w / 2)
        y2 = int(y + h / 2)
        cv2.rectangle(img_copy, (x1, y1), (x2, y2), c_dict[cls_id[i]], 2)
        conf[i] = "%.2f" % (conf[i]*100)
        font = cv2.FONT_HERSHEY_SIMPLEX
        name = names[cls_id[i]].capitalize()
        text = name + " " + str(conf[i]) + "%"
        objects.append(name)

        (text_width, text_height), _ = cv2.getTextSize(text, font, fontScale=1, thickness=2)
        cv2.rectangle(img_copy, (x1, y1 - 10 - text_height), (x1 + text_width - 10, y1), c_dict[cls_id[i]], -1 )
        cv2.putText(img_copy, text, (x1, y1 - 10), font, 0.9, (255,255,255), 2)
    return (img_copy, objects)

def main(img):
    model = YOLO("yolov8n.pt")
    result = infer(model, img) #img path
    print(result)

    bbox = []
    cls_id = []
    conf = []
    for i in range(len(result.boxes.xywh)):
        bbox.append(result.boxes.xywh[i].tolist())
        cls_id.append(int(result.boxes.cls[i]))
        conf.append(float(result.boxes.conf[i]))

    colors = [(255,0,0),(0,255,0),(0,0,255),(0,255,255),(255,255,0),(255,0,255)]
    c_dict = {}
    i = 0
    for key in set(cls_id):
        c_dict[key] = colors[i]
        i += 1
    
    # c_dict = {}
    # for key in result.names.keys():
    #     c_dict[key] = tuple(random.sample(range(0, 256), 3))
    # print(c_dict)

    # image = cv2.imread(img)
    image = np.array(img)
    image_with_bbox_objs = draw_boxes(image, bbox, result.names, cls_id, c_dict, conf)
    return (image_with_bbox_objs[0], image_with_bbox_objs[1], c_dict, result.names)
    # print(result)

# Unit Testing
# img = main("image copy 8.png")
# cv2.imshow("Image with Bounding Boxes", cv2.resize(img, (500,500)))
# cv2.waitKey(0)
# cv2.destroyAllWindows()

