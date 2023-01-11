import cv2 as cv
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
from detectron2.modeling import build_model
import torch

from rehan.utils import encodeImageIntoBase64


class Detector:

	def __init__(self,filename):

		self.model = 'mask_rcnn_R_50_FPN_3x.yaml'
		self.filename = filename
		self.cfg = get_cfg()
		self.cfg.merge_from_file("config.yml")

		self.cfg.MODEL.DEVICE = "cpu"
		self.cfg.MODEL.WEIGHTS = "model_final.pth"
		self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.75

	def convert_model_for_inference(self):

		model = build_model(self.cfg)
		torch.save(model.state_dict(), 'checkpoint.pth')
		return 'checkpoint.pth'


	def inference(self, file):

		predictor = DefaultPredictor(self.cfg)
		im = cv.imread(file)
		outputs = predictor(im)
		metadata = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0])
		v = Visualizer(im[:, :, ::-1], metadata=metadata, scale=1.2)
		v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
		cv.imwrite('img.jpg',v.get_image())
		opencodedbase64 = encodeImageIntoBase64("img.jpg")
		result = {"image" : opencodedbase64.decode('utf-8') }
		return result
